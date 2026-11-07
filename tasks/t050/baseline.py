"""Seeded randomized greedy endpoint extension with bounded restarts."""

import os
import random
import time

from tasks.t050.init_program import configured_dimension


def _extend(rng, start, order=None, dimension=9):
    vertices = [start]
    occupied = {start}
    while True:
        coordinates = list(range(dimension)) if order is None else order[:]
        rng.shuffle(coordinates)
        legal = []
        for coordinate in coordinates:
            candidate = vertices[-1] ^ (1 << coordinate)
            if candidate in occupied:
                continue
            if any((candidate ^ old).bit_count() == 1 for old in vertices[:-1]):
                continue
            legal.append(candidate)
        if not legal:
            break
        candidate = rng.choice(legal)
        vertices.append(candidate)
        occupied.add(candidate)
    return vertices


def run_code():
    dimension = configured_dimension()
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    restarts = max(1, min(10000, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "48"))))
    from mathbench.search import search_steps

    rng = random.Random(seed)
    best = [0]
    start_time = time.monotonic()
    run_count = 0
    for attempt in search_steps(restarts):
        run_count += 1
        candidate = _extend(rng, rng.randrange(1 << dimension), dimension=dimension)
        if len(candidate) > len(best):
            best = candidate
    if len(best) == 1:
        best = _extend(random.Random(seed), 0, dimension=dimension)
    return {
        "vertices": best,
        "search_metadata": {
            "algorithm": "seeded randomized greedy extension with independent restarts",
            "seed": seed,
            "iterations_requested": restarts,
            "iterations_run": run_count,
            "objective_recomputed": len(best) - 1,
            "generation_seconds": time.monotonic() - start_time,
            "budget": {"mode": "fixed iterations unless MATHBENCH_SEARCH_SECONDS is set", "runner_generation_seconds": 300},
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
