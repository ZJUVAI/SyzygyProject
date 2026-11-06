from mathbench.search import search_deadline, search_steps
"""Seeded mass-preserving pair-transfer search; reads no human data."""
from fractions import Fraction
import os
import random
import time

from tasks.t082.check import objective_fraction
from tasks.t082.init_program import run_code as initial


def run_code():
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    heights = [Fraction(str(x)) for x in initial()["heights"]]
    current, _, _ = objective_fraction(heights)
    best, best_value = heights[:], current
    try:
        seconds = max(0.0, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2")))
    except ValueError:
        seconds = 2.0
    deadline = search_deadline()
    quantum = Fraction(1, 1000)
    for _attempt in search_steps(100):
        i, j = rng.sample(range(51), 2)
        delta = quantum * rng.randint(1, 100) * rng.choice((-1, 1))
        candidate = best[:]
        candidate[i] += delta
        candidate[j] -= delta
        if not (0 <= candidate[i] <= 1 and 0 <= candidate[j] <= 1):
            continue
        value, _, _ = objective_fraction(candidate)
        if value < best_value:
            best, best_value = candidate, value
    return {"heights": [str(x) for x in best]}
