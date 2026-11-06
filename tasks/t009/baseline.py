from mathbench.search import search_deadline, search_steps
"""Deterministic multistart local search over 16 nonzero 3D directions."""
import math
import os
import time
import numpy as np
from scipy.optimize import minimize

def _n():
    return {"T009-C02": 16, "T009-C03": 17, "T009-C04": 19}.get(os.environ.get("MATHBENCH_CONFIG_ID", "T009-C02"))

def _score(z):
    n = _n()
    if n is None: raise ValueError("unknown T009 configuration")
    p = np.asarray(z, dtype=float).reshape(n, 3)
    norms = np.linalg.norm(p, axis=1)
    if np.any(norms == 0): return -1.0
    p = p / norms[:, None]
    dots = p @ p.T
    return math.acos(float(np.max(dots[np.triu_indices(n, 1)])))

def run_code():
    n = _n()
    if n is None: raise ValueError("unknown T009 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = np.random.default_rng(seed)
    budget = max(.1, min(30., float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2"))))
    deadline = search_deadline()
    k=np.arange(n); z=1-2*(k+.5)/n; phi=k*math.pi*(3-math.sqrt(5)); r=np.sqrt(1-z*z)
    best=np.column_stack((r*np.cos(phi),r*np.sin(phi),z))
    best_score = _score(best)
    starts = 0
    for _attempt in search_steps(2):
        x = rng.normal(size=(n,3))
        x /= np.linalg.norm(x, axis=1)[:,None]
        def objective(z):
            p=np.asarray(z).reshape(n,3)
            norms=np.linalg.norm(p,axis=1)
            if np.any(norms < 1e-10): return 1e3
            p=p/norms[:,None]
            return float(np.max((p @ p.T)[np.triu_indices(n,1)]))
        res=minimize(objective,x.ravel(),method="L-BFGS-B",options={"maxiter":180,"ftol":1e-11})
        candidate=np.asarray(res.x).reshape(n,3)
        score=_score(candidate)
        if np.isfinite(score) and score > best_score:
            best,best_score=candidate.copy(),score
        starts+=1
    if best is None:
        # Well-defined deterministic fallback, independent of the human file.
        k=np.arange(n); z=1-2*(k+.5)/n; phi=k*math.pi*(3-math.sqrt(5)); r=np.sqrt(1-z*z)
        best=np.column_stack((r*np.cos(phi),r*np.sin(phi),z))
    return {"points": [[float(x) for x in row] for row in best]}

if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
