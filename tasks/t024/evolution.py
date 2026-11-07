"""Task-local EVOLVE entry point and exact score helper."""
from tasks.t024.baseline import run_code
from tasks.t024.check import validate

def score(solution, config):
    return validate(solution, config)["objective"]
