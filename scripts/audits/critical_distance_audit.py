"""Independent exact real-root Sturm audit for saved critical-distance witnesses."""
from fractions import Fraction as F
import sympy as sp


def audit_real(solution):
    x=sp.Symbol('x');poly=sp.Poly(1,x);roots=[]
    for entry in solution['roots']:
        a,b=map(F,entry['root']);assert b==0,'This independent audit covers saved real-root witnesses only.'
        m=entry['multiplicity'];roots.extend([a]*m);poly*=sp.Poly(x-sp.Rational(a.numerator,a.denominator),x)**m
    assert len(roots)==8 and sum(map(abs,roots))<=8
    derivative=poly.diff();isolated=derivative.intervals(eps=sp.Rational(1,10**65))
    assert sum(m for _,m in isolated)==7
    critical=[(F(a),F(b)) for (a,b),m in isolated]
    lower=F(0);upper=F(0)
    for r in roots:
        ds=[(max(a-r,r-b,F(0)),max(abs(a-r),abs(b-r))) for a,b in critical]
        lower=max(lower,min(a for a,b in ds));upper=max(upper,min(b for a,b in ds))
    return {'ratio_interval':[str(lower),str(upper)],'polynomial_coefficients':[str(c) for c in poly.all_coeffs()],'critical_intervals':[[str(a),str(b)] for a,b in critical],'method':'Exact polynomial reconstruction, derivative factorization and Sturm real-root isolation; no claimed critical disks used.'}
