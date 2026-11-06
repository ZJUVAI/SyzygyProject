"""Fixed search counts by default; optional wall-clock cutoffs for exploration."""
import os
import time


def search_deadline():
    value = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    return float("inf") if value is None else time.monotonic() + max(0., min(30., float(value)))


def search_steps(count):
    deadline = search_deadline()
    for step in range(count):
        if time.monotonic() >= deadline:
            break
        yield step
