"""Shared-runner adapter for T068."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T068", program_path, config_id, **kwargs)
