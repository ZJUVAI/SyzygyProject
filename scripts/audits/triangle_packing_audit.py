"""Independent symbolic audit of four equilateral triangles."""
import itertools
import sympy as sp


def audit(solution):
    r=sp.sqrt(3)
    def number(v):
        return sp.Rational(v[0])+sp.Rational(v[1])*r
    L=number(solution['side']);assert L>0
    triangles=[]
    for record in solution['triangles']:
        x,y=map(number,record['anchor']);u,v=map(sp.Rational,record['direction'])
        t=[(x,y),(x+u,y+v),(x+(u-r*v)/2,y+(v+r*u)/2)]
        for a,b in itertools.combinations(t,2):assert sp.expand(sum((z-w)**2 for z,w in zip(a,b)))==1
        assert all(sp.sign(sp.expand(z))>=0 and sp.sign(sp.expand(L-z))>=0 for p in t for z in p)
        triangles.append(t)
    assert len(triangles)==4
    # Intersection clipping uses exact orientations, not the formal projection test.
    def cross(a,b,c):return sp.expand((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
    for a,b in itertools.combinations(triangles,2):
        poly=a[:]
        for p,q in zip(b,b[1:]+b[:1]):
            out=[]
            for x,y in zip(poly,poly[1:]+poly[:1]):
                cx,cy=cross(p,q,x),cross(p,q,y)
                ix,iy=sp.sign(cx)>=0,sp.sign(cy)>=0
                if ix:out.append(x)
                if ix!=iy:
                    alpha=sp.cancel(cx/(cx-cy));out.append(tuple(sp.simplify(xi+alpha*(yi-xi)) for xi,yi in zip(x,y)))
            poly=out
            if not poly:break
        area=sp.expand(sum(x[0]*y[1]-x[1]*y[0] for x,y in zip(poly,poly[1:]+poly[:1])))
        assert sp.simplify(area)==0
    return {'exact_side':str(L),'unit_sides_checked':12,'pairs_checked':6,'method':'SymPy algebraic expressions; exact polygon clipping and intersection area, independent of formal ordered-field separating axes'}
