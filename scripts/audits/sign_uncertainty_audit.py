"""Independent Fourier differentiation and odd-multiplicity tail-root audit."""
from fractions import Fraction as F
from math import isqrt
import sympy as sp


def audit(s):
    p=list(map(F,s['coefficients']));t=sp.Symbol('u')
    P=sp.Poly(sum(sp.Rational(v.numerator,v.denominator)*t**i for i,v in enumerate(p)),t)
    q=sp.Poly(0,t);mode=sp.Poly(1,t)
    for v in p:
        q+=sp.Rational(v.numerator,v.denominator)*mode
        mode=sp.Poly((sp.Rational(1,2)-t)*mode.as_expr()+(2*t-sp.Rational(1,2))*mode.diff().as_expr()-t*mode.diff().diff().as_expr(),t)
    assert P.eval(0)<0 and q.eval(0)<0 and P.LC()>0 and q.LC()>0
    def last_odd(poly):
        roots=[]
        for (lo,hi),mult in poly.intervals(eps=sp.Rational(1,10**55)):
            if mult%2 and lo>0:roots.append((F(int(lo.p),int(lo.q)),F(int(hi.p),int(hi.q)) ))
        assert roots
        return max(roots,key=lambda x:x[0])
    a,b=last_odd(P),last_odd(q)
    def atan(q,n):
        v=sum((F((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(n)),F(0))
        w=v+F((-1)**n,(2*n+1)*q**(2*n+1))
        return min(v,w),max(v,w)
    c,d=atan(5,90),atan(239,35);pi=(16*c[0]-4*d[1],16*c[1]-4*d[0])
    S=10**70
    def sqrt_bounds(v):
        z=isqrt(v.numerator*S*S//v.denominator)
        return F(z,S),F(z+(F(z,S)**2<v),S)
    lo=sqrt_bounds(a[0]*b[0])[0]/pi[1];hi=sqrt_bounds(a[1]*b[1])[1]/pi[0]
    return {'ratio_interval':[str(lo),str(hi)],'fourier_coefficients':[str(F(v)) for v in reversed(q.all_coeffs())],'p_tail_root':list(map(str,a)),'q_tail_root':list(map(str,b)),'method':'Fourier multiplication-by-pi*x^2 computed by differential recurrence on transformed Gaussian; final odd-multiplicity positive root, finer rational isolation and Machin bounds.'}
