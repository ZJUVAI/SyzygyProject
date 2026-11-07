"""Seeded population search using endpoint truncation and greedy regrowth."""

import os
import random
import time

from tasks.t050.baseline import _extend
from tasks.t050.init_program import configured_dimension


def run_code():
    dimension = configured_dimension()
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    generations = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "96"))))
    from mathbench.search import search_steps

    rng = random.Random(seed ^ 0x11009)
    population = [_extend(rng, rng.randrange(1 << dimension), dimension=dimension) for _ in range(8)]
    best = max(population, key=len)
    start_time = time.monotonic()
    generations_run = 0
    for generation in search_steps(generations):
        generations_run += 1
        parent = max(population, key=lambda path: len(path) + rng.random() * 2)
        keep = max(1, len(parent) - rng.randint(0, min(24, len(parent) - 1)))
        prefix = parent[:keep]
        # Rebuild from a retained prefix, accepting only legal extensions.
        candidate = prefix[:]
        occupied = set(candidate)
        while True:
            moves = list(range(dimension))
            rng.shuffle(moves)
            legal = [candidate[-1] ^ (1 << bit) for bit in moves
                     if (candidate[-1] ^ (1 << bit)) not in occupied
                     and not any(((candidate[-1] ^ (1 << bit)) ^ old).bit_count() == 1 for old in candidate[:-1])]
            if not legal:
                break
            nxt = rng.choice(legal)
            candidate.append(nxt)
            occupied.add(nxt)
        population[generation % len(population)] = candidate
        if len(candidate) > len(best):
            best = candidate
    return {
        "vertices": best,
        "search_metadata": {
            "algorithm": "seeded population endpoint truncation and greedy regrowth",
            "seed": seed,
            "iterations_requested": generations,
            "iterations_run": generations_run,
            "objective_recomputed": len(best) - 1,
            "generation_seconds": time.monotonic() - start_time,
            "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set", "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
