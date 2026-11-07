"""Multistart continuous optimization for T015, with exact rational selection."""
import os
import random
import time
import json
from fractions import Fraction

import numpy as np

from tasks.t015.check import objective_fraction
from tasks.t015.init_program import run_code as initial


def _objective(x):
    # Normalization to unit mass removes the scale invariance.
    x = np.maximum(np.asarray(x, dtype=float), 0.0)
    mass = float(x.sum())
    if not np.isfinite(mass) or mass <= 1e-15:
        return -1e6
    x = x / mass
    b = np.convolve(x, x)
    return (2.0 * np.dot(b, b) + np.dot(b[:-1], b[1:])) / (3.0 * b.max())


def _gradient(x):
    b = np.convolve(x, x)
    idx = np.arange(39)[:, None] - np.arange(20)[None, :]
    jac = 2*x[np.clip(idx, 0, 19)]*((idx >= 0) & (idx < 20))
    weights = 4*b
    weights[:-1] += b[1:]
    weights[1:] += b[:-1]
    numerator = 2*np.dot(b,b)+np.dot(b[:-1],b[1:])
    k = np.argmax(b)
    return -(weights@jac/b[k] - numerator*jac[k]/b[k]**2)/3


def _rationalize(x):
    x = np.maximum(np.asarray(x, dtype=float), 0.0)
    if not np.isfinite(x).all() or x.sum() <= 1e-15:
        return None
    x /= x.sum()
    # Bounded denominators keep exact checking practical while preserving shape.
    return [Fraction(float(v)).limit_denominator(100000) for v in x]


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = np.random.default_rng(seed)
    py_rng = random.Random(seed)
    try:
        budget = max(0.0, float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45")))
    except ValueError:
        budget = 45.0
    deadline = time.monotonic() + budget

    # Keep a valid fallback, then prefer the supplied own-best archive when present.
    best = [Fraction(int(v)) for v in initial()["coefficients"]]
    warm_path = os.environ.get("MATHBENCH_WARM_START")
    if warm_path:
        try:
            with open(warm_path, encoding="utf-8") as source:
                warm = json.load(source)
            raw = warm.get("coefficients", [])
            warm_coefficients = [Fraction(str(v)) for v in raw]
            if len(warm_coefficients) == 20 and all(v >= 0 for v in warm_coefficients) and sum(warm_coefficients) > 0:
                best = warm_coefficients
        except (OSError, ValueError, TypeError, ZeroDivisionError):
            pass
    best_value, _ = objective_fraction(best)
    try:
        from scipy.optimize import minimize
    except ImportError:
        return {"coefficients": [str(v) for v in best]}

    # Introduce an epigraph variable for the largest convolution value.
    # This keeps all derivatives smooth even when several peaks are active.
    idx = np.arange(39)[:,None]-np.arange(20)[None,:]
    mask = (idx>=0)&(idx<20)
    clipped = np.clip(idx,0,19)
    def terms(z):
        x=z[:20]; b=np.convolve(x,x)
        jac=2*x[clipped]*mask
        numerator=2*np.dot(b,b)+np.dot(b[:-1],b[1:])
        w=4*b.copy();w[:-1]+=b[1:];w[1:]+=b[:-1]
        return b,jac,numerator,w@jac
    def fun(z):
        return -terms(z)[2]/(3*z[-1])
    def grad(z):
        b,jac,num,dnum=terms(z)
        return np.r_[-dnum/(3*z[-1]), num/(3*z[-1]**2)]
    def ineq(z):
        return z[-1]-np.convolve(z[:20],z[:20])
    def ineq_jac(z):
        return np.c_[-2*z[:20][clipped]*mask,np.ones(39)]
    def consider(x):
        nonlocal best,best_value
        x=np.maximum(x,0)
        if x.sum()<=1e-15 or _objective(x)<=float(best_value)+1e-14:
            return
        # A common grid avoids large, unrelated rational denominators.
        units=np.rint(x/x.sum()*10**12).astype(np.int64)
        candidate=[Fraction(int(v),10**12) for v in units]
        value,_=objective_fraction(candidate)
        if value>best_value:
            best,best_value=candidate,value
    restarts=0
    while time.monotonic()<deadline:
        warm_x=np.array([float(v) for v in best]);warm_x/=warm_x.sum()
        mode = restarts % 10
        if restarts==0:
            x0=warm_x.copy()
        elif mode in (0,1):
            scale=(.001,.005,.02,.08,.2)[(restarts//10)%5]
            x0=np.maximum(warm_x+rng.normal(0,scale,20),0)
        elif mode==2:
            x0=warm_x*np.exp(rng.normal(0,rng.uniform(.15,1.5),20))
        elif mode==3:
            # Remove part of the support, then let SLSQP choose active entries.
            x0=warm_x.copy()
            remove=rng.choice(20,size=int(rng.integers(1,8)),replace=False)
            x0[remove]=0
        elif mode==4:
            x0=warm_x.copy()
            for _ in range(int(rng.integers(1,4))):
                i,j=rng.choice(20,size=2,replace=False)
                x0[i],x0[j]=x0[j],x0[i]
        elif mode==5:
            x0=warm_x.copy()
            for _ in range(int(rng.integers(1,6))):
                i=int(rng.integers(20));j=int(np.clip(i+rng.integers(-3,4),0,19))
                amount=x0[i]*rng.uniform(.2,.9)
                x0[i]-=amount;x0[j]+=amount
        elif mode==6:
            x0=np.roll(warm_x,int(rng.choice([-3,-2,-1,1,2,3])))
        elif mode==7:
            x0=rng.dirichlet(np.full(20,rng.uniform(.07,.4)))
        elif mode==8:
            support=rng.choice(20,size=int(rng.integers(3,19)),replace=False)
            x0=np.zeros(20);x0[support]=rng.dirichlet(np.ones(len(support)))
        else:
            x0=rng.dirichlet(np.full(20,rng.uniform(.5,4)))
        if x0.sum()<=1e-15:
            x0=warm_x.copy()
        x0/=x0.sum()
        restarts+=1
        z0=np.r_[x0,np.max(np.convolve(x0,x0))+1e-10]
        def callback(z):
            consider(z[:20])
            if time.monotonic()>=deadline:
                raise TimeoutError
        try:
            result=minimize(fun,z0,jac=grad,method="SLSQP",
                bounds=[(0,1)]*20+[(1e-5,1)],
                constraints=[{"type":"eq","fun":lambda z:z[:20].sum()-1,
                    "jac":lambda z:np.r_[np.ones(20),0]},
                    {"type":"ineq","fun":ineq,"jac":ineq_jac}],
                callback=callback,options={"maxiter":300,"ftol":2e-13})
            consider(result.x[:20])
        except TimeoutError:
            break
        except (ValueError,FloatingPointError,OverflowError):
            continue
    return {"coefficients":[str(v) for v in best], "search_metadata":{
        "restarts":restarts,"budget_seconds":budget,"method":"smooth epigraph quotient SLSQP with sparse-support changes and analytic derivatives"}}
