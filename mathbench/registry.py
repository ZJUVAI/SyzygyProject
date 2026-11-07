"""Read task packages without executing candidate code."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
# The v1.0 catalog contains one hundred consecutively numbered tasks.
INITIAL_TASKS = tuple(f"T{number:03d}" for number in range(1, 101))


def resolve_task_id(value):
    task_id = value.upper()
    if task_id in INITIAL_TASKS:
        return task_id
    raise ValueError(f"Unknown task {value!r}. Use T001–T100.")


def task_path(task_id):
    if task_id not in INITIAL_TASKS:
        raise ValueError("Unknown task ID")
    return TASKS / task_id.lower()


def load_task(task_id):
    task = json.loads((task_path(task_id) / "task.json").read_text())
    task["configurations"] = [
        config for config in task["configurations"]
        if config.get("acceptance_status", "accepted_by_sol") == "accepted_by_sol"
    ]
    return task


def load_config(task_id, config_id=None):
    task = load_task(task_id)
    configs = task["configurations"]
    if config_id is None:
        return configs[0]
    for config in configs:
        if config["id"] == config_id:
            return config
    raise ValueError("Unknown configuration ID")
