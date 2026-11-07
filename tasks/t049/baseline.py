"""Seeded fixed-budget search over 10x10 square-grid 91-point subsets."""

import os
import random
import time


N = 91
SIDE = 10
ITERATION_LIMIT = 128
GRID = [(x, y) for x in range(SIDE) for y in range(SIDE)]


def _score(points):
    return len({(points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2
                for i in range(N) for j in range(i)})


def _solution(points):
    return {
        "minimal_polynomial": [0, 1],
        "isolating_interval": ["-1", "1"],
        "points": [{"x": [str(x)], "y": [str(y)]} for x, y in points],
    }


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T049-C01")
    if config_id != "T049-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None if seconds is None else time.monotonic() + max(0.0, float(seconds))
    incumbent = [(i, 0) for i in range(N)]
    incumbent_score = _score(incumbent)
    iterations = 0
    for _ in range(ITERATION_LIMIT):
        if deadline is not None and time.monotonic() >= deadline:
            break
        candidate = rng.sample(GRID, N)
        score = _score(candidate)
        iterations += 1
        if score < incumbent_score:
            incumbent, incumbent_score = candidate, score
    return {
        **_solution(incumbent),
        "search_metadata": {
            "algorithm": "sample 91-point subsets of the integer 10x10 square grid; keep lowest exact integer squared-distance count",
            "seed": seed,
            "iteration_limit": ITERATION_LIMIT,
            "iterations": iterations,
            "budget": {"iteration_limit": ITERATION_LIMIT},
            "reference_data_read": False,
            "search_seconds_cutoff": seconds,
        },
    }
