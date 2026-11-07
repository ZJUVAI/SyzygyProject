"""Fixed-work seeded random dispatch search, independent of reference assets."""

import os
import random

from tasks.t056.dispatch import generate_active_schedule
from tasks.t056.init_program import run_code as initial_run
from tasks.t056.check import PARAMETERS, validate


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T056-C01") != "T056-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(1000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "32"))))
    rng = random.Random(seed)
    best = initial_run()["machine_orders"]
    best_value = validate({"machine_orders": best}, {"parameters": PARAMETERS})["objective"]
    accepted = 0
    for iteration in range(iterations):
        candidate = generate_active_schedule(
            seed=rng.randrange(1 << 30), rule="random_priority", randomized=True
        )
        value = validate({"machine_orders": candidate}, {"parameters": PARAMETERS})["objective"]
        accepted += 1
        if value < best_value:
            best, best_value = candidate, value
    return {
        "machine_orders": best,
        "search_metadata": {
            "algorithm": "multi-start Giffler-Thompson active-schedule generator with seeded random conflict-set choices",
            "seed": seed,
            "iterations_requested": iterations,
            "iterations_run": iterations,
            "candidates_checked": accepted,
            "objective_recomputed": best_value,
            "budget": {"mode": "fixed iterations; runner generation timeout 300 seconds", "runner_generation_seconds": 300},
        },
    }
