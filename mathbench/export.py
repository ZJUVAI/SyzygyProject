"""Prepare only the public seed material for a separate model workspace."""
import json
from pathlib import Path
import shutil
from .registry import load_config, task_path

# Sol-reviewed input files. Comparison witnesses are never exported.
PUBLIC_INPUTS = {
    'T028': ('data/source/uniform-0000500-1.instance.json',),
    'T029': ('data/source/socg_fixed92.instance.json',),
    'T006': ('data/source/random_cf2_74ae2d30_50.cgshop2024_instance.json',),
    'T044': ('data/source/arc130.mtx.rnd',),
    'T096': ('data/source/mona-lisa100K.tsp.gz',),
    'T026': ('data/source/ortho40.instance.json',),
    'T039': ('data/source/C2000.9.bits',),
    'T097': ('data/source/X-n1001-k43.vrp',),
    'T098': ('data/source/b4794d123e18a908924d3d33cdeeae3b.wcnf.gz',),
    'T095': ('data/source/ta41_instance.json',),
    'T043': ('data/source/gd96a.rmf',),
    'T042': ('data/source/G70.gz',),
    'T038': ('data/DSJC1000.5.bits',),
    'T093': ('data/tai256c.dat.gz',),
    'T094': ('data/ta051.json',),
}


def export_seed(task_id, destination, config_id=None):
    config = load_config(task_id, config_id)
    folder = Path(destination)
    folder.mkdir(parents=True, exist_ok=False)
    source = task_path(task_id)
    for name in ("init_program.py", "instruction.txt"):
        shutil.copyfile(source / name, folder / name)
    if task_id == "T030":
        shutil.copyfile(source / "lps.py", folder / "lps.py")
    for relative in PUBLIC_INPUTS.get(task_id, ()):
        target = folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / relative, target)
    # No normalization reference or record data is exposed.
    public = {k: config[k] for k in ("id", "parameters", "direction")}
    (folder / "configuration.json").write_text(json.dumps(public, ensure_ascii=False, indent=2)+"\n")
    return folder
