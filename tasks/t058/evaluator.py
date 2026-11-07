"""Shared-runner adapter for T058."""

from mathbench.evaluate import evaluate_candidate


def evaluate(program_path, config_id=None, **kwargs):
    return evaluate_candidate("T058", program_path, config_id, **kwargs)
