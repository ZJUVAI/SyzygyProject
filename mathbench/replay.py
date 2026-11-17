"""Recompute a saved witness without its original construction program."""
import gzip
import json
from pathlib import Path
import tempfile
from .evaluate import evaluate_candidate
from .saved_result import best_record_path, extract_witness, read_best_record


def witness_path(path):
    """Resolve current and previous saved-construction paths."""
    path = Path(path)
    if path.is_file():
        return path
    if path.parent.name == "best" and path.name in ("solution.json", "solution.json.gz", "result.json"):
        record = best_record_path(path.parent)
        if record.is_file():
            return record
    task = path.parent.parent.parent
    if path.parent.parent.name == "best" and task.name == path.parent.name.split("-")[0].lower():
        best = task / "data" / "best"
        record = best_record_path(best)
        if record.is_file() and read_best_record(record)["result"]["config_id"] == path.parent.name:
            return record
    if path.suffix == ".json":
        packed = path.with_suffix(".json.gz")
        if packed.is_file():
            return packed
    return path


def read_witness_bytes(path):
    """Read the original bytes used for witness hashes."""
    path = witness_path(path)
    contents = path.read_bytes()
    if path.suffix == ".gz":
        contents = gzip.decompress(contents)
    return extract_witness(contents) if path.name in ("result.json", "result.json.gz") else contents


def replay(task_id, solution_path, config_id=None, **kwargs):
    solution = json.loads(read_witness_bytes(solution_path))
    with tempfile.TemporaryDirectory(prefix="mathbench-replay-") as directory:
        program = Path(directory) / "saved.py"
        program.write_text("def run_code():\n    return " + repr(solution) + "\n")
        return evaluate_candidate(task_id, program, config_id, **kwargs)
