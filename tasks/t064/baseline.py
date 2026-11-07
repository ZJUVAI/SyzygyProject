"""Fixed-seed search over traditional grid-diagonal patterns."""
import os
import random

from mathbench.search import search_steps
from tasks.t064.grid_method import build_grid

ITERATION_LIMIT = 3


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T064-C01") != "T064-C01":
        raise ValueError("unsupported T064 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    seconds = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    order = [0, 1, 2]
    random.Random(seed).shuffle(order)
    best = None
    best_count = None
    tested = []
    for index in search_steps(ITERATION_LIMIT):
        pattern = order[index]
        candidate = build_grid(pattern)
        count = len(candidate["steiner_points_x"])
        tested.append(pattern)
        if best_count is None or count < best_count:
            best, best_count = candidate, count
    if best is None:
        best = build_grid(0)
        best_count = len(best["steiner_points_x"])
    best["search_metadata"] = {
        "algorithm": "fixed-count comparison of Cartesian-grid diagonal patterns",
        "seed": seed,
        "tested_patterns": tested,
        "iterations": len(tested),
        "iteration_limit": ITERATION_LIMIT,
        "reference_data_read": False,
        "budget": {
            "mode": "wall_clock_cutoff" if seconds is not None else "fixed_iteration_count",
            "requested_iterations": ITERATION_LIMIT,
            "actual_iterations": len(tested),
            "requested_wall_clock_seconds": seconds,
        },
    }
    best.pop("construction_metadata", None)
    return best
