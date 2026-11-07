from mathbench.search import search_deadline, search_steps
"""Bounded random-restart coordinate search baseline."""
import random
import os
import time
from itertools import combinations

from .check import triangle_area2, validate


def _score(points):
    return min(triangle_area2(*triple) for triple in combinations(points, 3)) / 2


def run_code():
    seed, restarts, steps = int(os.environ.get('MATHBENCH_SEED', '0')), 8, 1200
    n = {'T005-C01': 11, 'T005-C02': 12, 'T005-C03': 16}.get(os.environ.get('MATHBENCH_CONFIG_ID', 'T005-C01'), 11)
    deadline = search_deadline()
    rng = random.Random(seed)
    best = None
    for _ in range(restarts):
        points = [(rng.random(), rng.random()) for _ in range(n)]
        score = _score(points)
        scale = 0.18
        for step in range(steps):
            if time.monotonic() >= deadline:
                break
            i = rng.randrange(n)
            candidate = list(points)
            x, y = candidate[i]
            candidate[i] = (min(1., max(0., x + rng.gauss(0, scale))),
                            min(1., max(0., y + rng.gauss(0, scale))))
            new_score = _score(candidate)
            if new_score >= score:
                points, score = candidate, new_score
            if (step + 1) % 200 == 0:
                scale *= .65
        if best is None or score > best[0]:
            best = (score, points)
        if time.monotonic() >= deadline:
            break
    solution = {"points": [[format(x, ".17g"), format(y, ".17g")] for x, y in best[1]]}
    validate(solution, {"parameters": {"n": n}})
    return solution
