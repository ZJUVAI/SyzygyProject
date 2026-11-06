"""The evaluator interface shared by SimpleTES and DREAM-RSI."""
from .evaluate import evaluate_candidate


def make_evaluator(task_id, config_id=None, *, strict=False):
    """Return an evaluate(program_path) callable for either framework."""
    def evaluate(program_path):
        return evaluate_candidate(task_id, program_path, config_id, strict=strict)
    return evaluate
