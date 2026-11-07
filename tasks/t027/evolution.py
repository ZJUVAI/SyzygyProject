"""Task-limited search entry point used for evolution runs."""
from tasks.t027.baseline import run_code as _baseline_run_code


def run_code():
    return _baseline_run_code()
