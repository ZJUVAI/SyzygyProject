"""Exact checker for the ring loading problem."""
from fractions import Fraction
from itertools import product
from math import lcm

CONFIG_ID="T084-C01"
PARAMETERS={"m":15}

def _frac(value):
    if type(value) is int: return Fraction(value)
    if type(value) is str:
        try: return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc: raise ValueError("invalid rational string") from exc
    raise ValueError("pair entries must be integers or rational strings")

def validate(solution, config=None, strict=False):
    del strict
    if (type(config) is not dict or type(config.get("id")) is not str or config["id"] != CONFIG_ID
        or type(config.get("parameters")) is not dict or config["parameters"] != PARAMETERS
        or type(config.get("direction")) is not str or config["direction"] != "maximize"):
        raise ValueError("configuration does not match frozen T084-C01")
    if type(solution) is not dict or type(solution.get("pairs")) is not list or len(solution["pairs"]) != 15:
        raise ValueError("solution must contain exactly 15 pairs")
    pairs=[]; denominator=1
    for pair in solution["pairs"]:
        if type(pair) is not list or len(pair)!=2: raise ValueError("each pair must have two entries")
        u,v=map(_frac,pair)
        if u<0 or v<0 or u+v>1: raise ValueError("pairs must satisfy u,v >= 0 and u+v <= 1")
        pairs.append((u,v)); denominator=lcm(denominator,u.denominator,v.denominator)
    scaled=[(int(u*denominator),int(v*denominator)) for u,v in pairs]
    best=None
    for choices in product((0,1),repeat=15):
        z=[scaled[i][1] if choices[i]==0 else -scaled[i][0] for i in range(15)]
        total=sum(z); prefix=0; route=0
        for k in range(1,16):
            prefix+=z[k-1]
            route=max(route,abs(prefix-(total-prefix)))
        if best is None or route<best: best=route
    score=Fraction(best,denominator)
    return {"objective":str(score),"verification_status":"exact","details":{"routes":32768,"cuts_per_route":15}}
