"""Seeded traditional local search from the simple initial set."""

import os
import random
import time

from mathbench.search import search_steps
from tasks.t072.search_utils import mutate, score, search_integer_limit


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T072-C01") != "T072-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(5000, int(os.environ.get("MATHBENCH_BASELINE_ITERATIONS", "500"))))
    limit = search_integer_limit()
    rng = random.Random(seed ^ 0x055BA5E)
    current = list(range(1, 33))
    current_score = score(current)
    best, best_score = list(current), current_score
    accepted = 0
    completed = 0
    start = time.monotonic()
    for _ in search_steps(iterations):
        candidate = mutate(current, rng, limit)
        candidate_score = score(candidate)
        # Hill climbing with occasional equal-score moves explores plateaus.
        if candidate_score < current_score or (candidate_score == current_score and rng.random() < 0.08):
            current, current_score = candidate, candidate_score
            accepted += 1
        if candidate_score < best_score:
            best, best_score = candidate, candidate_score
        completed += 1
    return {
        "elements": best,
        "search_metadata": {
            "algorithm": "seeded one/two-element replacement hill climb with occasional equal-score plateau moves",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_run": completed,
            "accepted_moves": accepted,
            "search_only_integer_proposal_limit": limit,
            "best_objective": best_score,
            "generation_seconds": time.monotonic() - start,
            "budget": "fixed iterations unless MATHBENCH_SEARCH_SECONDS sets a wall-clock cutoff; runner cap 300 seconds",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
