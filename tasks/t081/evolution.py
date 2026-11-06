"""Cold-start multistart minimax search for the T081 signed AC3 task."""

import os
import random
import time
from fractions import Fraction

import numpy as np

from tasks.t081.init_program import run_code as initial
from tasks.t081.baseline import run_code as traditional_search


_N = 208
_SCORE_FACTOR = 416
_GRID = 10_000_000_000


def _exact_score(coefficients):
    """Score a rational candidate with the same exact rule as the evaluator."""
    # Candidates are all placed on _GRID, so integer convolution gives an exact
    # comparison without constructing thousands of large intermediate Fractions.
    numerators = [int(value * _GRID) for value in coefficients]
    mass = sum(numerators)
    if mass == 0:
        return Fraction(10**100)
    peak = 0
    for k in range(2 * _N - 1):
        lo = max(0, k - (_N - 1))
        hi = min(_N - 1, k)
        total = sum(numerators[i] * numerators[k - i] for i in range(lo, hi + 1))
        peak = max(peak, abs(total))
    return Fraction(_SCORE_FACTOR * peak, mass * mass)


def _rationalize(x):
    """Normalize and rationalize a finite numerical coefficient vector."""
    values = np.asarray(x, dtype=np.float64)
    mass = float(values.sum())
    if not np.isfinite(values).all() or not np.isfinite(mass) or abs(mass) < 1e-10:
        return None
    values = values / mass
    # Keep exact convolution checks practical while retaining useful precision.
    numerators = [int(round(float(v) * _GRID)) for v in values[:-1]]
    numerators.append(_GRID - sum(numerators))
    return [Fraction(v, _GRID) for v in numerators]


def _float_score(x):
    values = np.asarray(x, dtype=np.float64)
    mass = float(values.sum())
    if not np.isfinite(values).all() or abs(mass) < 1e-12:
        return float("inf")
    conv = np.convolve(values, values)
    return _SCORE_FACTOR * float(np.max(np.abs(conv))) / (mass * mass)


def _smooth_value_gradient(y, tau):
    """Log-sum-exp approximation to max(abs(a*a)); return value and gradient."""
    x = np.empty(_N, dtype=np.float64)
    x[:-1] = y
    x[-1] = 1.0 - float(np.sum(y))
    conv = np.convolve(x, x)

    scaled = np.concatenate((conv / tau, -conv / tau))
    peak = float(np.max(scaled))
    weights = np.exp(scaled - peak)
    weights /= float(weights.sum())
    signed_weights = weights[:len(conv)] - weights[len(conv):]

    # d/dx_j sum_k w_k sum_i x_i x_(k-i) = 2 sum_i x_i w_(i+j).
    full_gradient = 2.0 * np.correlate(signed_weights, x, mode="valid")
    # y_j moves x_j and x_(N-1) in opposite directions.
    gradient = full_gradient[:-1] - full_gradient[-1]
    smooth_max = tau * (peak + np.log(float(np.sum(np.exp(scaled - peak)))))
    return _SCORE_FACTOR * smooth_max, _SCORE_FACTOR * gradient


