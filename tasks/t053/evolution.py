"""Seeded prime-transfer mutations from the simple initial factorization."""

import os
import random
import time

from tasks.t053.baseline import _spf
from tasks.t053.check import PARAMETERS, validate
from tasks.t053.init_program import N, run_code as initial_run


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T053-C01") != "T053-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    steps = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "256"))))
    from mathbench.search import search_deadline

    start = time.monotonic()
    deadline = search_deadline()
    current = list(initial_run()["factors"])
    best = current[:]
    spf = _spf(N)
    rng = random.Random(seed ^ 0x100100)
    accepted = 0
    best_improvements = 0
    iterations_run = 0
    for _ in range(steps):
        if time.monotonic() >= deadline:
            break
        floor_value = min(current)
        receivers = [i for i, value in enumerate(current) if value == floor_value]
        receiver = rng.choice(receivers)
        moved = False
        for _attempt in range(64):
            donor = rng.randrange(N)
            if donor == receiver:
                continue
            value = current[donor]
            if value <= 1 or value > N:
                continue
            prime = spf[value]
            remainder = value // prime
            if remainder < floor_value:
                continue
            current[receiver] *= prime
            current[donor] = remainder
            accepted += 1
            moved = True
            break
        if moved:
            objective = min(current)
            if objective > min(best):
                best = current[:]
                best_improvements += 1
        iterations_run += 1
    checked = validate({"factors": best}, {"parameters": PARAMETERS})
    return {
        "factors": best,
        "search_metadata": {
            "algorithm": "seeded random receiver selection with prime-factor transfers from the initial 1..N factorization; product is preserved exactly",
            "seed": seed,
            "initial_objective": 1,
            "iterations_requested": steps,
            "iterations_run": iterations_run,
            "accepted_transfers": accepted,
            "best_improvements": best_improvements,
            "objective_recomputed": checked["objective"],
            "generation_seconds": time.monotonic() - start,
            "budget": {"runner_generation_seconds": 300,
                       "runner_verification_seconds": 60},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
