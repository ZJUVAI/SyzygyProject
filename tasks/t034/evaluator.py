"""Shared runner adapter for T034."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T034", program_path, config_id, **kwargs)
