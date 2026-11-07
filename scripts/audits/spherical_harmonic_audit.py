"""Independent iterated spherical-coordinate integration with integer products."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb, factorial, lcm, isqrt


@lru_cache(None)
def moment(a,b,c):
    if (a|b|c)&1:return F(0)
    a//=2;b//=2;c//=2
    azimuth=F(comb(2*a,a)*comb(2*b,b),4**(a+b)*comb(a+b,a))
    latitude=sum((F((-1)**j*comb(a+b,j),2*c+2*j+1) for j in range(a+b+1)),F(0))
    return azimuth*latitude


def square(poly):
    terms=list(poly.items());out={}
    for i,((a,b,c),v) in enumerate(terms):
        for j in range(i,len(terms)):
            (d,e,f),w=terms[j];key=(a+d,b+e,c+f)
            out[key]=out.get(key,0)+v*w*(1 if i==j else 2)
    return {k:v for k,v in out.items() if v}


@lru_cache(None)
def _audit(values):
    exps=[(a,b,20-a-b) for a in range(20,-1,-1) for b in range(20-a,-1,-1)]
    den=lcm(*(v.denominator for v in values));p={e:int(v*den) for e,v in zip(exps,values) if v}
    assert len(values)==231 and p
    lap={}
    for e,v in p.items():
        for j in range(3):
            if e[j]>=2:
                k=list(e);k[j]-=2;k=tuple(k);lap[k]=lap.get(k,0)+v*e[j]*(e[j]-1)
    assert not any(lap.values())
    p2=square(p);p4=square(p2)
    m2=sum((v*moment(*e) for e,v in p2.items()),F(0))/den**2
    m4=sum((v*moment(*e) for e,v in p4.items()),F(0))/den**4
    ratio=m4/m2**2;S=10**60;k=isqrt(isqrt(ratio.numerator*S**4//ratio.denominator))
    lo=F(k,S);hi=lo if lo**4==ratio else F(k+1,S)
    return {'ratio_interval':[str(lo),str(hi)],'M2':str(m2),'M4':str(m4),'fourth_power_ratio':str(ratio),'method':'Clear rational denominators, symmetric integer polynomial products, exact azimuth central-binomial integral and finite binomial latitude integral.'}


def audit(solution):
    return _audit(tuple(map(F,solution['coefficients'])))


def highest_weight_formula():
    B=lambda k:F(4**k*factorial(k)**2,factorial(2*k+1))
    return B(20)/2,3*B(40)/8
