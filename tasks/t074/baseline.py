"""Seeded local search from the simple parabola construction."""

import os
import random
import time
from fractions import Fraction

from mathbench.search import search_steps
from tasks.t074.check import PARAMETERS, validate


CONFIG = {"id": "T074-C01", "parameters": PARAMETERS}


def _score(points):
    return Fraction(validate({"points": points}, CONFIG)["objective"])


def _mutate(points, rng, coordinate_limit):
    child = [list(point) for point in points]
    index = rng.randrange(len(child))
    child[index] = [rng.randint(-coordinate_limit, coordinate_limit),
                    rng.randint(-coordinate_limit, coordinate_limit)]
    return child


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T074-C01") != "T074-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(3000, int(os.environ.get("MATHBENCH_BASELINE_ITERATIONS", "300"))))
    coordinate_limit = max(12, min(1000, int(os.environ.get("MATHBENCH_SEARCH_COORDINATE_LIMIT", "40"))))
    rng = random.Random(seed ^ 0x013BA5E)
    current = [[i, i * i] for i in range(12)]
    current_score = _score(current)
    best, best_score = [point[:] for point in current], current_score
    completed = accepted = invalid = 0
    start = time.monotonic()
    for _ in search_steps(iterations):
        candidate = _mutate(current, rng, coordinate_limit)
        try:
            candidate_score = _score(candidate)
        except ValueError:
            invalid += 1
            completed += 1
            continue
        if candidate_score > current_score or (candidate_score == current_score and rng.random() < 0.08):
            current, current_score = candidate, candidate_score
            accepted += 1
        if candidate_score > best_score:
            best, best_score = [point[:] for point in candidate], candidate_score
        completed += 1
    return {
        "points": best,
        "search_metadata": {
            "algorithm": "seeded one-point integer-coordinate hill climb with occasional equal-score plateau moves",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_run": completed,
            "accepted_moves": accepted,
            "invalid_trials": invalid,
            "search_only_coordinate_proposal_limit": coordinate_limit,
            "best_objective": str(best_score),
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed iterations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
