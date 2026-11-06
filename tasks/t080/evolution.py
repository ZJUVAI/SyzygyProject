"""Multistart continuous optimization for T080, with exact rational selection."""
import os
import random
import time
from fractions import Fraction

import numpy as np

from tasks.t080.check import objective_fraction
from tasks.t080.init_program import run_code as initial


def _objective(x):
    # Normalization to unit mass removes the scale invariance.
    x = np.maximum(np.asarray(x, dtype=float), 0.0)
    mass = float(x.sum())
    if not np.isfinite(mass) or mass <= 1e-15:
        return -1e6
    x = x / mass
    b = np.convolve(x, x)
    return (2.0 * np.dot(b, b) + np.dot(b[:-1], b[1:])) / (3.0 * b.max())


def _rationalize(x):
    x = np.maximum(np.asarray(x, dtype=float), 0.0)
    if not np.isfinite(x).all() or x.sum() <= 1e-15:
        return None
    x /= x.sum()
    # Bounded denominators keep exact checking practical while preserving shape.
    return [Fraction(float(v)).limit_denominator(100000) for v in x]


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = np.random.default_rng(seed)
    py_rng = random.Random(seed)
    try:
        budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    except ValueError:
        budget = 45.0
    deadline = time.monotonic() + budget

    # Retain the valid cold start as a guaranteed fallback.
    best = [Fraction(int(v)) for v in initial()["coefficients"]]
    best_value, _ = objective_fraction(best)
    try:
        from scipy.optimize import minimize
    except ImportError:
        return {"coefficients": [str(v) for v in best]}

    starts = []
    # Broad Dirichlet starts plus smooth and sparse profiles probe distinct basins.
    for _ in range(64):
        if time.monotonic() >= deadline:
            break
        mode = py_rng.randrange(4)
        if mode == 0:
            x = rng.dirichlet(np.full(20, rng.uniform(0.25, 3.0)))
        elif mode == 1:
            center = rng.uniform(0, 19)
            width = rng.uniform(1.0, 8.0)
            x = np.exp(-0.5 * ((np.arange(20) - center) / width) ** 2)
            x += rng.uniform(0.001, 0.08, 20)
            x /= x.sum()
        elif mode == 2:
            x = rng.random(20) ** rng.uniform(1.0, 8.0)
            x /= x.sum()
        else:
            x = np.ones(20) + rng.normal(0, 0.3, 20)
            x = np.maximum(x, 0.01)
            x /= x.sum()
        starts.append(x)

    # Optimize several diverse starts with simplex constraints and analytic-free
    # SLSQP derivatives. The max-convolution term is nonsmooth, so retain every
    # exactly checked rationalized incumbent.
    for x0 in starts:
        if time.monotonic() >= deadline:
            break
        try:
            def stop_if_expired(_x):
                if time.monotonic() >= deadline:
                    raise TimeoutError

            result = minimize(lambda x: -_objective(x), x0, method="SLSQP",
                              bounds=[(0.0, 1.0)] * 20,
                              constraints={"type": "eq", "fun": lambda x: x.sum() - 1.0},
                              callback=stop_if_expired,
                              options={"maxiter": 250, "ftol": 1e-11,
                                       "disp": False})
            candidate = _rationalize(result.x)
            if candidate is None:
                continue
            value, _ = objective_fraction(candidate)
            if value > best_value:
                best, best_value = candidate, value
        except (ValueError, FloatingPointError, OverflowError):
            continue
        except TimeoutError:
            break
    return {"coefficients": [str(v) for v in best]}
