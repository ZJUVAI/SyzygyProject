"""Task-local EVOLVE entry point and exact score helper."""
from tasks.t033.baseline import run_code
from tasks.t033.check import validate

def score(solution, config):
    return validate(solution, config)["objective"]
