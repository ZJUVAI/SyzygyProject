"""Recompute a saved witness without its original construction program."""
import json
from pathlib import Path
import tempfile
from .evaluate import evaluate_candidate


def replay(task_id, solution_path, config_id=None, **kwargs):
    solution = json.loads(Path(solution_path).read_text())
    with tempfile.TemporaryDirectory(prefix="mathbench-replay-") as directory:
        program = Path(directory) / "saved.py"
        program.write_text("def run_code():\n    return " + repr(solution) + "\n")
        return evaluate_candidate(task_id, program, config_id, **kwargs)
