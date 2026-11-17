"""Recompute a saved witness without its original construction program."""
import gzip
import json
from pathlib import Path
import tempfile
from .evaluate import evaluate_candidate


def witness_path(path):
    """Resolve an old JSON path to its compressed copy when necessary."""
    path = Path(path)
    if path.suffix == ".json" and not path.is_file():
        packed = path.with_suffix(".json.gz")
        if packed.is_file():
            return packed
    return path


def read_witness_bytes(path):
    """Read the original bytes used for witness hashes."""
    path = witness_path(path)
    if path.suffix == ".gz":
        return gzip.decompress(path.read_bytes())
    return path.read_bytes()


def replay(task_id, solution_path, config_id=None, **kwargs):
    solution = json.loads(read_witness_bytes(solution_path))
    with tempfile.TemporaryDirectory(prefix="mathbench-replay-") as directory:
        program = Path(directory) / "saved.py"
        program.write_text("def run_code():\n    return " + repr(solution) + "\n")
        return evaluate_candidate(task_id, program, config_id, **kwargs)
