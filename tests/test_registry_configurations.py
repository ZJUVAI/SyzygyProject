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


def test_release_uses_one_consecutive_task_id_per_problem():
    assert registry.INITIAL_TASKS == tuple(f"T{i:03d}" for i in range(1, 101))
    for task in registry.INITIAL_TASKS:
        configs = registry.load_task(task)["configurations"]
        assert [c["id"] for c in configs] == [
            f"{task}-C{i:02d}" for i in range(1, len(configs) + 1)
        ]
