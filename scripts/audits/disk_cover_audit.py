"""Independent exact certificates for saved disk coverings."""
from fractions import Fraction as F
import itertools
from math import lcm


def _audit_boxes(centers, radius):
    """Cover an exact dyadic subdivision of the target bounding box."""
    depth_limit = 42
    scale = lcm(radius.denominator, *(v.denominator for p in centers for v in p)) * 2**depth_limit
    sites = [tuple(int(scale * v) for v in p) for p in centers]
    edge = int(scale * radius)
    stack = [(-edge, edge, -edge, edge, 0)]
    count = 0
    while stack:
        x0, x1, y0, y1, depth = stack.pop()
        count += 1
        assert count <= 2_000_000
        near_x = max(x0, 0, -x1)
        near_y = max(y0, 0, -y1)
        if near_x**2 + near_y**2 > edge**2:
            continue
        if any(max(abs(x0-u), abs(x1-u))**2 + max(abs(y0-v), abs(y1-v))**2 <= scale**2
               for u,v in sites):
            continue
        assert depth < depth_limit, 'Dyadic audit could not certify a boundary box'
        x, y = (x0+x1)//2, (y0+y1)//2
        stack.extend((a, b, c, d, depth+1) for a,b in ((x0,x),(x,x1)) for c,d in ((y0,y),(y,y1)))
    return count


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
        if sorted(centers)!=sorted(expected) or R>F(7,2):
            boxes=_audit_boxes(centers,R)
            return {'radius':str(R),'circle_count':21,'distinct_centers':len(set(centers)),
                    'boxes_checked':boxes,'method':'Exact dyadic subdivision; each retained box lies in one unit disk.'}
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
