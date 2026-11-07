"""Fixed-seed numerical search. It does not read the human or reference witness."""
import json
import math
import os
import random

import numpy as np
from scipy.spatial import ConvexHull

from mathbench.search import search_steps
from tasks.t040.init_program import configured_size


def _xyz(pair):
    u, v = pair
    d = 1.0 + u*u + v*v
    return (2*u/d, 2*v/d, (1-u*u-v*v)/d)


def _volume(parameters):
    points = np.asarray([_xyz(p) for p in parameters], dtype=float)
    return float(ConvexHull(points).volume)


def _seed_points(n):
    params = []
    golden = math.pi * (3.0 - math.sqrt(5.0))
    for k in range(n):
        z = 1.0 - 2.0 * (k + 0.5) / n
        radius = math.sqrt(1.0 - z*z)
        theta = k * golden
        x, y = radius * math.cos(theta), radius * math.sin(theta)
        params.append([x/(1.0+z), y/(1.0+z)])
    return params


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    requested = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    n = configured_size()
    current = _seed_points(n)
    current_score = _volume(current)
    best, best_score = [p[:] for p in current], current_score
    rng = random.Random(seed)
    actual = 0
    for step in search_steps(400):
        actual += 1
        temp = 0.12 * (1.0 - step/500.0)
        trial = [p[:] for p in current]
        index = rng.randrange(n)
        trial[index][0] += rng.gauss(0.0, temp)
        trial[index][1] += rng.gauss(0.0, temp)
        score = _volume(trial)
        if score > best_score:
            best, best_score = [p[:] for p in trial], score
        if score >= current_score or rng.random() < math.exp(min(0.0, (score-current_score)/max(temp, 1e-9))):
            current, current_score = trial, score
    return {
        "stereographic": best,
        "search_metadata": {
            "algorithm": "single-coordinate Gaussian perturbation with simulated-annealing acceptance and incumbent retention",
            "seed": seed,
            "actual_iterations": actual,
            "iteration_budget": 400,
            "requested_seconds": float(requested) if requested is not None else None,
            "feedback_objective": best_score,
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_code()))
