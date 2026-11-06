"""Bounded continuous search for the 208-term nonnegative convolution problem."""
import os
import random
import time
from fractions import Fraction

import numpy as np

from tasks.t079.check import validate
from tasks.t079.init_program import run_code as initial


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
    try:
        from scipy.optimize import minimize
    except ImportError:
        return {"coefficients": [str(v) for v in best]}

    # Epigraph formulation: minimize t subject to every convolution term <= t.
    # Its analytic Jacobian avoids finite-difference work over 208 variables.
    def objective(z):
        return 416.0 * z[-1]

    def objective_jac(z):
        g = np.zeros(_N + 1)
        g[-1] = 416.0
        return g

    def equality(z):
        return np.array([z[:_N].sum() - 1.0])

    def equality_jac(z):
        g = np.zeros((_N + 1,))
        g[:_N] = 1.0
        return g.reshape(1, -1)

    def inequalities(z):
        return z[-1] - _convolution(z[:_N])

    def inequalities_jac(z):
        x = z[:_N]
        conv = np.zeros((2 * _N - 1, _N + 1))
        # d(x*x)[k]/dx[j] = 2*x[k-j], including the valid index range.
        for k in range(2 * _N - 1):
            lo, hi = max(0, k - (_N - 1)), min(_N - 1, k)
            js = np.arange(lo, hi + 1)
            conv[k, js] = 2.0 * x[k - js]
        conv[:, -1] = -1.0
        return -conv

    # Uniform is a strong, deterministic basin seed. Random positive profiles
    # explore other shapes; all starts remain on the unit simplex.
    starts = [np.full(_N, 1.0 / _N)]
    for _ in range(20):
        if time.monotonic() >= deadline:
            break
        mode = py_rng.randrange(3)
        if mode == 0:
            x = rng.dirichlet(np.full(_N, rng.uniform(0.2, 2.0)))
        elif mode == 1:
            grid = np.arange(_N, dtype=float)
            center = rng.uniform(0, _N - 1)
            width = rng.uniform(12.0, 100.0)
            x = np.exp(-0.5 * ((grid - center) / width) ** 2)
            x += rng.uniform(0.001, 0.03, _N)
            x /= x.sum()
        else:
            x = rng.random(_N) ** rng.uniform(0.5, 4.0)
            x /= x.sum()
        starts.append(x)

    for x0 in starts:
        if time.monotonic() >= deadline:
            break
        conv = _convolution(x0)
        z0 = np.r_[x0, float(conv.max()) + 1e-10]

        def retain(z):
            nonlocal best, best_value, best_numeric
            candidate = _rationalize(z[:_N])
            if candidate is None:
                return
            numeric = 416.0 * float(_convolution(np.asarray(
                [float(v) for v in candidate])).max())
            if numeric >= best_numeric:
                return
            value = _exact_value(candidate)
            if value < best_value:
                best, best_value = candidate, value
                best_numeric = float(value)

        def stop_if_expired(z):
            retain(z)
            if time.monotonic() >= deadline:
                raise TimeoutError

        try:
            result = minimize(
                objective, z0, jac=objective_jac, method="SLSQP",
                bounds=[(0.0, 1.0)] * _N + [(0.0, 1.0)],
                constraints=[
                    {"type": "eq", "fun": equality, "jac": equality_jac},
                    {"type": "ineq", "fun": inequalities, "jac": inequalities_jac},
                ], callback=stop_if_expired,
                options={"maxiter": 180, "ftol": 1e-12, "disp": False})
            retain(result.x)
        except TimeoutError:
            break
        except (ValueError, FloatingPointError, OverflowError, ZeroDivisionError):
            continue

    return {"coefficients": [str(v) for v in best]}
