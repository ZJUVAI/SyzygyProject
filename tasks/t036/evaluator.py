"""Shared runner adapter for T036."""
from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T036", program_path, config_id, **kwargs)
