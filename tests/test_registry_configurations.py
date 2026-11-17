"""Draft configurations must not enter released runs before admission."""
import json
import re

import pytest

from mathbench import registry
from mathbench.saved_result import best_record_path, read_best_record


def test_pending_configurations_are_excluded_until_acceptance(tmp_path, monkeypatch):
    task = {
        "task_id": "T001",
        "official_configuration": "T001-C01",
        "configurations": [
            {"id": "T001-C01", "acceptance_status": "pending_sol_review"},
        ],
    }
    path = tmp_path / "task.json"
    path.write_text(json.dumps(task))
    monkeypatch.setattr(registry, "task_path", lambda _: tmp_path)
    with pytest.raises(ValueError, match="no accepted configuration"):
        registry.load_config("T001")
    with pytest.raises(ValueError, match="Unknown configuration"):
        registry.load_config("T001", "T001-C01")

    task["configurations"][0]["acceptance_status"] = "accepted_by_sol"
    path.write_text(json.dumps(task))
    assert registry.load_config("T001", "T001-C01")["id"] == "T001-C01"


def test_release_uses_one_configuration_per_active_task():
    assert len(registry.INITIAL_TASKS) == len(set(registry.INITIAL_TASKS)) == 100
    assert {"T101", "T102"} <= set(registry.INITIAL_TASKS)
    assert not set(registry.ARCHIVED_TASKS).intersection(registry.INITIAL_TASKS)
    for task in registry.INITIAL_TASKS:
        config_id = f"{task}-C02" if task == "T003" else f"{task}-C01"
        directory = registry.task_path(task)
        manifest = json.loads((directory / "task.json").read_text())
        assert [c["id"] for c in manifest["configurations"]] == [config_id]
        assert not (directory / "best").exists()
        assert not (directory / "review").exists()
        best = directory / "data/best"
        path = best_record_path(best)
        assert list(best.iterdir()) == [path]
        result = read_best_record(path)["result"]
        assert result["config_id"] == config_id
        assert [c["id"] for c in registry.load_task(task)["configurations"]] == [config_id]
        for config in registry.load_task(task, include_history=True)["configurations"]:
            assert registry.load_config(task, config["id"]) == config
            assert config["id"] == config_id


def test_task_programs_and_data_have_no_removed_configuration_ids():
    for task in (*registry.INITIAL_TASKS, *registry.ARCHIVED_TASKS):
        directory = registry.task_path(task)
        config_id, = [config["id"] for config in
                      registry.load_task(task, include_history=True)["configurations"]]
        program_ids = re.compile(rf"\b{task}-C\d+\b")
        for path in directory.glob("*.py"):
            if not path.name.startswith("test"):
                assert set(program_ids.findall(path.read_text())) <= {config_id}, path
        filename_ids = re.compile(r"(?<![a-z0-9])C\d{2}(?!\d)", re.IGNORECASE)
        for path in (directory / "data").rglob("*"):
            if path.is_file():
                suffixes = {match.upper() for match in filename_ids.findall(path.name)}
                assert suffixes <= {config_id.split("-")[1]}, path


@pytest.mark.parametrize(("task", "config_id"), [
    ("T003", "T003-C01"),
    ("T006", "T006-C02"),
])
def test_removed_configuration_is_not_available(task, config_id):
    with pytest.raises(ValueError, match="Unknown configuration"):
        registry.load_config(task, config_id)


@pytest.mark.parametrize("task", registry.ARCHIVED_TASKS)
def test_retired_task_requires_explicit_config(task):
    assert registry.resolve_task_id(task.lower()) == task
    assert not registry.load_task(task)["configurations"]
    assert registry.load_config(task, f"{task}-C01")["id"] == f"{task}-C01"
    with pytest.raises(ValueError, match="archived"):
        registry.load_config(task)
