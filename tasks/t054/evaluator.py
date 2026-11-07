"""Shared-runner adapter for T054."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T054", program_path, config_id, **kwargs)
