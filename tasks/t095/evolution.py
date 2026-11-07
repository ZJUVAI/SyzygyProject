"""Evolutionary search over greedy convex-merge policy weights."""

from __future__ import annotations

import os
import random

from tasks.t095.construction import greedy_merge
from tasks.t095.check import load_points

_CONFIG = {
    "id": "T095-C01",
    "parameters": {
        "instance": "uniform-0000500-1",
        "point_count": 500,
        "objective": "minimize number of internal convex faces",
    },
    "direction": "minimize",
}


def run_search(seed=0, steps=12):
    rng = random.Random(seed)
    points = load_points()
    policy = [1.0, 0.0, 0.0]
    incumbent = greedy_merge(points, seed=seed, weights=tuple(policy))
    best_score = len(incumbent["edges"]) - len(points) + 1
    step = 0.25
    for _ in range(steps):
        trial_policy = policy[:]
        k = rng.randrange(3)
        trial_policy[k] += rng.uniform(-step, step)
        candidate = greedy_merge(points, seed=rng.randrange(1 << 30),
                                 weights=tuple(trial_policy), shuffle_ties=True)
        score = len(candidate["edges"]) - len(points) + 1
        if score <= best_score or rng.random() < 0.05:
            policy = trial_policy
        if score < best_score:
            incumbent, best_score = candidate, score
        step *= 0.94
    return incumbent


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T095-C01") != "T095-C01":
        raise ValueError("unknown T095 configuration")
    return run_search(seed=int(os.environ.get("MATHBENCH_SEED", "0")), steps=12)
