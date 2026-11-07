"""Shared-runner adapter for T062."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T062", program_path, config_id, **kwargs)
