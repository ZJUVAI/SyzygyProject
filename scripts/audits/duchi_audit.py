"""Independent symbolic matrix products and rational root enclosures."""
import itertools
import math
from fractions import Fraction as F
import sympy as sp


def audit(solution):
    matrices=[sp.Matrix([[sp.Rational(v[0])+sp.I*sp.Rational(v[1]) for v in row] for row in a]) for a in solution['matrices']]
    assert len(matrices)==4 and all(a.shape==(3,3) and a==a.H for a in matrices)
    for a in matrices:
        for k in range(1,4):
            for ix in itertools.combinations(range(3),k):assert a.extract(ix,ix).det()>=0
    def norm_squared(ix):
        m=sp.eye(3)
        for j in ix:m=m*matrices[j]
        return F(sp.expand(sp.trace(m.H*m)))
    wr=[norm_squared(ix) for ix in itertools.product(range(4),repeat=4)]
    wo=[norm_squared(ix) for ix in itertools.permutations(range(4))]
    assert any(wo)
    if len(set(wr+wo))==1:
        interval=(F(1),F(1))
    else:
        nonzero=min(x for x in wr+wo if x>0)
        scale=10**50*max(1,math.isqrt(nonzero.denominator//nonzero.numerator)+1)
        def root(v):
            a=math.isqrt(v.numerator*scale*scale//v.denominator)
            lo=F(a,scale)
            return lo,lo if lo*lo==v else F(a+1,scale)
        wl,wh=map(sum,zip(*(root(x) for x in wr)))
        dl,dh=map(sum,zip(*(root(x) for x in wo)))
        assert dl>0
        interval=(F(3,32)*wl/dh,F(3,32)*wh/dl)
    return {'ratio_interval':list(map(str,interval)),'with_replacement_products':len(wr),'without_replacement_products':len(wo),'squared_norms_verified':280,'method':'SymPy complex matrices and trace(M.H*M); independent exact product norms and finer rational root enclosures'}
