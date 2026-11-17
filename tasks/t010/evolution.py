"""Evolution-style search over symmetries and clean rectangular cuts."""

from __future__ import annotations

import os

import random

from tasks.t010.construction import _trim_candidates, _whole_board_transform
from tasks.t010.init_program import run_code as initial_solution


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T010-C01") != "T010-C01":
        raise ValueError("unknown T010 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    initial = initial_solution()
    population = [initial]
    best = initial
    best_count = len(initial["placements"])
    # Twelve generations mutate D4 orientation genes and tile-aligned crop cuts.
    for _ in range(12):
        parent = rng.choice(population)
        child = _whole_board_transform(parent, rng.randrange(8))
        children = [child, *_trim_candidates(child, rng)]
        child = min(children, key=lambda item: len(item["placements"]))
        count = len(child["placements"])
        population.append(child)
        population.sort(key=lambda item: len(item["placements"]))
        population = population[:4]
        if count < best_count:
            best, best_count = child, count
    return best
