from mathbench.search import search_deadline, search_steps
"""Seeded local search using exact determinant scores."""
import os
import random
import time
from tasks.t089.init_program import run_code as initial
from tasks.t089.check import determinant_bareiss


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    matrix = initial()["matrix"]
    score = abs(determinant_bareiss(matrix))
    best = [row[:] for row in matrix]
    best_score = score
    budget = max(0.0, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2")))
    deadline = search_deadline()
    # Each step flips one row or one entry; no witness data is read.
    for _attempt in search_steps(100):
        if _attempt % 25 == 0:
            restart = [[rng.choice((-1, 1)) for _ in range(29)] for _ in range(29)]
            restart_score = abs(determinant_bareiss(restart))
            if restart_score > best_score:
                best, best_score = restart, restart_score
        candidate = [row[:] for row in best]
        if rng.random() < 0.2:
            i = rng.randrange(29)
            candidate[i] = [-x for x in candidate[i]]
        else:
            i, j = rng.randrange(29), rng.randrange(29)
            candidate[i][j] = -candidate[i][j]
        value = abs(determinant_bareiss(candidate))
        if value >= best_score:
            best, best_score = candidate, value
    return {"matrix": best}
