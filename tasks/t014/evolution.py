"""Bounded SLSQP restarts for Heilbronn triangle configurations.

Each restart fixes the orientation of every triple at its random initial point,
then maximizes the smallest oriented double area. The exact task checker is
used to score every retained candidate after decimal serialization.
"""
from fractions import Fraction
from itertools import combinations
import os
import random
import time

import numpy as np
from scipy.optimize import minimize

from tasks.t014.check import validate


_CONFIG_N = {"T014-C01": 11, "T014-C02": 12, "T014-C03": 16}


class _DeadlineReached(Exception):
    pass


def _exact_score(points):
    return Fraction(validate({"points": points}, {"parameters": {"n": len(points)}})["objective"])


def _serialize(z, n):
    return [[format(float(z[2 * i]), ".16g"), format(float(z[2 * i + 1]), ".16g")]
            for i in range(n)]


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T014-C01")
    n = _CONFIG_N.get(config_id, _CONFIG_N["T014-C01"])
    seconds = max(0.1, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = np.random.default_rng(seed)
    deadline = time.monotonic() + seconds
    triples = np.asarray(list(combinations(range(n), 3)), dtype=np.intp)
    best_points = None
    best_score = Fraction(-1)

    def consider(z):
        nonlocal best_points, best_score
        points = _serialize(z, n)
        try:
            score = _exact_score(points)
        except (ValueError, TypeError, ZeroDivisionError):
            return
        if score > best_score:
            best_score, best_points = score, points

    # Restart with an independent uniform point set; preserve its orientation
    # class so that absolute areas become smooth signed constraints.
    while time.monotonic() < deadline:
        xy = rng.uniform(0.0, 1.0, size=(n, 2))
        a, b, c = xy[triples[:, 0]], xy[triples[:, 1]], xy[triples[:, 2]]
        orient = np.sign((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) -
                         (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))
        # Random continuous points are distinct and noncollinear with probability 1.
        orient[orient == 0] = 1.0
        consider(xy.ravel())

        def signed_areas(v):
            if time.monotonic() >= deadline:
                raise _DeadlineReached
            p = v[:2 * n].reshape((n, 2))
            aa, bb, cc = p[triples[:, 0]], p[triples[:, 1]], p[triples[:, 2]]
            det = (bb[:, 0] - aa[:, 0]) * (cc[:, 1] - aa[:, 1]) - (bb[:, 1] - aa[:, 1]) * (cc[:, 0] - aa[:, 0])
            return orient * det - v[-1]

        def callback(v):
            consider(v[:2 * n])
            if time.monotonic() >= deadline:
                raise _DeadlineReached

        x0 = np.concatenate((xy.ravel(), [0.0]))
        bounds = [(0.0, 1.0)] * (2 * n) + [(0.0, 1.0)]
        try:
            result = minimize(lambda v: -v[-1], x0, method="SLSQP", bounds=bounds,
                              constraints=[{"type": "ineq", "fun": signed_areas}],
                              callback=callback,
                              options={"maxiter": 350, "ftol": 1e-10, "disp": False})
            consider(result.x[:2 * n])
        except _DeadlineReached:
            break

    # The random initial candidate is always valid; exact validation is repeated
    # immediately before return to guarantee checker-compatible output.
    if best_points is None:
        best_points = _serialize(rng.uniform(0.0, 1.0, size=(n, 2)).ravel(), n)
    validate({"points": best_points}, {"parameters": {"n": n}})
    return {"points": best_points}
