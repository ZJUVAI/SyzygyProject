"""Seeded local search over diagonal PSD matrices, from identity."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t086.construction import initial_diagonals, matrices_from_diagonals
from tasks.t086.search_utils import diagonal_ratio, mutate_diagonals


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T086-C01") != "T086-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(5000, int(os.environ.get("MATHBENCH_BASELINE_ITERATIONS", "250"))))
    rng = random.Random(seed ^ 0x094BA5E)
    current = initial_diagonals()
    current_score = diagonal_ratio(current)
    best, best_score = [row[:] for row in current], current_score
    accepted = completed = 0
    start = time.monotonic()
    for _ in search_steps(iterations):
        candidate = mutate_diagonals(current, rng)
        score = diagonal_ratio(candidate)
        if score < current_score or (score == current_score and rng.random() < 0.04):
            current, current_score = candidate, score
            accepted += 1
        if score < best_score:
            best, best_score = [row[:] for row in candidate], score
        completed += 1
    return {
        **matrices_from_diagonals(best),
        "search_metadata": {
            "algorithm": "seeded hill climb over four positive diagonal matrices; exact domain validation is separate",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_run": completed,
            "accepted_moves": accepted,
            "heuristic_ratio": best_score,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed iterations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
