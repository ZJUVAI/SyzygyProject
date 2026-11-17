"""Read task packages without executing candidate code."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"
INITIAL_TASKS = tuple(
    f"T{number:03d}" for number in range(1, 103) if number not in (86, 96)
)


def resolve_task_id(value):
    task_id = value.upper()
    if task_id in INITIAL_TASKS:
        return task_id
    raise ValueError(f"Unknown task {value!r}. Run mathbench list for the official catalog.")


def task_path(task_id):
    if task_id not in INITIAL_TASKS:
        raise ValueError("Unknown task ID")
    return TASKS / task_id.lower()


def load_task(task_id):
    """Read the task and expose its accepted configuration."""
    task = json.loads((task_path(task_id) / "task.json").read_text())
    configs = task["configurations"]
    if len(configs) != 1:
        raise ValueError(f"{task_id}: expected one configuration")
    config = configs[0]
    if task.get("official_configuration", config["id"]) != config["id"]:
        raise ValueError(f"{task_id}: invalid official configuration")
    if config.get("acceptance_status", "accepted_by_sol") != "accepted_by_sol":
        task["configurations"] = []
    return task


def load_config(task_id, config_id=None):
    configs = load_task(task_id)["configurations"]
    if config_id is None:
        if configs:
            return configs[0]
        raise ValueError(f"{task_id} has no accepted configuration.")
    if configs and configs[0]["id"] == config_id:
        return configs[0]
    raise ValueError("Unknown configuration ID")