def _objective_and_gradient(y, tau):
    value, gradient = _smooth_value_gradient(y, tau)
    return value, gradient


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T081-C02") != "T081-C02":
        raise ValueError("unsupported configuration: T081-C02")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    try:
        budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    except (TypeError, ValueError):
        budget = 45.0
    deadline = time.monotonic() + budget
    rng = np.random.default_rng(seed)
    py_rng = random.Random(seed)

    # The unmodified initial construction is always the fallback incumbent.
    initial_values = _rationalize(initial()["coefficients"])
    if initial_values is None:
        raise ValueError("initial construction has invalid coefficient mass")
    best = initial_values
    best_score = _exact_score(best)
    best_float_score = _float_score([float(v) for v in best])

    # Seed the incumbent with the task's traditional search when it improves
    # the cold-start construction. This routine does not read witness assets.
    try:
        traditional = _rationalize(traditional_search()["coefficients"])
        if traditional is not None:
            traditional_score = _exact_score(traditional)
            if traditional_score < best_score:
                best, best_score = traditional, traditional_score
                best_float_score = _float_score([float(v) for v in best])
    except (ImportError, ValueError, FloatingPointError, OverflowError):
        pass

    try:
        from scipy.optimize import minimize
    except ImportError:
        return {"coefficients": [str(v) for v in best]}
    if time.monotonic() >= deadline:
        return {"coefficients": [str(v) for v in best]}

    initial_array = np.asarray([float(v) for v in initial_values], dtype=np.float64)
    initial_mass = float(initial_array.sum())
    if abs(initial_mass) < 1e-12:
        initial_array = np.full(_N, 1.0 / _N)
    else:
        initial_array /= initial_mass

    # Every variable vector represents unit mass, with the final coefficient
    # enforcing the affine constraint. Starts span positive and signed shapes.
    incumbent = np.asarray([float(v) for v in best], dtype=np.float64)
    incumbent /= float(incumbent.sum())
    temperatures = (0.001, 0.0002, 0.00005, 0.00001, 0.000002)
    restart = 0
    while time.monotonic() < deadline:
        restart += 1
        if restart == 1:
            x = initial_array.copy()
        elif restart % 5 == 0:
            # Explore near the best exactly checked basin.
            x = incumbent + rng.normal(0.0, rng.uniform(0.0005, 0.012), _N)
        elif restart % 4 == 0:
            # Randomly centered smooth positive profile.
            idx = np.arange(_N, dtype=np.float64)
            center = rng.uniform(0.0, _N - 1.0)
            width = rng.uniform(8.0, 80.0)
            x = np.exp(-0.5 * ((idx - center) / width) ** 2)
            x += rng.uniform(0.001, 0.05)
        elif restart % 4 == 1:
            x = rng.dirichlet(np.full(_N, rng.uniform(0.15, 4.0)))
        else:
            scale = rng.uniform(0.006, 0.10)
            perturbation = rng.normal(0.0, scale, _N)
            perturbation -= float(perturbation.mean())
            x = np.full(_N, 1.0 / _N) + perturbation
        mass = float(x.sum())
        if abs(mass) < 1e-12 or not np.isfinite(x).all():
            continue
        x /= mass
        start = x[:-1].copy()
        if time.monotonic() >= deadline:
            break
        y = start.copy()
        try:
            for tau in temperatures:
                if time.monotonic() >= deadline:
                    break

                def callback(_y):
                    nonlocal best, best_score, best_float_score
                    candidate_array = np.empty(_N, dtype=np.float64)
                    candidate_array[:-1] = _y
                    candidate_array[-1] = 1.0 - float(np.sum(_y))
                    value = _float_score(candidate_array)
                    if value < best_float_score:
                        candidate = _rationalize(candidate_array)
                        if candidate is not None:
                            exact_score = _exact_score(candidate)
                            if exact_score < best_score:
                                best, best_score = candidate, exact_score
                                best_float_score = value
                                incumbent = np.asarray([float(v) for v in best])
                    if time.monotonic() >= deadline:
                        raise TimeoutError

                result = minimize(
                    lambda z: _objective_and_gradient(z, tau), y,
                    method="L-BFGS-B", jac=True, callback=callback,
                    options={"maxiter": 500, "ftol": 1e-12, "gtol": 1e-7,
                             "maxls": 30, "maxcor": 16},
                )
                y = np.asarray(result.x, dtype=np.float64)
                if not np.isfinite(y).all():
                    break
                candidate_array = np.empty(_N, dtype=np.float64)
                candidate_array[:-1] = y
                candidate_array[-1] = 1.0 - float(y.sum())
                candidate = _rationalize(candidate_array)
                if candidate is not None:
                    exact_score = _exact_score(candidate)
                    if exact_score < best_score:
                        best, best_score = candidate, exact_score
                        best_float_score = _float_score([float(v) for v in candidate])
                        incumbent = np.asarray([float(v) for v in best])
        except TimeoutError:
            break
        except (FloatingPointError, OverflowError, ValueError):
            continue

    return {"coefficients": [str(v) for v in best]}
