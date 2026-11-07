"""Exact-checked, warm-started SLSQP search for Heilbronn configurations."""
from fractions import Fraction
from itertools import combinations
import json
import os
import time

import numpy as np
from scipy.optimize import minimize

from tasks.t005.check import validate

_CONFIG_N = {"T005-C01": 11, "T005-C02": 12, "T005-C03": 16}


class _DeadlineReached(Exception):
    pass


def _serialize(xy):
    return [[format(float(x), ".16g"), format(float(y), ".16g")] for x, y in xy]


def _exact_score(points):
    return Fraction(validate({"points": points}, {"parameters": {"n": len(points)}})["objective"])


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T005-C01")
    n = _CONFIG_N.get(config_id, _CONFIG_N["T005-C01"])
    seconds = max(0.1, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = np.random.default_rng(seed)
    deadline = time.monotonic() + seconds
    triples = np.asarray(list(combinations(range(n), 3)), dtype=np.intp)
    incumbent = None
    incumbent_score = Fraction(-1)
    exact_checks = 0
    optimizer_iterations = 0

    def consider(xy):
        nonlocal incumbent, incumbent_score, exact_checks
        array = np.asarray(xy, dtype=float).reshape((n, 2))
        if incumbent is not None:
            a, b, c = array[triples[:, 0]], array[triples[:, 1]], array[triples[:, 2]]
            det = ((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) -
                   (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))
            # A cheap upper-level filter avoids costly rational checks for
            # candidates that cannot beat the exact incumbent.
            if float(np.min(np.abs(det))) <= float(incumbent_score) * 2.0 - 1e-14:
                return
        points = _serialize(array)
        try:
            score = _exact_score(points)
        except (ValueError, TypeError, ZeroDivisionError):
            return
        exact_checks += 1
        if score > incumbent_score:
            incumbent, incumbent_score = points, score

    warm_path = os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        # Runner snapshots the task's own best into this immutable run directory.
        with open(os.path.abspath(warm_path), encoding="utf-8") as handle:
            warm = json.load(handle)
        warm_points = warm.get("points") if isinstance(warm, dict) else None
        if not isinstance(warm_points, list) or len(warm_points) != n:
            raise ValueError("warm start does not match the active configuration")
        incumbent_score = _exact_score(warm_points)
        incumbent = warm_points
    if incumbent is None:
        consider(rng.uniform(0.0, 1.0, size=(n, 2)))

    def optimize(start):
        nonlocal optimizer_iterations
        if time.monotonic() >= deadline:
            raise _DeadlineReached
        xy = np.asarray(start, dtype=float).reshape((n, 2))
        a, b, c = xy[triples[:, 0]], xy[triples[:, 1]], xy[triples[:, 2]]
        det = ((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) -
               (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))
        orient = np.sign(det)
        orient[orient == 0] = 1.0

        def margins(v):
            if time.monotonic() >= deadline:
                raise _DeadlineReached
            p = v[:2 * n].reshape((n, 2))
            aa, bb, cc = p[triples[:, 0]], p[triples[:, 1]], p[triples[:, 2]]
            area2 = ((bb[:, 0] - aa[:, 0]) * (cc[:, 1] - aa[:, 1]) -
                     (bb[:, 1] - aa[:, 1]) * (cc[:, 0] - aa[:, 0]))
            return orient * area2 - v[-1]

        def margins_jac(v):
            p=v[:2*n].reshape(n,2)
            aa,bb,cc=p[triples[:,0]],p[triples[:,1]],p[triples[:,2]]
            jac=np.zeros((len(triples),2*n+1)); row=np.arange(len(triples))
            for index,dx,dy in ((0,bb[:,1]-cc[:,1],cc[:,0]-bb[:,0]),
                                (1,cc[:,1]-aa[:,1],aa[:,0]-cc[:,0]),
                                (2,aa[:,1]-bb[:,1],bb[:,0]-aa[:,0])):
                jac[row,2*triples[:,index]]=orient*dx
                jac[row,2*triples[:,index]+1]=orient*dy
            jac[:,-1]=-1
            return jac

        def callback(v):
            nonlocal optimizer_iterations
            optimizer_iterations += 1
            # The incumbent is always the exact rational checker score.
            consider(v[:2 * n])
            if time.monotonic() >= deadline:
                raise _DeadlineReached

        x0 = np.concatenate((xy.ravel(), [0.0]))
        bounds = [(0.0, 1.0)] * (2 * n) + [(0.0, 1.0)]
        result = minimize(lambda v: -v[-1], x0, method="SLSQP", bounds=bounds,
                          jac=lambda v: np.r_[np.zeros(2*n),-1.],
                          constraints=[{"type": "ineq", "fun": margins,"jac":margins_jac}],
                          callback=callback,
                          options={"maxiter": 350, "ftol": 1e-11, "disp": False})
        consider(result.x[:2 * n])
        return result.x[:2*n].reshape(n, 2).copy()

    # Perturb the verified incumbent at several scales. Also use random starts
    # to reach other orientation classes. Exact scores decide every incumbent.
    scales = (0.025, 0.08, 0.18, 0.35)
    restart = 0
    chain = np.asarray(incumbent, dtype=float)
    chain_score = float(incumbent_score)
    downhill_accepts = 0
    def numeric_score(points):
        a,b,c = points[triples[:,0]],points[triples[:,1]],points[triples[:,2]]
        return float(np.min(np.abs((b[:,0]-a[:,0])*(c[:,1]-a[:,1])
                                   -(b[:,1]-a[:,1])*(c[:,0]-a[:,0]))))/2
    while time.monotonic() < deadline:
        if restart % 8 < 7:
            base = chain.copy() if restart % 8 else np.asarray(incumbent, dtype=float)
            scale = scales[(restart // 4) % len(scales)]
            if restart % 8 == 6:
                # Replace one point with the best of sampled locations. The
                # score only considers triangles that contain this point.
                start = base.copy()
                index = int(rng.integers(n))
                other = np.delete(base,index,axis=0)
                pairs = np.asarray(list(combinations(range(n-1),2)))
                p,q = other[pairs[:,0]],other[pairs[:,1]]
                probes = rng.uniform(0,1,size=(192,2))
                area = np.abs((q[None,:,0]-p[None,:,0])*(probes[:,None,1]-p[None,:,1])
                              -(q[None,:,1]-p[None,:,1])*(probes[:,None,0]-p[None,:,0]))
                start[index] = probes[np.argmax(np.min(area,axis=1))]
            elif restart % 8 < 4:
                # Move one vertex across its tightest triangle line. This
                # changes one orientation cell without disturbing all points.
                start=base.copy()
                a,b,c=base[triples[:,0]],base[triples[:,1]],base[triples[:,2]]
                det=(b[:,0]-a[:,0])*(c[:,1]-a[:,1])-(b[:,1]-a[:,1])*(c[:,0]-a[:,0])
                tri=triples[np.argsort(np.abs(det))[rng.integers(min(12,len(triples)))]]
                i,j,k=rng.permutation(tri); edge=base[k]-base[j]
                normal=np.array([-edge[1],edge[0]])
                normal/=max(np.linalg.norm(normal),1e-12)
                distance=np.dot(base[i]-base[j],normal)
                start[i]-=(2*distance+rng.normal(0,.01))*normal
                start=np.clip(start,0,1)
            else:
                start = np.clip(base + rng.normal(0.0, scale, size=(n, 2)), 0.0, 1.0)
        else:
            start = rng.uniform(0.0, 1.0, size=(n, 2))
        try:
            local = optimize(start)
            score = numeric_score(local)
            temperature = max(float(incumbent_score)*.025,
                              float(incumbent_score)*.12*(.998**restart))
            if score >= chain_score or rng.random() < np.exp((score-chain_score)/max(temperature,1e-12)):
                downhill_accepts += int(score < chain_score)
                chain, chain_score = local, score
        except _DeadlineReached:
            break
        restart += 1

    # Recheck the final serialized witness before returning it.
    validate({"points": incumbent}, {"parameters": {"n": n}})
    return {"points": incumbent,
            "search_metadata": {"optimizer_iterations": optimizer_iterations,
                                "exact_score_checks": exact_checks,
                                "restarts": restart,
                                "downhill_accepts": downhill_accepts,
                                "method": "orientation_cell_annealing_and_vertex_relocation"}}
