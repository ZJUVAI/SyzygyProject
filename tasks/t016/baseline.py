from mathbench.search import search_deadline, search_steps
"""Seeded signed-coordinate search; it does not read the human witness."""
import os
import random
import time
import numpy as np
from tasks.t016.init_program import run_code as initial


def _score(a):
    mass = float(np.sum(a))
    if not np.isfinite(mass) or abs(mass) < 1e-12:
        return float("inf")
    conv = np.convolve(a, a)
    return 416.0 * float(np.max(np.abs(conv))) / (mass * mass)


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T016-C01")
    if config_id != "T016-C01":
        raise ValueError("unsupported configuration: " + config_id)
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    best = np.asarray(initial()["coefficients"], dtype=np.float64)
    score = _score(best)
    deadline = search_deadline()
    scale = 0.1
    for _attempt in search_steps(100):
        cand = best.copy()
        i, j = rng.sample(range(208), 2)
        delta = rng.gauss(0.0, scale)
        cand[i] += delta
        cand[j] -= delta  # preserve the mass, hence the integral
        value = _score(cand)
        if value < score:
            best, score = cand, value
            scale = min(0.5, scale * 1.01)
        else:
            scale = max(1e-4, scale * 0.999)
    return {"coefficients": [float(x) for x in best]}
