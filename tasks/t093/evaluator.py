"""Shared mathbench evaluator adapter for T093."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T093", program_path, config_id, **kwargs)
