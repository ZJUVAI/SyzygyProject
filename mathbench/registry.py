"""Read task packages without executing candidate code."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
INITIAL_TASKS = ("T001", "T002", "T005", "T009", "T014", "T035", "T044", "T060", "T066", "T067", "N001", "T057", "T073", "T079", "T080", "T081", "T082", "T089", "T099", "T097")


def task_path(task_id):
    if task_id not in INITIAL_TASKS:
        raise ValueError("Unknown task ID")
    return TASKS / task_id.lower()


def load_task(task_id):
    return json.loads((task_path(task_id) / "task.json").read_text())


def load_config(task_id, config_id=None):
    task = load_task(task_id)
    configs = task["configurations"]
    if config_id is None:
        return configs[0]
    for config in configs:
        if config["id"] == config_id:
            return config
    raise ValueError("Unknown configuration ID")
