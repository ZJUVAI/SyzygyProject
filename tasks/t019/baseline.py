"""Fixed-seed greedy point-set search. It does not read comparison assets."""

import random
import os

from tasks.t019.check import validate
from tasks.t019.init_program import run_code as initial_solution


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T019-C01")
    if config_id != "T019-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    best = initial_solution()
    best_score = 6
    for _ in range(250):
        x = rng.randint(-1000, 1000)
        y = rng.randint(-1000, 1000)
        candidate = {"points": best["points"] + [[x, y]], "claimed_objective": -999}
        try:
            result = validate(candidate, {"forbidden_convex_polygon_vertices": 7})
        except ValueError:
            continue
        if result["objective"] > best_score:
            best, best_score = candidate, result["objective"]
    return best
