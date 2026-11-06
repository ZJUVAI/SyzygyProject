"""Pinned witness and evaluator wrapper for T079."""
from tasks.t079.human import run_code
from mathbench.evaluate import evaluate_candidate

def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T079", program_path, config_id, **kwargs)
