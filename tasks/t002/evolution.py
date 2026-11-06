"""Cold-start evolutionary search for unit-square packing instances.

The search starts from a regular grid and makes bounded, exact-rational
coordinate and orientation proposals.  It retains only layouts accepted by
the task checker, so the returned construction is always feasible.
"""
import os
import random
import time
from fractions import Fraction

from tasks.t002.check import Q, validate


CONFIGS = {"T002-C01": 26, "T002-C03": 29, "T002-C04": 38}


def _seed(n):
    cols = 5 if n == 26 else (6 if n == 29 else 7)
    return {"squares": [
        {"x": str(Fraction(2 * (i % cols) + 1, 2)),
         "y": str(Fraction(2 * (i // cols) + 1, 2)), "t": "0"}
        for i in range(n)
    ]}


def _score(layout, config):
    return Q.parse(validate(layout, config)["objective"])


def _optimize(n, seconds, rng):
    """Joint smooth penalty optimization, followed by exact rational repair."""
    try:
        import numpy as np
        from scipy.optimize import minimize
    except ImportError:
        return None
    cols = 5 if n == 26 else (6 if n == 29 else 7)
    rows = (n + cols - 1) // cols
    xy = np.array([[(i % cols) + .5, (i // cols) + .5]
                   for i in range(n)], dtype=float)
    # Add small independent jitter so the optimizer can break grid symmetry.
    xy += np.array([[rng.uniform(-.025, .025), rng.uniform(-.025, .025)]
                    for _ in range(n)])
    z0 = np.concatenate((xy.ravel(), np.zeros(n), [float(max(cols, rows))]))
    deadline = time.monotonic() + seconds
    best = None
    best_value = float("inf")

    def loss(z):
        centers = z[:2*n].reshape((n, 2))
        angles = z[2*n:3*n]
        side = z[-1]
        c, s = np.cos(angles), np.sin(angles)
        # Half extents of each square along x and y.
        hx = .5 * (np.abs(c) + np.abs(s))
        hy = hx
        over = np.maximum(0., centers[:, 0] + hx - side/2) ** 2
        over += np.maximum(0., -side/2 - (centers[:, 0] - hx)) ** 2
        over += np.maximum(0., centers[:, 1] + hy - side/2) ** 2
        over += np.maximum(0., -side/2 - (centers[:, 1] - hy)) ** 2
        penalty = 250. * float(over.sum())
        dx = centers[:, 0, None] - centers[None, :, 0]
        dy = centers[:, 1, None] - centers[None, :, 1]
        da = angles[:, None] - angles[None, :]
        ca, sa = np.cos(angles), np.sin(angles)
        # SAT gaps projected on each square's two local axes.
        ext = .5 * (np.abs(np.cos(da)) + np.abs(np.sin(da)))
        gaps = [np.abs(dx*ca[:, None] + dy*sa[:, None]) - .5 - ext,
                np.abs(-dx*sa[:, None] + dy*ca[:, None]) - .5 - ext,
                np.abs(dx*ca[None, :] + dy*sa[None, :]) - .5 - ext,
                np.abs(-dx*sa[None, :] + dy*ca[None, :]) - .5 - ext]
        best_gap = np.maximum.reduce(gaps)
        tri = np.triu_indices(n, 1)
        overlap = np.maximum(0., -best_gap[tri])
        penalty += 250. * float(np.dot(overlap, overlap))
        return side + penalty

    # Keep optimization iterations bounded by the per-run deadline. Every
    # decoded candidate is checked exactly before it can become the archive.
    while time.monotonic() < deadline:
        result = minimize(loss, z0, method="L-BFGS-B",
                          bounds=[(None, None)] * (len(z0)-1) + [(4.5, 10.)],
                          options={"maxiter": 80, "ftol": 1.e-8})
        z = result.x
        centers = z[:2*n].reshape((n, 2))
        angles = z[2*n:3*n]
        # Rationalize the tan-half-angle and center coordinates. Expand the
        # centers about their mean until the exact checker certifies the pose.
        squares = []
        for (x, y), a in zip(centers, angles):
            t = Fraction(float(np.tan(a/2))).limit_denominator(100000)
            squares.append({"x": str(Fraction(float(x)).limit_denominator(100000)),
                            "y": str(Fraction(float(y)).limit_denominator(100000)),
                            "t": str(t)})
        cx = sum(float(Fraction(s["x"])) for s in squares)/n
        cy = sum(float(Fraction(s["y"])) for s in squares)/n
        for scale in (1.0, 1.0001, 1.001, 1.01, 1.03, 1.08, 1.16, 1.32):
            repaired = {"squares": []}
            for sq in squares:
                repaired["squares"].append({
                    "x": str(Fraction(float(cx + scale*(float(Fraction(sq["x"]))-cx))).limit_denominator(100000)),
                    "y": str(Fraction(float(cy + scale*(float(Fraction(sq["y"]))-cy))).limit_denominator(100000)),
                    "t": sq["t"]})
            try:
                qvalue = _score(repaired, {"parameters": {"n": n}})
                value = float(qvalue.a) + float(qvalue.b) * 2 ** .5
            except (ValueError, ZeroDivisionError):
                continue
            if value < best_value:
                best, best_value = repaired, value
            break
        if time.monotonic() >= deadline:
            break
        # Restart from the relaxed pose with fresh small perturbations.
        z0 = z.copy()
        z0[:2*n] += np.array([[rng.uniform(-.08, .08), rng.uniform(-.08, .08)]
                              for _ in range(n)]).ravel()
        z0[2*n:3*n] += np.array([rng.uniform(-.12, .12) for _ in range(n)])
    return best


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T002-C01")
    if cid not in CONFIGS:
        raise ValueError("unknown T002 configuration")
    n = CONFIGS[cid]
    conf = {"parameters": {"n": n}}
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "2002")))
    budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    deadline = time.monotonic() + budget
    best = _seed(n)
    best_score = _score(best, conf)
    optimized = _optimize(n, min(budget, max(0., deadline-time.monotonic())), rng)
    if optimized is not None:
        try:
            value = _score(optimized, conf)
            if value < best_score:
                best, best_score = optimized, value
        except ValueError:
            pass
    current = best
    # Coordinate values stay rational. Small translations can use the unused
    # grid cells; occasional 45-degree proposals explore a different geometry.
    # The exact checker, rather than a floating-point penalty, decides
    # feasibility and recomputes every candidate's score.
    step = Fraction(1, 8)
    while time.monotonic() < deadline:
        trial = {"squares": [dict(s) for s in current["squares"]]}
        idx = rng.randrange(n)
        sq = trial["squares"][idx]
        action = rng.randrange(5)
        if action < 4:
            key = "x" if action < 2 else "y"
            delta = step if action % 2 == 0 else -step
            sq[key] = str(Fraction(sq[key]) + delta)
        else:
            # tan(pi/8) is in Q(sqrt(2)); the checker supports Q(sqrt(2))
            # for center/vertex arithmetic, so use t=1/2 as an exact angle.
            sq["t"] = "1/2" if sq["t"] == "0" else "0"
        try:
            score = _score(trial, conf)
        except (ValueError, ZeroDivisionError):
            continue
        # Greedy improvement plus occasional neutral movement allows the
        # search to traverse layouts without ever dropping its valid archive.
        if score < best_score:
            best, best_score = trial, score
            current = trial
        elif score <= best_score and rng.random() < 0.08:
            current = trial
    return best
