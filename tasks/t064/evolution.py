"""Seeded search over exact grid triangulations; no comparison witness is read."""
import os
import random

from mathbench.search import search_steps
from tasks.t064.grid_method import build_grid

ITERATION_LIMIT = 20


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T064-C01") != "T064-C01":
        raise ValueError("unsupported T064 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    rng = random.Random(seed)
    best = None
    best_count = None
    patterns = []
    for _ in search_steps(ITERATION_LIMIT):
        pattern = rng.randrange(3)
        patterns.append(pattern)
        candidate = build_grid(pattern)
        count = len(candidate["steiner_points_x"])
        if best_count is None or count < best_count:
            best, best_count = candidate, count
    if best is None:
        from tasks.t064.init_program import run_code as init_run
        best = init_run()
        best_count = len(best["steiner_points_x"])
    best.pop("construction_metadata", None)
    best["search_metadata"] = {
        "algorithm": "seeded mixed-pattern Cartesian-grid enumeration",
        "seed": seed,
        "tested_patterns": patterns,
        "iterations": len(patterns),
        "iteration_limit": ITERATION_LIMIT,
        "best_steiner_points": best_count,
        "reference_data_read": False,
        "budget": {
            "mode": "wall_clock_cutoff" if seconds is not None else "fixed_iteration_count",
            "requested_iterations": ITERATION_LIMIT,
            "actual_iterations": len(patterns),
            "requested_wall_clock_seconds": seconds,
        },
    }
    return best
