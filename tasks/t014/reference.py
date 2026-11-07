"""Pinned witness and evaluator wrapper for T014."""
from tasks.t014.human import run_code
from mathbench.evaluate import evaluate_candidate

def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T014", program_path, config_id, **kwargs)
