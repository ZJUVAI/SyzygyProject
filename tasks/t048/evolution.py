"""Seeded comparator mutations from the simple initial network."""

import os
import random
import time

from tasks.t048.check import _CONFIGS, validate
from tasks.t048.init_program import run_code as initial_network


def _random_pair(rng, inputs):
    left = rng.randrange(inputs)
    right = rng.randrange(inputs - 1)
    if right >= left:
        right += 1
    return min(left, right), max(left, right)


def run_code():
    cid=os.environ.get("MATHBENCH_CONFIG_ID","T048-C01")
    if cid not in _CONFIGS:raise ValueError(f"unsupported T048 configuration: {cid}")
    inputs=_CONFIGS[cid];params={"inputs":inputs}
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    steps = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "256"))))
    from mathbench.search import search_deadline

    start = time.monotonic()
    deadline = search_deadline()
    initial = [tuple(pair) for pair in initial_network()["comparators"]]
    current = initial[:]
    best = current[:]
    rng = random.Random(seed ^ 0x71017)
    accepted = 0
    best_improvements = 0
    iterations_run = 0
    for _ in range(steps):
        if time.monotonic() >= deadline or not current:
            break
        proposal = current[:]
        move = rng.randrange(3)
        if move == 0 and len(proposal) > 1:
            del proposal[rng.randrange(len(proposal))]
        elif move == 1:
            index = rng.randrange(len(proposal))
            proposal[index] = _random_pair(rng, inputs)
        else:
            left = rng.randrange(len(proposal))
            right = rng.randrange(len(proposal))
            proposal[left], proposal[right] = proposal[right], proposal[left]
        try:
            validate({"comparators": proposal}, {"id":cid,"parameters":params})
        except ValueError:
            iterations_run += 1
            continue
        current = proposal
        accepted += 1
        if len(current) < len(best):
            best = current[:]
            best_improvements += 1
        iterations_run += 1
    final = validate({"comparators": best}, {"id":cid,"parameters":params})
    return {
        "comparators": [list(pair) for pair in best],
        "search_metadata": {
            "algorithm": "seeded deletion, replacement, and order-swap mutations from the self-contained odd-even transposition seed; every candidate exact-checked",
            "seed": seed,
            "initial_size": len(initial),
            "iterations_requested": steps,
            "iterations_run": iterations_run,
            "accepted_mutations": accepted,
            "best_improvements": best_improvements,
            "objective_recomputed": final["objective"],
            "generation_seconds": time.monotonic() - start,
            "budget": {"runner_generation_seconds": 300,
                       "runner_verification_seconds": 60},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
