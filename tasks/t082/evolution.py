"""Multistart SLSQP search for the 51-bin minimum-overlap problem.

The search starts from the supplied flat construction and random feasible
profiles. It uses the exact checker only after rational serialization; no
record or human witness files are read.
"""
from fractions import Fraction
import os
import time

import numpy as np
from scipy.optimize import minimize

from tasks.t082.check import objective_fraction, validate
from tasks.t082.init_program import run_code as initial_program


N = 51
MASS = 25.5
GRID = 1_000_000_000


def _lag_data():
    """Return pair indices and the exact floating objective scale per lag."""
    data = []
    for lag in range(-(N - 1), N):
        first = []
        second = []
        for i in range(N):
            j = i + lag
            if 0 <= j < N:
                first.append(i)
                second.append(j)
        data.append((np.asarray(first), np.asarray(second)))
    return data


LAGS = _lag_data()
SCALE = 2.0 / N


def _profile_and_jac(h):
    values = np.empty(len(LAGS), dtype=float)
    jac = np.zeros((len(LAGS), N), dtype=float)
    for k, (ii, jj) in enumerate(LAGS):
        values[k] = SCALE * np.sum(h[ii] * (1.0 - h[jj]))
        np.add.at(jac[k], ii, SCALE * (1.0 - h[jj]))
        np.add.at(jac[k], jj, -SCALE * h[ii])
    return values, jac


def _project_mass(values):
    """Euclidean projection onto [0,1]^51 with sum 25.5."""
    lo, hi = float(np.min(values) - 1.0), float(np.max(values))
    for _ in range(70):
        mid = (lo + hi) / 2.0
        total = float(np.clip(values - mid, 0.0, 1.0).sum())
        if total > MASS:
            lo = mid
        else:
            hi = mid
    return np.clip(values - (lo + hi) / 2.0, 0.0, 1.0)


def _rational_repair(h):
    """Quantize to billionths and repair the sum to exactly 25.5."""
    bounded = np.clip(np.asarray(h, dtype=float), 0.0, 1.0)
    scaled = bounded * GRID
    units = np.floor(scaled).astype(np.int64)
    target = int(MASS * GRID)
    residual = target - int(units.sum())
    fractions = scaled - units
    if residual > 0:
        order = np.argsort(-fractions)
        while residual:
            progressed = False
            for i in order:
                add = min(residual, GRID - int(units[i]))
                if add:
                    units[i] += add
                    residual -= add
                    progressed = True
                    if not residual:
                        break
            if not progressed:
                raise ValueError("cannot repair mass within height bounds")
    elif residual < 0:
        order = np.argsort(fractions)
        residual = -residual
        while residual:
            progressed = False
            for i in order:
                take = min(residual, int(units[i]))
                if take:
                    units[i] -= take
                    residual -= take
                    progressed = True
                    if not residual:
                        break
            if not progressed:
                raise ValueError("cannot repair mass within height bounds")
    return [str(Fraction(int(v), GRID)) for v in units]


class _DeadlineReached(Exception):
    pass


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = np.random.default_rng(seed)
    try:
        seconds = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    except ValueError:
        seconds = 45.0
    deadline = time.monotonic() + seconds

    best_heights = _rational_repair(initial_program()["heights"])
    best_value = objective_fraction([Fraction(x) for x in best_heights])[0]
    best_float = float(best_value)

    def consider(h):
        nonlocal best_heights, best_value, best_float
        candidate = _rational_repair(h)
        value = objective_fraction([Fraction(x) for x in candidate])[0]
        if value < best_value:
            best_heights, best_value = candidate, value
            best_float = float(value)

    def values(z):
        if time.monotonic() >= deadline:
            raise _DeadlineReached
        return _profile_and_jac(z[:-1])

    def inequalities(z):
        prof, _ = values(z)
        return z[-1] - prof

    def inequalities_jac(z):
        _, grad = values(z)
        out = np.empty((len(LAGS), N + 1), dtype=float)
        out[:, :N] = -grad
        out[:, N] = 1.0
        return out

    equality = {"type": "eq", "fun": lambda z: np.sum(z[:N]) - MASS,
                "jac": lambda z: np.r_[np.ones(N), 0.0]}
    ineq = {"type": "ineq", "fun": inequalities, "jac": inequalities_jac}

    # One flat start plus independently sampled feasible profiles. Each SLSQP
    # run minimizes the epigraph variable t subject to t >= every lag value.
    restart = 0
    while time.monotonic() < deadline:
        if restart == 0:
            h0 = np.full(N, 0.5)
        else:
            raw = rng.uniform(0.0, 1.0, size=N)
            if restart % 3 == 0:
                raw = 0.5 + rng.normal(0.0, 0.22, size=N)
            h0 = _project_mass(raw)
        restart += 1
        consider(h0)
        p0, _ = _profile_and_jac(h0)
        z0 = np.r_[h0, float(np.max(p0)) + 1e-10]

        def callback(z):
            # Preserve useful progress even when the deadline interrupts this
            # local solve. The exact checker is only called for likely gains.
            profile, _ = _profile_and_jac(z[:N])
            if float(np.max(profile)) < best_float - 1e-12:
                consider(z[:N])
            if time.monotonic() >= deadline:
                raise _DeadlineReached

        try:
            result = minimize(lambda z: z[-1], z0,
                              jac=lambda z: np.r_[np.zeros(N), 1.0],
                              method="SLSQP", bounds=[(0.0, 1.0)] * N + [(0.0, 1.0)],
                              constraints=[equality, ineq], callback=callback,
                              options={"maxiter": 180, "ftol": 1e-10, "disp": False})
            if np.all(np.isfinite(result.x[:N])):
                consider(result.x[:N])
        except _DeadlineReached:
            break

    # Repeat the exact full-domain check immediately before returning.
    validate({"heights": best_heights}, {"parameters": {
        "steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1
    }})
    return {"heights": best_heights}
