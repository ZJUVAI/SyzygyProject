"""Seeded dynamic-degree multi-start and exact one-for-two clique search."""

import os
import random

from tasks.t059.check import PARAMETERS, validate
from tasks.t059.graph import greedy_clique, improve_clique
from tasks.t059.init_program import run_code as initial_run


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T059-C01") != "T059-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(20000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "256"))))
    rng = random.Random(seed)
    best = list(initial_run()["vertices"])
    best_value = validate({"vertices": best}, {"parameters": PARAMETERS})["objective"]
    accepted = improvements = 0
    for _ in range(iterations):
        candidate = greedy_clique(rng.randrange(1 << 30), randomized=True, degree_mode="dynamic")
        candidate = improve_clique(candidate, rounds=6)
        value = validate({"vertices": candidate}, {"parameters": PARAMETERS})["objective"]
        accepted += 1
        if value > best_value:
            best, best_value = candidate, value
            improvements += 1
    return {
        "vertices": best,
        "search_metadata": {
            "algorithm": "multi-start randomized dynamic-degree greedy clique construction with repeated one-for-two improvement",
            "seed": seed,
            "initial_objective": 1,
            "iterations_requested": iterations,
            "iterations_run": iterations,
            "candidates_checked": accepted,
            "best_improvements": improvements,
            "objective_recomputed": best_value,
            "budget": {"mode": "fixed iterations; runner generation timeout 300 seconds", "runner_generation_seconds": 300},
        },
    }
