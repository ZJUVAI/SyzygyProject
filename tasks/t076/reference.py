"""Pinned witness and evaluator wrapper for T076."""
from tasks.t076.human import run_code
from mathbench.evaluate import evaluate_candidate

def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T076", program_path, config_id, **kwargs)
