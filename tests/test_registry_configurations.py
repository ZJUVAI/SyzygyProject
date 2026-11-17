"""Draft configurations must not enter released runs before admission."""
import json

import pytest

from mathbench import registry


def test_pending_configurations_are_excluded_until_acceptance(tmp_path, monkeypatch):
    task = {
        "task_id": "T001",
        "configurations": [
            {"id": "T001-C01"},
            {"id": "T001-C02", "acceptance_status": "pending_sol_review"},
        ],
    }
    path = tmp_path / "task.json"
    path.write_text(json.dumps(task))
    monkeypatch.setattr(registry, "task_path", lambda _: tmp_path)
    assert registry.load_config("T001")["id"] == "T001-C01"
    with pytest.raises(ValueError, match="Unknown configuration"):
        registry.load_config("T001", "T001-C02")

    task["configurations"][1]["acceptance_status"] = "accepted_by_sol"
    path.write_text(json.dumps(task))
    assert registry.load_config("T001", "T001-C02")["id"] == "T001-C02"


def test_release_uses_one_configuration_per_active_task():
    assert len(registry.INITIAL_TASKS) == len(set(registry.INITIAL_TASKS)) == 100
    assert {"T101", "T102"} <= set(registry.INITIAL_TASKS)
    assert not set(registry.ARCHIVED_TASKS).intersection(registry.INITIAL_TASKS)
    historical = 0
    for task in registry.INITIAL_TASKS:
        config_id = f"{task}-C02" if task == "T003" else f"{task}-C01"
        assert [c["id"] for c in registry.load_task(task)["configurations"]] == [config_id]
        for config in registry.load_task(task, include_history=True)["configurations"]:
            assert registry.load_config(task, config["id"]) == config
            historical += config["id"] != config_id
    assert historical == 39


@pytest.mark.parametrize("task", registry.ARCHIVED_TASKS)
def test_retired_task_requires_explicit_config(task):
    assert registry.resolve_task_id(task.lower()) == task
    assert not registry.load_task(task)["configurations"]
    assert registry.load_config(task, f"{task}-C01")["id"] == f"{task}-C01"
    with pytest.raises(ValueError, match="archived"):
        registry.load_config(task)
