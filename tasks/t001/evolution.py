"""Warm-start multistart SLSQP search for equal-circle square packings.

The search uses only synthetic grids, hexagonal rows, and seeded random
perturbations.  Every incumbent is rounded to rational centers and assigned a
conservative rational radius before it is retained.
"""
from fractions import Fraction
import math
import os
import random
import time


_CONFIG_N = {"T001-C01": 26, "T001-C02": 32, "T001-C03": 50}
_DEN = 10**15


def _candidate(points):
    """Round centers and compute a radius certified by integer arithmetic."""
    pts = [(round(float(x) * _DEN), round(float(y) * _DEN)) for x, y in points]
    if len(set(pts)) != len(pts):
        return None
    wall = min(min(x, y, _DEN - x, _DEN - y) for x, y in pts)
    if wall <= 0:
        return None
    min_d2 = None
    for i, (x, y) in enumerate(pts):
        for a, b in pts[:i]:
            d2 = (x-a)**2 + (y-b)**2
            if min_d2 is None or d2 < min_d2:
                min_d2 = d2
    if min_d2 is None:
        return None
    radius_ticks = min(wall, math.isqrt(min_d2) // 2)
    if radius_ticks <= 0:
        return None
    candidate = {
        "radius": str(Fraction(radius_ticks, _DEN)),
        "centers": [[str(Fraction(x, _DEN)), str(Fraction(y, _DEN))] for x, y in pts],
    }
    return candidate


def _grid(n, cols, hexagonal=False):
    rows = (n + cols - 1) // cols
    pts = []
    for row in range(rows):
        count = min(cols, n - len(pts))
        for col in range(count):
            x = (col + 0.5 + (0.5 if hexagonal and row % 2 else 0.0)) / (cols + (0.5 if hexagonal else 0.0))
            y = (row + 0.5) / rows
            pts.append((x, y))
    return pts


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T001-C01")
    n = _CONFIG_N.get(config_id, _CONFIG_N["T001-C01"])
    seconds = max(0.1, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    deadline = time.monotonic() + seconds
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    import numpy as np
    from scipy.optimize import minimize
    from tasks.t001.check import validate

    best = None
    best_r = Fraction(0)
    warm_points = None
    warm_radius = 0.0
    warm_path = os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        # The runner supplies an immutable copy of this task's own saved best.
        import json
        from pathlib import Path
        saved = json.loads(Path(warm_path).read_text())
        if len(saved.get("centers", [])) == n:
            checked = validate(saved, {"id":config_id,"parameters":{"n":n,"container":"unit square"}}, strict=True)
            best, best_r = saved, Fraction(checked["objective"])
            warm_points = np.asarray([[float(Fraction(x)), float(Fraction(y))]
                                      for x, y in saved["centers"]])
            warm_radius = float(Fraction(saved["radius"]))

    def consider(xy):
        nonlocal best, best_r
        cand = _candidate(np.asarray(xy).reshape(n, 2))
        if cand is None:
            return
        if Fraction(cand['radius']) <= best_r:
            return
        try:
            checked = validate(cand, {"id": config_id, "parameters": {"n": n, "container": "unit square"}}, strict=True)
        except (ValueError, TypeError, ZeroDivisionError):
            return
        score = Fraction(checked["objective"])
        if score > best_r:
            best, best_r = cand, score

    pair_i, pair_j = np.triu_indices(n, 1)
    m = len(pair_i)

    def constraints(z):
        xy = z[:-1].reshape(n, 2)
        r = z[-1]
        delta = xy[pair_i] - xy[pair_j]
        d2 = np.einsum("ij,ij->i", delta, delta)
        return np.r_[xy[:, 0]-r, 1-xy[:, 0]-r, xy[:, 1]-r, 1-xy[:, 1]-r,
                     d2 - 4*r*r]

    def constraints_jac(z):
        xy = z[:-1].reshape(n, 2)
        r = z[-1]
        jac = np.zeros((4*n + m, 2*n + 1))
        idx = np.arange(n)
        jac[idx, 2*idx] = 1; jac[idx, -1] = -1
        jac[n+idx, 2*idx] = -1; jac[n+idx, -1] = -1
        jac[2*n+idx, 2*idx+1] = 1; jac[2*n+idx, -1] = -1
        jac[3*n+idx, 2*idx+1] = -1; jac[3*n+idx, -1] = -1
        delta = xy[pair_i] - xy[pair_j]
        row = np.arange(4*n, 4*n+m)
        jac[row, 2*pair_i] = 2*delta[:, 0]
        jac[row, 2*pair_i+1] = 2*delta[:, 1]
        jac[row, 2*pair_j] = -2*delta[:, 0]
        jac[row, 2*pair_j+1] = -2*delta[:, 1]
        jac[row, -1] = -8*r
        return jac

    # Seed the incumbent before optimization; the grid is an exact fallback.
    starts = []
    if warm_points is not None:
        starts.append(warm_points.copy())
    for cols in sorted({max(2, round(math.sqrt(n))), max(2, round(math.sqrt(n))+1), max(2, round(math.sqrt(n))-1)}):
        starts.extend((_grid(n, cols), _grid(n, cols, True)))
    for pts in starts:
        consider(pts)

    solve_count = 0
    while time.monotonic() < deadline:
        template = starts[solve_count % len(starts)]
        if best is not None and solve_count % 3 != 2:
            template = np.array([[float(Fraction(x)),float(Fraction(y))] for x,y in best["centers"]])
        xy = np.asarray(template, dtype=float).copy()
        mode = (solve_count // len(starts)) % 4
        if warm_points is not None and template is starts[0]:
            # Alternate a direct refinement with local contact-graph changes.
            scale = (0.0015, 0.006, 0.018)[(solve_count // len(starts)) % 3]
            xy += np.asarray([[rng.uniform(-scale, scale), rng.uniform(-scale, scale)] for _ in range(n)])
        elif mode == 0:
            scale = 0.012
            xy += np.asarray([[rng.uniform(-scale, scale), rng.uniform(-scale, scale)] for _ in range(n)])
        elif mode == 1:
            xy = np.asarray([[rng.random(), rng.random()] for _ in range(n)])
        else:
            # Randomly permute labels and use a larger perturbation to change contacts.
            xy = xy[np.asarray(rng.sample(range(n), n))]
            scale = 0.035
            xy += np.asarray([[rng.uniform(-scale, scale), rng.uniform(-scale, scale)] for _ in range(n)])
        if solve_count % 5 == 4:
            # Relocate a single circle to a sampled largest empty region.
            index=rng.randrange(n)
            probes=np.array([[rng.random(),rng.random()] for _ in range(256)])
            rest=np.delete(xy,index,axis=0)
            gap=np.minimum(np.min(np.linalg.norm(probes[:,None,:]-rest[None,:,:],axis=2),axis=1)/2,
                           np.min(np.c_[probes,1-probes],axis=1))
            xy[index]=probes[np.argmax(gap)]
        xy = np.clip(xy, 1e-5, 1-1e-5)
        if solve_count % 3 != 0 and best_r > 0:
            # Relax overlaps at a fixed, slightly compressed radius before
            # maximizing radius. This permits contact changes at lower cost.
            target = float(best_r) * (1.001, 1.008, 1.025)[solve_count % 3]
            def soft_loss(flat):
                if time.monotonic() >= deadline:
                    raise TimeoutError
                p = flat.reshape(n,2)
                delta = p[pair_i]-p[pair_j]
                distance = np.maximum(np.linalg.norm(delta,axis=1),1e-12)
                overlap = np.maximum(2*target-distance,0.)
                low = np.maximum(target-p,0.)
                high = np.maximum(p-(1-target),0.)
                gradient = -2*low+2*high
                force = -2*overlap[:,None]*delta/distance[:,None]
                np.add.at(gradient,pair_i,force)
                np.add.at(gradient,pair_j,-force)
                return float(overlap@overlap+np.sum(low*low+high*high)),gradient.ravel()
            try:
                relaxed = minimize(soft_loss,xy.ravel(),method='L-BFGS-B',jac=True,
                                   bounds=[(1e-6,1-1e-6)]*(2*n),
                                   options={'maxiter':180,'ftol':1e-12,'gtol':1e-8})
                xy = relaxed.x.reshape(n,2)
            except TimeoutError:
                break
        consider(xy)
        initial = _candidate(xy)
        r0 = max(float(Fraction(initial["radius"])) if initial else 1e-5,
                 warm_radius * 0.999999 if warm_points is not None and np.array_equal(template, starts[0]) else 1e-5)
        z0 = np.r_[xy.ravel(), r0]

        last_check = [0]
        def callback(z):
            # Exact arithmetic is costly; check every fourth major iterate.
            last_check[0] += 1
            if last_check[0] % 4 == 0:
                consider(z[:-1])
            if time.monotonic() >= deadline:
                raise TimeoutError

        try:
            result = minimize(lambda z: -z[-1], z0, method="SLSQP",
                              jac=lambda z: np.r_[np.zeros(2*n), -1.0],
                              bounds=[(1e-8, 1-1e-8)]*(2*n)+[(0.0, 0.5)],
                              constraints=[{"type": "ineq", "fun": constraints, "jac": constraints_jac}],
                              callback=callback,
                              options={"maxiter": 180, "ftol": 2e-13, "disp": False})
            consider(result.x[:-1])
        except TimeoutError:
            break
        solve_count += 1

    # Validate again before returning. The incumbent always includes the grid.
    validate(best, {"id": config_id, "parameters": {"n": n, "container": "unit square"}}, strict=True)
    best['search_metadata'] = {'solves':solve_count,'method':'soft_collision_relaxation_slsqp_exact_radius'}
    return best
