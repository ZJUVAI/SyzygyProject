"""Multi-start continuous search with exact rational feasibility repair.

The optimizer is only a proposal generator.  Every archived construction is
reparsed and checked by the exact task checker before it can replace the grid
fallback.  Coordinates and tan(theta/2) are rational strings.
"""
import os
import random
import time
import json
import math
from fractions import Fraction

from tasks.t002.check import Q, validate


CONFIGS = {"T002-C01": 26, "T002-C02": 29, "T002-C03": 38}


def _seed(n):
    cols = 5 if n == 26 else (6 if n == 29 else 7)
    return {"squares": [
        {"x": str(Fraction(2 * (i % cols) + 1, 2)),
         "y": str(Fraction(2 * (i // cols) + 1, 2)), "t": "0"}
        for i in range(n)
    ]}


def _score(layout, n):
    return Q.parse(validate(layout, {"parameters": {"n": n}})["objective"])


def _numeric(q):
    return float(q.a) + float(q.b) * 2 ** .5


def _to_exact(z, n, np):
    centers = z[:2*n].reshape((n, 2))
    angles = z[2*n:3*n]
    return [{"x": str(Fraction(format(float(x), '.12g'))),
             "y": str(Fraction(format(float(y), '.12g'))),
             "t": str(Fraction(format(float(np.tan(a / 2)), '.12g')))}
            for (x, y), a in zip(centers, angles)]


def _repair(squares, n):
    """Compute the least uniform center dilation using exact separating axes."""
    cx = sum((Fraction(s["x"]) for s in squares), Fraction(0)) / n
    cy = sum((Fraction(s["y"]) for s in squares), Fraction(0)) / n
    xy = [(Fraction(s['x']), Fraction(s['y'])) for s in squares]
    axes = []
    for s in squares:
        t = Fraction(s['t']); den = 1 + t*t
        axes.append(((1-t*t)/den, 2*t/den))
    scale = Fraction(1)
    for i in range(n):
        ci, si = axes[i]
        for j in range(i):
            cj, sj = axes[j]
            dx, dy = xy[i][0]-xy[j][0], xy[i][1]-xy[j][1]
            projection = max(abs(dx*ci+dy*si), abs(-dx*si+dy*ci),
                             abs(dx*cj+dy*sj), abs(-dx*sj+dy*cj))
            if not projection:
                return None, None
            extent = (1 + abs(ci*cj+si*sj) + abs(si*cj-ci*sj))/2
            scale = max(scale, extent/projection)
    # Round the dilation upward to keep denominator size bounded. All pair
    # separations stay valid because their center projections increase.
    den = 10**13
    scale = Fraction((scale.numerator*den + scale.denominator-1)//scale.denominator, den)
    layout = {'squares': [{'x': str(cx+scale*(x-cx)), 'y': str(cy+scale*(y-cy)),
                            't': s['t']} for (x,y),s in zip(xy,squares)]}
    half = [(abs(c)+abs(s))/2 for c,s in axes]
    bounds = [[cx+scale*(x-cx)-h, cx+scale*(x-cx)+h,
               cy+scale*(y-cy)-h, cy+scale*(y-cy)+h] for (x,y),h in zip(xy,half)]
    side = max(max(b[1] for b in bounds)-min(b[0] for b in bounds),
               max(b[3] for b in bounds)-min(b[2] for b in bounds))
    return layout, Q(side)


def _optimize(n, seconds, rng, incumbent, warm_start=None):
    """Run fixed-box feasibility searches and return the exact best layout."""
    deadline = time.monotonic() + seconds
    try:
        import numpy as np
        from scipy.optimize import minimize
    except ImportError:
        return incumbent, 0, "grid_fallback_scipy_unavailable"

    cols = 5 if n == 26 else (6 if n == 29 else 7)
    rows = (n + cols - 1) // cols
    best = incumbent
    best_value = _numeric(_score(incumbent, n))
    chain = warm_start
    chain_value = best_value
    downhill_accepts = 0
    iterations = 0

    class DeadlineReached(Exception):
        pass

    ii, jj = np.triu_indices(n, 1)
    def loss_factory(weight, target):
        def loss(z):
            if time.monotonic() >= deadline:
                raise DeadlineReached
            xy=z[:2*n].reshape(n,2); ang=z[2*n:3*n]
            ca,sa=np.cos(ang),np.sin(ang)
            half=.5*(np.abs(ca)+np.abs(sa))
            hp=.5*(-np.sign(ca)*sa+np.sign(sa)*ca)
            gxy=np.zeros_like(xy); ga=np.zeros(n); value=0.
            for dim in range(2):
                for sign in (-1,1):
                    v=np.maximum(0.,sign*xy[:,dim]+half-target/2)
                    value+=v@v; gxy[:,dim]+=2*sign*v; ga+=2*v*hp
            d=xy[ii]-xy[jj]; delta=ang[ii]-ang[jj]
            ext=.5*(np.abs(np.cos(delta))+np.abs(np.sin(delta)))
            ep=.5*(-np.sign(np.cos(delta))*np.sin(delta)+np.sign(np.sin(delta))*np.cos(delta))
            axes=np.stack((np.stack((ca[ii],sa[ii]),1),np.stack((-sa[ii],ca[ii]),1),
                           np.stack((ca[jj],sa[jj]),1),np.stack((-sa[jj],ca[jj]),1)),1)
            proj=np.einsum('mi,mki->mk',d,axes)
            gaps=np.abs(proj)-.5-ext[:,None]
            k=np.argmax(gaps,axis=1); row=np.arange(len(ii))
            v=np.maximum(0.,-gaps[row,k]); value+=v@v
            axis=axes[row,k]; sg=np.sign(proj[row,k]); coeff=-2*v
            grad=coeff[:,None]*sg[:,None]*axis
            np.add.at(gxy,ii,grad); np.add.at(gxy,jj,-grad)
            directional=sg*(-d[:,0]*axis[:,1]+d[:,1]*axis[:,0])
            gi=-ep+np.where(k<2,directional,0.)
            gj=ep+np.where(k>=2,directional,0.)
            np.add.at(ga,ii,coeff*gi); np.add.at(ga,jj,coeff*gj)
            return weight*value, weight*np.r_[gxy.ravel(),ga,0.]
        return loss

    # Alternate warm starts, axis-grid starts, and structured rotation
    # clusters. Shrinking target sizes turn this into a sequence of SAT
    # feasibility problems, with each stage increasing collision pressure.
    start_number = 0
    while time.monotonic() < deadline:
        if start_number % 12 == 0:
            chain, chain_value = warm_start, best_value
        if start_number % 3 != 2 and chain is not None:
            xy = np.array([[float(Fraction(s['x'])), float(Fraction(s['y']))]
                           for s in chain['squares']], dtype=float)
            angles = np.array([2 * math.atan(float(Fraction(s['t'])))
                               for s in chain['squares']], dtype=float)
            side = chain_value
            xy -= (xy.max(axis=0)+xy.min(axis=0))/2
            target = min(side, best_value) - (.002,.025,.08,.18)[start_number % 4]
            xy += np.array([[rng.uniform(-.08, .08),
                             rng.uniform(-.08, .08)] for _ in range(n)])
            angles += np.array([rng.uniform(-.08, .08) for _ in range(n)])
            if start_number % 4 == 3:
                for index in rng.sample(range(n),max(1,n//6)):
                    angles[index]+=rng.choice((-.4,.4))
        else:
            cols = rng.choice((int(math.sqrt(n)), int(math.sqrt(n))+1))
            rows = (n + cols - 1) // cols
            sites = rng.sample(range(cols*rows), n)
            xy = np.array([[(i % cols) + .5, (i // cols) + .5]
                           for i in sites], dtype=float)
            jitter = .12 if start_number == 0 else .38
            base_side = float(max(cols, rows))
            # Begin close to the fixed box. The center scaling is only a
            # continuous start; exact containment is never assumed.
            target = best_value - (.005 + .008 * ((start_number - 1) % 5))
            factor = max(.82, target / base_side)
            xy = (xy - np.array([cols / 2, rows / 2])) * factor
            xy += np.array([[rng.uniform(-jitter, jitter),
                             rng.uniform(-jitter, jitter)] for _ in range(n)])
            # Rotate in a few coherent clusters before adding small noise.
            clusters = (0., math.pi/8, -math.pi/8, math.pi/4, -math.pi/4)
            cluster = clusters[(start_number - 1) % len(clusters)]
            angles = np.array([(cluster if i % cols >= cols//2 else 0.)
                               + rng.uniform(-.07, .07) for i in sites])
        z = np.concatenate((xy.ravel(), angles, [target]))
        start_number += 1
        for weight in (1.e3, 1.e5, 1.e7):
            if time.monotonic() >= deadline:
                break
            def stop_if_expired(_x):
                if time.monotonic() >= deadline:
                    raise DeadlineReached
            try:
                result = minimize(loss_factory(weight, target), z,
                                  method="L-BFGS-B", jac=True, callback=stop_if_expired,
                                  bounds=[(None, None)] * (len(z)-1) + [(target, target)],
                                  options={"maxiter": 1000, "ftol": 1.e-12,
                                           "maxls": 40})
                iterations += int(getattr(result, "nit", 0))
                z = result.x
            except DeadlineReached:
                break
            raw = _to_exact(z, n, np)
            candidate, value = _repair(raw, n)
            if candidate is not None and _numeric(value) < best_value:
                best, best_value = candidate, _numeric(value)
                warm_start = candidate
            if candidate is not None:
                numeric = _numeric(value)
                temperature = .025
                if numeric <= chain_value or rng.random() < math.exp(min(0.,(chain_value-numeric)/temperature)):
                    downhill_accepts += int(numeric > chain_value)
                    chain, chain_value = candidate, numeric
            if result.fun / weight < 1.e-10:
                target -= .01
            if time.monotonic() >= deadline:
                break
        # The next loop makes a fully independent randomized start.
    return best, iterations, "cluster_rotation_sat_annealing_exact_minimal_dilation"


def run_code():
    started = time.monotonic()
    cid = os.environ.get("MATHBENCH_CONFIG_ID", "T002-C01")
    if cid not in CONFIGS:
        raise ValueError("unknown T002 configuration")
    n = CONFIGS[cid]
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "2002")))
    budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    best = _seed(n)  # Always-valid exact fallback.
    warm_start = None
    warm_path = os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        try:
            with open(warm_path, encoding="utf-8") as stream:
                proposed = json.load(stream)
            _score(proposed, n)
            warm_start = proposed
            if _numeric(_score(proposed, n)) < _numeric(_score(best, n)):
                best = proposed
        except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError):
            warm_start = None
    best, iterations, method = _optimize(n, max(0.,budget-(time.monotonic()-started)), rng, best, warm_start)
    # Defensive final replay; never emit a proposal the exact checker rejects.
    _score(best, n)
    best["search_method"] = method
    best["search_iterations"] = iterations
    return best
