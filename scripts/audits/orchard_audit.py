"""Sol's independent saved-orchard audit: rational determinants or cubic group law."""
import itertools
import math
from fractions import Fraction


def audit(solution):
    raw=solution['points'];assert len(raw)==17
    if solution['minimal_polynomial']==[0,1]:
        points=[]
        for p in raw:
            assert len(p['x'])==len(p['y'])==1
            points.append((Fraction(p['x'][0]),Fraction(p['y'][0])))
        assert len(set(points))==17
        lines=set()
        for i,j in itertools.combinations(range(17),2):
            a,b=points[i],points[j]
            mask=tuple(k for k,c in enumerate(points) if (b[0]-a[0])*(c[1]-a[1])==(b[1]-a[1])*(c[0]-a[0]))
            if len(mask)==3:lines.add(mask)
        return {'three_point_lines':len(lines),'method':'independent rational determinant incidence sets'}
    import sympy as sp
    x=sp.Symbol('x')
    coefficients=[(-1)**j*math.comb(17,2*j+1) for j in range(9)]
    expected=[0]*17
    for j,c in enumerate(coefficients):expected[2*j]=c
    assert solution['minimal_polynomial']==expected
    modulus=sp.Poly.from_list(expected[::-1],x,domain=sp.QQ)
    assert modulus.is_irreducible
    zero=sp.Poly(0,x,domain=sp.QQ);one=sp.Poly(1,x,domain=sp.QQ);alpha=sp.Poly(x,x,domain=sp.QQ)
    tangent=zero;seen=set()
    def parse(a):return sp.Poly.from_list([sp.Rational(str(c)) for c in a[::-1]],x,domain=sp.QQ).rem(modulus)
    for point in raw:
        u,v=parse(point['x']),parse(point['y']);assert u==tangent
        assert (v*(one+u*u)-u*u*u).rem(modulus).is_zero
        key=tuple(u.all_coeffs());assert key not in seen;seen.add(key)
        denominator=(one-alpha*tangent).rem(modulus);assert not denominator.is_zero
        tangent=((tangent+alpha)*sp.invert(denominator,modulus)).rem(modulus)
    assert tangent.is_zero
    triples=[t for t in itertools.combinations(range(17),3) if sum(t)%17==0]
    # Cubic y(1+x^2)-x^3 has no line component. Each line has at most three points.
    # The determinant numerator is Vandermonde times (abc-a-b-c); tangent addition gives the index rule.
    assert len(triples)==40
    return {'three_point_lines':40,'method':'exact cubic coordinates, tangent group order17 and index-sum incidence','group_order':17,'no_four_collinear':'irreducible cubic has no line component'}
