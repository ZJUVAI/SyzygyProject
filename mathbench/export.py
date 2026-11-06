"""Prepare only the public seed material for a separate model workspace."""
import json
from pathlib import Path
import shutil
from .registry import load_config, task_path


def export_seed(task_id, destination, config_id=None):
    config = load_config(task_id, config_id)
    folder = Path(destination)
    folder.mkdir(parents=True, exist_ok=False)
    source = task_path(task_id)
    for name in ("init_program.py", "instruction.txt"):
        shutil.copyfile(source / name, folder / name)
    if task_id == "T035":
        shutil.copyfile(source / "lps.py", folder / "lps.py")
    # No normalization reference or record data is exposed.
    public = {k: config[k] for k in ("id", "parameters", "direction")}
    (folder / "configuration.json").write_text(json.dumps(public, ensure_ascii=False, indent=2)+"\n")
    return folder
