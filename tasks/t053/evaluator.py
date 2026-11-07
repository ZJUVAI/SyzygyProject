"""Shared benchmark evaluator adapter for T053."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T053", program_path, config_id, **kwargs)
