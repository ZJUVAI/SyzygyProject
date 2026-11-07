from mathbench.search import search_deadline, search_steps
"""Bounded numerical search; exact checker remains the authority."""
import os
import time
from fractions import Fraction

from scipy.optimize import minimize

# This file intentionally uses only a generated grid seed, never human data.
def _seed(n):
    return ([(str(Fraction(2*c+1,12)), str(Fraction(2*r+1,12)), '1/12') for r in range(6) for c in range(6)][:n] if n <= 36 else [(str(Fraction(2*c+1,16)), str(Fraction(2*r+1,10)), '1/16') for r in range(5) for c in range(8)])

def run_code():
    import os
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T003-C01")
    try: n = {"T003-C01":26,"T003-C02":32,"T003-C03":40}[cid]
    except KeyError: raise ValueError(f"unsupported T003 configuration: {cid}") from None
    valid = _seed(n)
    budget = max(0.1, min(30.0, float(os.environ.get("MATHBENCH_SEARCH_SECONDS", "2"))))
    deadline = search_deadline()
    # SLSQP proposes center and radius updates. Retain the exact grid if the
    # proposal does not finish or does not improve this feasible objective.
    try:
        import numpy as np
        z0 = np.array([[float(Fraction(v)) for v in circle] for circle in valid], dtype=float).reshape(-1)
        def objective(z): return -float(sum(z[2::3]))
        constraints = []
        for i in range(n):
            constraints += [
                {"type":"ineq", "fun":lambda z,i=i: z[3*i]-z[3*i+2]},
                {"type":"ineq", "fun":lambda z,i=i: 1-z[3*i]-z[3*i+2]},
                {"type":"ineq", "fun":lambda z,i=i: z[3*i+1]-z[3*i+2]},
                {"type":"ineq", "fun":lambda z,i=i: 1-z[3*i+1]-z[3*i+2]},
            ]
        for i in range(n):
            for j in range(i):
                constraints.append({"type":"ineq", "fun":lambda z,i=i,j=j:
                    (z[3*i]-z[3*j])**2+(z[3*i+1]-z[3*j+1])**2-(z[3*i+2]+z[3*j+2])**2})
        result = minimize(objective, z0, method="SLSQP", bounds=[(0,1),(0,1),(1e-8,0.5)]*n,
                          constraints=constraints, options={"maxiter":max(1, min(12, int(budget*2))),"ftol":1e-9})
        if time.monotonic() <= deadline and result.success and -result.fun > n/12:
            proposal = [(float(result.x[3*i]),float(result.x[3*i+1]),float(result.x[3*i+2])-1e-8) for i in range(n)]
            from tasks.t003.check import validate
            candidate = {"circles":[{"x":x,"y":y,"r":r} for x,y,r in proposal]}
            if time.monotonic() <= deadline:
                try:
                    validate(candidate, {"id": {26:"T003-C01",32:"T003-C02",40:"T003-C03"}[n]}, strict=True)
                    valid = proposal
                except ValueError:
                    pass
    except Exception:
        pass
    return {"circles":[{"x":x,"y":y,"r":r} for x,y,r in valid]}

if __name__ == "__main__":
    import json
    print(json.dumps(run_code()))
