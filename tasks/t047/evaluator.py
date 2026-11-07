"""Shared evaluator adapter for T047."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T047", program_path, config_id, **kwargs)
