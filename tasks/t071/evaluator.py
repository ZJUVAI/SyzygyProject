"""Shared evaluator adapter for T071."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T071", program_path, config_id, **kwargs)
