"""Fixed-step comparator deletion search from the simple initial network."""

import os
import random
import time

from tasks.t048.check import _CONFIGS, validate
from tasks.t048.init_program import run_code as initial_network


def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T048-C01")
    if cid not in _CONFIGS:raise ValueError(f"unsupported T048 configuration: {cid}")
    params={"inputs":_CONFIGS[cid]}
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "64"))))
    from mathbench.search import search_steps

    started = time.monotonic()
    best = [tuple(pair) for pair in initial_network()["comparators"]]
    initial_size = len(best)
    rng = random.Random(seed)
    accepted_removals = 0
    iterations_run = 0
    for _ in search_steps(iterations):
        if not best:
            break
        index = rng.randrange(len(best))
        candidate = best[:index] + best[index + 1:]
        try:
            validate({"comparators": candidate}, {"id":cid,"parameters":params})
        except ValueError:
            pass
        else:
            if len(candidate) < len(best):
                best = candidate
                accepted_removals += 1
        iterations_run += 1
    checked = validate({"comparators": best}, {"id":cid,"parameters":params})
    return {
        "comparators": [list(pair) for pair in best],
        "search_metadata": {
            "algorithm": "seeded greedy comparator deletion from the self-contained odd-even transposition seed",
            "seed": seed,
            "initial_size": initial_size,
            "iterations_requested": iterations,
            "iterations_run": iterations_run,
            "accepted_removals": accepted_removals,
            "objective_recomputed": checked["objective"],
            "generation_seconds": time.monotonic() - started,
            "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set",
                       "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
