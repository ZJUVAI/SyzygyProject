"""Bounded continuous search for the 208-term nonnegative convolution problem."""
import os
import random
import time
import json
from fractions import Fraction

import numpy as np

from mathbench.search import linear_polish as _linear_polish
from tasks.t014.check import validate
from tasks.t014.init_program import run_code as initial


_N = 208
_GRID = 10**10
_CONFIG = {"parameters": {"steps": 208, "support": ["-1/4", "1/4"],
                          "nonnegative": True}}


def _convolution(x):
    return np.convolve(x, x)


def _rationalize(x):
    x = np.asarray(x, dtype=float)
    if not np.isfinite(x).all():
        return None
    x = np.maximum(x, 0.0)
    mass = float(x.sum())
    if mass <= 1e-15:
        return None
    x /= mass
    # One shared integer grid gives every coefficient the same exact denominator.
    numerators = np.rint(x * _GRID).astype(np.int64)
    numerators = np.maximum(numerators, 0)
    total = int(numerators.sum())
    if total == 0:
        return None
    return [Fraction(int(v), total) for v in numerators]


def _exact_value(values):
    result = validate({"coefficients": [str(v) for v in values]}, _CONFIG)
    return Fraction(result["objective"])



def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = np.random.default_rng(seed)
    py_rng = random.Random(seed)
    try:
        budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    except ValueError:
        budget = 45.0
    deadline = time.monotonic() + budget

    best = [Fraction(int(v)) for v in initial()["coefficients"]]
    best_value = _exact_value(best)
    best_numeric = float(best_value)

    # The runner copies this task's saved best witness into an isolated warm
    # start file. Validate it with the exact task checker before using it.
    warm_start = os.environ.get("MATHBENCH_WARM_START")
    if warm_start:
        try:
            with open(warm_start, encoding="utf-8") as stream:
                supplied = json.load(stream)
            values = [Fraction(value) for value in supplied["coefficients"]]
            value = _exact_value(values)
            if value < best_value:
                best, best_value = values, value
                best_numeric = float(value)
        except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError):
            pass
    try:
        from scipy.optimize import minimize
    except ImportError:
        return {"coefficients": [str(v) for v in best]}

    # Repeated trust-region linear programs allow many independent basin probes.
    # Exact rational checks select every archived improvement.
    restarts = 0
    while time.monotonic() < deadline:
        incumbent = np.asarray([float(v) for v in best], dtype=float)
        incumbent /= incumbent.sum()
        if restarts == 0:
            x = incumbent.copy()
        elif restarts % 6 < 5:
            scale = (.003, .015, .06, .2, .6)[(restarts-1)%5]
            x = incumbent*np.exp(rng.normal(0, scale, _N))
            # Additive mass can reactivate zero coefficients.
            if restarts % 3 == 0:
                x += rng.exponential(scale/(10*_N), _N)
            x /= x.sum()
        else:
            x = rng.dirichlet(np.full(_N, rng.uniform(.3,2)))
        restarts += 1
        x = _linear_polish(x, min(deadline,time.monotonic()+18.0))
        candidate = _rationalize(x)
        if candidate is not None:
            value = _exact_value(candidate)
            if value < best_value:
                best, best_value = candidate, value
    return {"coefficients": [str(v) for v in best], "search_metadata": {
        "restarts":restarts,"budget_seconds":budget,"method":"multiscale simplex perturbation with trust-region linear-program descent"}}
