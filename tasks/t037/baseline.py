"""Seeded greedy search over a bounded, generated rational direction pool."""

import itertools
import os
import random


def _compatible(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot <= 0 or 4 * dot * dot <= sum(x*x for x in a) * sum(y*y for y in b)


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T037-C01") != "T037-C01":
        raise ValueError("unknown T037 configuration")
    seed = 0
    rng = random.Random(seed)
    pool = [v for v in itertools.product((-1, 0, 1), repeat=5)
            if any(v) and next((x for x in v if x), 1) > 0]
    rng.shuffle(pool)
    selected = []
    for v in pool:
        if all(_compatible(v, q) for q in selected):
            selected.append(v)
    return {"directions": [list(v) for v in selected],
            "search_metadata": {"algorithm": "seeded greedy maximal subset",
                                "candidate_pool": "nonzero ternary vectors, first nonzero coordinate positive",
                                "seed": seed, "iterations": len(pool),
                                "accepted": len(selected),
                                "budget": "fixed finite candidate pool"}}
