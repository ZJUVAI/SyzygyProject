"""Bounded seeded continuous search with exact rational acceptance."""
from fractions import Fraction
import os
import random
from mathbench.search import search_steps

_N = {"T001-C01": 26, "T001-C02": 32, "T001-C03": 50}


def _grid(n):
    cols = 1
    while cols*cols < n:
        cols += 1
    rows = (n+cols-1)//cols
    r = min(Fraction(1, 2*cols), Fraction(1, 2*rows))
    pts = [[str(Fraction(2*c+1, 2*cols)), str(Fraction(2*y+1, 2*rows))]
           for y in range(rows) for c in range(cols)][:n]
    return {"radius": str(r), "centers": pts}


def _feasible(candidate):
    from tasks.t001.check import validate
    n = len(candidate["centers"])
    cid = {26: "T001-C01", 32: "T001-C02", 50: "T001-C03"}[n]
    try:
        validate(candidate, {"id": cid, "parameters": {"n": n, "container": "unit square"}}, strict=True)
        return True
    except ValueError:
        return False


def run_code():
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T001-C01")
    n = _N[cid]
    best = _grid(n)
    # EVOLVE-BLOCK-START
    # Classical bounded multistart SLSQP; every returned candidate is rechecked
    # with exact rationals. The grid remains the deterministic fallback.
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    try:
        import numpy as np
        from scipy.optimize import minimize
        base = np.asarray([[float(Fraction(v)) for v in p] for p in best["centers"]])
        pair_i, pair_j = np.triu_indices(n, 1)
        for _attempt in search_steps(1):
            start = np.clip(base + np.asarray([[rng.uniform(-0.015, 0.015), rng.uniform(-0.015, 0.015)] for _ in range(n)]), 0.01, 0.99)
            z0 = np.r_[start.ravel(), float(Fraction(best["radius"]))]
            def clearance(z):
                xy = z[:-1].reshape(n, 2)
                r = z[-1]
                return np.r_[xy[:, 0]-r, 1-xy[:, 0]-r,
                             xy[:, 1]-r, 1-xy[:, 1]-r]
            def separation(z):
                xy = z[:-1].reshape(n, 2)
                delta = xy[pair_i] - xy[pair_j]
                return np.einsum("ij,ij->i", delta, delta) - 4*z[-1]**2
            cons = [{"type": "ineq", "fun": clearance},
                    {"type": "ineq", "fun": separation}]
            res=minimize(lambda z:-z[-1],z0,method="SLSQP",bounds=[(0,1)]*(2*n)+[(0,0.5)],constraints=cons,options={"maxiter":120,"ftol":1e-9})
            if not res.success:
                continue
            pts=[[format(float(res.x[2*i]), ".15f"),format(float(res.x[2*i+1]), ".15f")] for i in range(n)]
            r=Fraction(format(float(res.x[-1]), ".15f"))
            for _ in range(100):
                if r <= Fraction(best["radius"]):
                    break
                candidate={"radius":str(r),"centers":pts}
                if _feasible(candidate):
                    best=candidate
                    break
                r-=Fraction(1,10**12)
    except Exception:
        pass
    # EVOLVE-BLOCK-END
    return best
