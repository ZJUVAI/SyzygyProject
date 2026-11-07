"""Prepare only the public seed material for a separate model workspace."""
import json
from pathlib import Path
import shutil
from .registry import load_config, task_path

# Sol-reviewed input files. Comparison witnesses are never exported.
PUBLIC_INPUTS = {
    'T095': ('data/source/uniform-0000500-1.instance.json',),
    'T097': ('data/source/socg_fixed92.instance.json',),
    'T093': ('data/source/random_cf2_74ae2d30_50.cgshop2024_instance.json',),
    'T088': ('data/source/arc130.mtx.rnd',),
    'T069': ('data/source/mona-lisa100K.tsp',),
    'T064': ('data/source/ortho40.instance.json',),
    'T059': ('data/source/C2000.9.clq.gz',),
    'T057': ('data/source/X-n1001-k43.vrp',),
    'T055': ('data/source/b4794d123e18a908924d3d33cdeeae3b.wcnf',),
    'T056': ('data/source/ta41_instance.json',),
    'T045': ('data/source/gd96a.rmf',),
    'T033': ('data/instance.json',),
    'T030': ('data/instance.json',),
    'T027': ('data/tai256c.dat',),
    'T028': ('data/ta051.json',),
}


def export_seed(task_id, destination, config_id=None):
    config = load_config(task_id, config_id)
    folder = Path(destination)
    folder.mkdir(parents=True, exist_ok=False)
    source = task_path(task_id)
    for name in ("init_program.py", "instruction.txt"):
        shutil.copyfile(source / name, folder / name)
    if task_id == "T006":
        shutil.copyfile(source / "lps.py", folder / "lps.py")
    for relative in PUBLIC_INPUTS.get(task_id, ()):
        target = folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, target)
    # No normalization reference or record data is exposed.
    public = {k: config[k] for k in ("id", "parameters", "direction")}
    (folder / "configuration.json").write_text(json.dumps(public, ensure_ascii=False, indent=2)+"\n")
    return folder
