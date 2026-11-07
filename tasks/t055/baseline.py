"""Seeded bounded local search over hard-feasible Boolean assignments."""

import os
import random
import time

from tasks.t055.check import PARAMETERS, validate
from tasks.t055.maxsat import HARD, SOFT, hard_sat_assignment, random_perturb, score_assignment


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T055-C01") != "T055-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "128"))))
    from mathbench.search import search_steps

    rng = random.Random(seed)
    assignment = hard_sat_assignment(HARD)
    best = assignment[:]
    best_score = score_assignment(best, HARD, SOFT)["soft_satisfied_weight"]
    current = assignment[:]
    start = time.monotonic()
    attempted = 0
    accepted = 0
    for step in search_steps(iterations):
        attempted += 1
        candidate = random_perturb(rng, current, rng.randint(1, 8))
        result = score_assignment(candidate, HARD, SOFT)
        if result["hard_satisfied"] == len(HARD):
            score = result["soft_satisfied_weight"]
            if score > best_score:
                best, best_score = candidate, score
                current = candidate
                accepted += 1
            elif rng.random() < 0.08:
                current = candidate
    result = {"assignment": best}
    validate(result, {"parameters": PARAMETERS}, strict=True)
    result["search_metadata"] = {
        "algorithm": "seeded random block-flip search; retain hard-feasible improving assignments",
        "seed": seed,
        "iterations_requested": iterations,
        "iterations_run": attempted,
        "accepted_best_improvements": accepted,
        "objective_recomputed": best_score,
        "generation_seconds": time.monotonic() - start,
        "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set", "runner_generation_seconds": 300},
    }
    return result


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
