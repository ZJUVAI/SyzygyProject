"""Task-qualified evolution entry point with bounded local direction search."""

import os
import random

from tasks.t037.init_program import run_code as initial


def _compatible(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot <= 0 or 4 * dot * dot <= sum(x*x for x in a) * sum(y*y for y in b)


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T037-C01") != "T037-C01":
        raise ValueError("unknown T037 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    steps = max(1, int(os.environ.get("MATHBENCH_SEARCH_STEPS", "200")))
    rng = random.Random(seed)
    dirs = [list(map(int, v)) for v in initial()["directions"]]
    # Explore small integer perturbations, retaining only exactly feasible additions.
    accepted = 0
    for _ in range(steps):
        v = [rng.randint(-2, 2) for _ in range(5)]
        if not any(v):
            continue
        first = next(x for x in v if x)
        if first < 0:
            v = [-x for x in v]
        if all(_compatible(v, q) for q in dirs):
            dirs.append(v)
            accepted += 1
    return {"directions": dirs, "search_metadata": {
        "algorithm": "seeded random integer-direction greedy additions",
        "seed": seed, "iterations": steps, "accepted_additions": accepted,
        "coordinate_range": [-2, 2],
        "budget": "fixed iteration count; shared runner hard limit applies"}}
