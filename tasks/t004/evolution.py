"""Multistart smooth search for Tammes configurations on the unit sphere."""
import json
import math
import os
import random
import time


def _size():
    config = os.environ.get("MATHBENCH_CONFIG_ID", "T004-C01")
    sizes = {"T004-C01": 16, "T004-C02": 17, "T004-C03": 19}
    if config not in sizes:
        raise ValueError("unsupported MATHBENCH_CONFIG_ID")
    return sizes[config]


def _fibonacci(n, rng, jitter=0.0):
    golden = math.pi * (3.0 - math.sqrt(5.0))
    points = []
    for k in range(n):
        z = 1.0 - 2.0 * (k + 0.5) / n
        phi = k * golden + rng.uniform(-jitter, jitter)
        r = math.sqrt(max(0.0, 1.0 - z*z))
        points.append((r*math.cos(phi), r*math.sin(phi), z))
    return points


def _optimize(points, seconds, deadline):
    import numpy as np
    from scipy.optimize import minimize
    n = len(points)
    pairs = [(i, j) for i in range(n) for j in range(i)]
    ii = np.array([i for i, _ in pairs]); jj = np.array([j for _, j in pairs])
    x0 = np.concatenate((np.asarray(points, dtype=float).reshape(-1), [0.0]))
    incumbent = [np.asarray(points, dtype=float)]
    # Minimize t subject to every normalized-direction dot product <= t.
    def objective(x): return float(x[-1])
    def objective_jac(x):
        g=np.zeros(3*n+1); g[-1]=1.0; return g
    def sphere(x):
        p=x[:-1].reshape(n,3); return np.einsum("ij,ij->i",p,p)-1.0
    def sphere_jac(x):
        p=x[:-1].reshape(n,3); g=np.zeros((n,3*n+1))
        for i in range(n): g[i,3*i:3*i+3]=2*p[i]
        return g
    def gaps(x):
        p=x[:-1].reshape(n,3); return x[-1]-np.einsum("ij,ij->i",p[ii],p[jj])
    def gaps_jac(x):
        p=x[:-1].reshape(n,3); g=np.zeros((len(pairs),3*n+1))
        for k,(i,j) in enumerate(pairs):
            g[k,3*i:3*i+3]=-p[j]; g[k,3*j:3*j+3]=-p[i]; g[k,-1]=1
        return g
    def callback(_x):
        p=_x[:-1].reshape(n,3).copy()
        p/=np.maximum(np.linalg.norm(p,axis=1)[:,None],1e-12)
        incumbent[0]=p
        if time.monotonic() >= deadline: raise TimeoutError("evolution budget reached")
    try:
        result=minimize(objective,x0,jac=objective_jac,method="SLSQP",
                        constraints=[{"type":"eq","fun":sphere,"jac":sphere_jac},
                                     {"type":"ineq","fun":gaps,"jac":gaps_jac}],
                        callback=callback,
                        options={"maxiter":240,"ftol":2e-13,"disp":False})
        p=result.x[:-1].reshape(n,3)
    except TimeoutError:
        p=incumbent[0]
    norms=np.linalg.norm(p,axis=1)
    p=p/np.maximum(norms[:,None],1e-12)
    return p.tolist()


def run_code():
    n=_size(); seed=int(os.environ.get("MATHBENCH_SEED","0")); rng=random.Random(seed)
    budget=max(0.2,float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS","45")))
    start=time.monotonic(); deadline=start+budget
    best=_fibonacci(n,rng)
    best_score=min(sum((best[i][k]-best[j][k])**2 for k in range(3))
                   for i in range(n) for j in range(i))
    exact_best={"points":best}
    from tasks.t004.check import validate
    config={"id":os.environ.get("MATHBENCH_CONFIG_ID","T004-C01"),"parameters":{"n":n,"space":"S2","objective":"minimum pairwise angular separation in radians"}}
    warm_path=os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        from fractions import Fraction
        with open(warm_path) as f: warm=json.load(f)
        validate(warm,config,strict=True)
        exact_best=warm
        best=[[float(Fraction(v)) for v in p] for p in warm["points"]]
        import numpy as np
        arr=np.asarray(best); arr/=np.linalg.norm(arr,axis=1)[:,None]; best=arr.tolist()
        best_score=min(sum((best[i][k]-best[j][k])**2 for k in range(3)) for i in range(n) for j in range(i))
    certified=validate(exact_best,config,strict=True)["objective"]
    attempts=0
    while attempts == 0 or time.monotonic()-start < budget:
        init=_fibonacci(n,rng,0.8 if attempts else 0.0)
        if attempts % 4 != 3:
            import numpy as np
            arr=np.asarray(best)
            scale=(.001,.025,.10,.25)[(attempts//4)%4]
            arr+=np.array([[rng.gauss(0,scale) for _ in range(3)] for _ in range(n)])
            arr/=np.linalg.norm(arr,axis=1)[:,None]; init=arr.tolist()
        try:
            candidate=_optimize(init,max(0.0,budget-(time.monotonic()-start)),deadline)
            # Save every valid incumbent immediately; checker recomputes score.
            score=min(sum((candidate[i][k]-candidate[j][k])**2 for k in range(3))
                      for i in range(n) for j in range(i))
            if score>best_score:
                checked=validate({"points":candidate},config,strict=True)["objective"]
                if checked>certified:
                    best_score=score; best=candidate; exact_best={"points":candidate}; certified=checked
        except TimeoutError:
            break
        except Exception:
            pass
        attempts+=1
    return {**exact_best,"search":{"algorithm":"Fibonacci and perturbed multistart SLSQP chord-maximization",
            "seed":seed,"attempts":attempts,"seconds":time.monotonic()-start}}


if __name__ == "__main__":
    print(json.dumps(run_code()))
