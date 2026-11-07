"""Shared evaluator adapter for T080."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T080", program_path, config_id, **kwargs)
