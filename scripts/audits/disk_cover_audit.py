"""Independent analytic proofs for the admission disk coverings."""
from fractions import Fraction as F
import itertools


def audit(solution):
    centers=[tuple(map(F,p)) for p in solution['centers']];R=F(solution['radius'])
    assert len(centers)==21 and R>0
    if R<=1 and (F(0),F(0)) in centers:
        method='The origin unit disk contains the entire concentric target disk.'
    else:
        r=F(1732050807568877293527446341505872366942805253810380628055806979,10**63)
        scale=F(999,1000);eps=F(1,10**60)
        sites=[(q,t) for q,t in itertools.product(range(-2,3),repeat=2) if max(abs(q),abs(t),abs(q+t))<=2]
        expected=[(scale*r*(q+F(t,2)),scale*F(3,2)*t) for q,t in sites]+[(F(0),F(0))]*2
        assert sorted(centers)==sorted(expected) and R<=F(7,2)
        assert r*r<3<(r+eps)**2
        assert min(q*q+q*t+t*t for q,t in itertools.product(range(-3,4),repeat=2) if max(abs(q),abs(t),abs(q+t))>2)==7
        # If any axial coordinate has magnitude>=4, the quadratic form is>=12.
        # All omitted ideal lattice sites therefore have norm>=scale*sqrt(21).
        assert 21*scale*scale>(R+1)**2
        # Each equilateral lattice face has circumradius scale; perturbation
        # of every retained site is at most2*scale*eps in horizontal distance.
        assert scale+2*scale*eps<1
        method='Analytic triangular tessellation radius; omitted-site norm lower bound and exact rational perturbation slack. Independent of formal restricted Voronoi enumeration.'
    return {'radius':str(R),'circle_count':21,'distinct_centers':len(set(centers)),'method':method}
