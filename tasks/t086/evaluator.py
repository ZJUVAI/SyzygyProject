"""Shared evaluator adapter for T086."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T086", program_path, config_id, **kwargs)
