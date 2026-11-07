"""Shared-runner adapter for T049."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T049", program_path, config_id, **kwargs)
