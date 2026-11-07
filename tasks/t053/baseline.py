"""Greedy prime transfers from the simple 1*2*...*N initial factorization."""

import os
import random
import time

from tasks.t053.check import PARAMETERS, validate
from tasks.t053.init_program import N, run_code as initial_run


def _spf(limit):
    result = [0] * (limit + 1)
    primes = []
    for value in range(2, limit + 1):
        if result[value] == 0:
            result[value] = value
            primes.append(value)
        for prime in primes:
            multiple = value * prime
            if multiple > limit or prime > result[value]:
                break
            result[multiple] = prime
    return result


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T053-C01") != "T053-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    iterations = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "64"))))
    from mathbench.search import search_steps

    start = time.monotonic()
    factors = list(initial_run()["factors"])
    spf = _spf(N)
    rng = random.Random(seed)
    accepted = 0
    iterations_run = 0
    for _ in search_steps(iterations):
        floor_value = min(factors)
        receiver = next(i for i, value in enumerate(factors) if value == floor_value)
        for _attempt in range(256):
            donor = rng.randrange(1, N)
            if donor == receiver:
                continue
            value = factors[donor]
            if value <= 1 or value > N:
                continue
            prime = spf[value]
            remainder = value // prime
            if remainder < floor_value:
                continue
            factors[receiver] *= prime
            factors[donor] = remainder
            accepted += 1
            break
        iterations_run += 1
    checked = validate({"factors": factors}, {"parameters": PARAMETERS})
    return {
        "factors": factors,
        "search_metadata": {
            "algorithm": "seeded greedy transfer of one prime from a donor factor to a smallest factor; exact product preserved by each transfer",
            "seed": seed,
            "initial_objective": 1,
            "iterations_requested": iterations,
            "iterations_run": iterations_run,
            "accepted_transfers": accepted,
            "objective_recomputed": checked["objective"],
            "generation_seconds": time.monotonic() - start,
            "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set",
                       "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
