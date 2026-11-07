"""Seeded multi-start and adjacent-swap search from the simple FIFO schedule."""

import os
import random

from tasks.t056.dispatch import generate_active_schedule
from tasks.t056.init_program import run_code as initial_run
from tasks.t056.check import PARAMETERS, validate


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T056-C01") != "T056-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(20000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "500"))))
    rng = random.Random(seed)
    initial = initial_run()["machine_orders"]
    initial_value = validate({"machine_orders": initial}, {"parameters": PARAMETERS})["objective"]
    best = [row[:] for row in initial]
    best_value = initial_value
    current = [row[:] for row in best]
    current_value = best_value
    feasible, improvements = 0, 0
    restart_count = max(1, (iterations * 3) // 4)
    for step in range(iterations):
        if step < restart_count:
            candidate = generate_active_schedule(
                seed=rng.randrange(1 << 30), rule="random_priority", randomized=True
            )
        else:
            machine = rng.randrange(len(current))
            position = rng.randrange(len(current[machine]) - 1)
            candidate = [row[:] for row in current]
            candidate[machine][position], candidate[machine][position + 1] = (
                candidate[machine][position + 1], candidate[machine][position]
            )
        try:
            value = validate({"machine_orders": candidate}, {"parameters": PARAMETERS})["objective"]
        except ValueError:
            continue
        feasible += 1
        if value <= current_value or rng.random() < 0.02:
            current, current_value = candidate, value
        if value < best_value:
            best, best_value = [row[:] for row in candidate], value
            improvements += 1
    return {
        "machine_orders": best,
        "search_metadata": {
            "algorithm": "multi-start randomized Giffler-Thompson schedules followed by feasible adjacent machine-order swaps",
            "seed": seed,
            "initial_objective": initial_value,
            "iterations_requested": iterations,
            "iterations_run": iterations,
            "randomized_restarts": restart_count,
            "feasible_candidates": feasible,
            "best_improvements": improvements,
            "objective_recomputed": best_value,
            "budget": {"mode": "fixed iterations; runner generation timeout 300 seconds", "runner_generation_seconds": 300},
        },
    }
