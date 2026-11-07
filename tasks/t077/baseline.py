"""Seeded local search from the small set {0,1,3}."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t077.search_utils import heuristic_score, mutate


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T077-C01") != "T077-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(5000, int(os.environ.get("MATHBENCH_BASELINE_ITERATIONS", "500"))))
    rng = random.Random(seed ^ 0x058BA5E)
    current = [0, 1, 3]
    current_score = heuristic_score(current)
    best, best_score = current[:], current_score
    completed = accepted = 0
    start = time.monotonic()
    for _ in search_steps(iterations):
        candidate = mutate(current, rng)
        candidate_score = heuristic_score(candidate)
        if candidate_score > current_score or (candidate_score == current_score and rng.random() < 0.05):
            current, current_score = candidate, candidate_score
            accepted += 1
        if candidate_score > best_score:
            best, best_score = candidate, candidate_score
        completed += 1
    return {
        "set": best,
        "search_metadata": {
            "algorithm": "seeded one-element replacement/add/remove hill climb with occasional plateau moves",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_run": completed,
            "accepted_moves": accepted,
            "heuristic_score": best_score,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed iterations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
