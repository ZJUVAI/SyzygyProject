from mathbench.search import search_deadline, search_steps
"""Bounded seeded coordinate-edit search; no human witness data is read."""
from fractions import Fraction
import os
import random
import time

from tasks.t015.check import objective_fraction
from tasks.t015.init_program import run_code as initial


def run_code():
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    coefficients = [int(x) for x in initial()["coefficients"]]
    current, _ = objective_fraction([Fraction(x) for x in coefficients])
    best, best_value = coefficients[:], current
    try:
        seconds = max(0.0, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2")))
    except ValueError:
        seconds = 2.0
    deadline = search_deadline()
    for _attempt in search_steps(200):
        candidate = best[:]
        i = rng.randrange(20)
        candidate[i] = max(0, candidate[i] + rng.randint(-max(1, candidate[i]//3), max(1, candidate[i]//3)))
        if not any(candidate):
            continue
        value, _ = objective_fraction([Fraction(x) for x in candidate])
        if value > best_value:
            best, best_value = candidate, value
    return {"coefficients": best}
