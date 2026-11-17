"""Read task packages without executing candidate code."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
# Archived task IDs remain valid for explicit replay.
ARCHIVED_TASKS = ("T086", "T096")
INITIAL_TASKS = tuple(
    task for number in range(1, 103)
    if (task := f"T{number:03d}") not in ARCHIVED_TASKS
)


def resolve_task_id(value):
    task_id = value.upper()
    if task_id in INITIAL_TASKS or task_id in ARCHIVED_TASKS:
        return task_id
    raise ValueError(f"Unknown task {value!r}. Run mathbench list for the official catalog.")


def task_path(task_id):
    if task_id not in INITIAL_TASKS and task_id not in ARCHIVED_TASKS:
        raise ValueError("Unknown task ID")
    return TASKS / task_id.lower()


def load_task(task_id, *, include_history=False):
    task = json.loads((task_path(task_id) / "task.json").read_text())
    task["configurations"] = [
        config for config in task["configurations"]
        if config.get("acceptance_status", "accepted_by_sol") == "accepted_by_sol"
    ]
    official = task.get("official_configuration")
    if official is not None:
        active = [config for config in task["configurations"] if config["id"] == official]
        if len(active) != 1:
            raise ValueError(f"{task_id}: invalid official configuration {official!r}")
        if not include_history:
            task["configurations"] = active
    if task_id in ARCHIVED_TASKS and not include_history:
        task["configurations"] = []
    return task


def load_config(task_id, config_id=None):
    if config_id is None:
        configs = load_task(task_id)["configurations"]
        if not configs:
            raise ValueError(f"{task_id} is archived. Specify its configuration ID.")
        return configs[0]
    configs = load_task(task_id, include_history=True)["configurations"]
    for config in configs:
        if config["id"] == config_id:
            return config
    raise ValueError("Unknown configuration ID")
