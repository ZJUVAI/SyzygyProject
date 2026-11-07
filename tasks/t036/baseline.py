"""Seeded random point replacement search; comparison assets are never read."""
from __future__ import annotations

import os
import random

from mathbench.search import search_steps
from tasks.t036.check import validate

ITERATION_LIMIT = 80
_CONFIG = {
    "id": "T036-C01",
    "parameters": {
        "vertices": 28,
        "graph": "complete graph K28",
        "general_position": "no three points collinear",
        "crossing_definition": "unordered pairs of disjoint straight edges whose relative interiors intersect",
    },
}


def _candidate(rng):
    while True:
        points = []
        seen = set()
        while len(points) < 28:
            p = (rng.randrange(-10000, 10001), rng.randrange(-10000, 10001))
            if p not in seen:
                seen.add(p)
                points.append(p)
        if _general_position(points):
            return points


def _general_position(points):
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    for i in range(28):
        for j in range(i + 1, 28):
            for k in range(j + 1, 28):
                if orient(points[i], points[j], points[k]) == 0:
                    return False
    return True


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T036-C01")
    if config_id != "T036-C01":
        raise ValueError("unsupported configuration id")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    current = _candidate(rng)
    score = validate({"points": [list(p) for p in current]}, _CONFIG)["objective"]
    best, best_score = list(current), score
    steps = iter(search_steps(ITERATION_LIMIT))
    iterations = accepted = 0
    for _ in range(ITERATION_LIMIT):
        if next(steps, None) is None:
            break
        iterations += 1
        index = rng.randrange(28)
        point = (rng.randrange(-10000, 10001), rng.randrange(-10000, 10001))
        if point in current:
            continue
        trial = list(current)
        trial[index] = point
        if not _general_position(trial):
            continue
        trial_score = validate({"points": [list(p) for p in trial]}, _CONFIG)["objective"]
        if trial_score <= score:
            current, score = trial, trial_score
            accepted += 1
            if score < best_score:
                best, best_score = list(current), score
    return {
        "points": [list(p) for p in best],
        "claimed_objective": best_score,
        "search_metadata": {
            "algorithm": "seeded random general-position integer initialization with greedy single-point replacement",
            "configuration_id": config_id,
            "seed": seed,
            "iterations": iterations,
            "iteration_limit": ITERATION_LIMIT,
            "accepted_moves": accepted,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "reference_data_read": False,
            "budget": {"iteration_limit": ITERATION_LIMIT, "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS")}
        }
    }
