"""Independent exact complement-area proof for eight-square coverings."""
from fractions import Fraction as F


def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]


def clip(poly,p,q,keep_inside):
    edge=(q[0]-p[0],q[1]-p[1])
    def value(x):
        v=cross(edge,(x[0]-p[0],x[1]-p[1]))
        return v if keep_inside else -v
    result=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        va,vb=value(a),value(b)
        if va>=0:result.append(a)
        if (va<0<vb) or (vb<0<va):
            t=va/(va-vb)
            result.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
    return result


def area(poly):
    return abs(sum((cross(a,b) for a,b in zip(poly,poly[1:]+poly[:1])),F(0)))/2


def audit(s):
    side=F(s['side']);assert side>0 and len(s['squares'])==8
    h=side/2
    pieces=[[(-h,-h),(h,-h),(h,h),(-h,h)]]
    for record in s['squares']:
        x,y=map(F,record['center']);a,b=map(F,record['direction']);assert a*a+b*b==1
        polygon=[(x+(se*a-sf*b)/2,y+(se*b+sf*a)/2) for se,sf in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        uncovered=[]
        for poly in pieces:
            rest=poly
            for p,q in zip(polygon,polygon[1:]+polygon[:1]):
                if not rest:break
                out=clip(rest,p,q,False)
                if len(out)>=3 and area(out)>0:uncovered.append(out)
                rest=clip(rest,p,q,True)
        pieces=uncovered
    uncovered_area=sum(map(area,pieces),F(0));assert uncovered_area==0
    # A finite union of closed squares is closed. Any missing point of a
    # positive-area target square would leave a positive-area relative open
    # neighbourhood. Thus zero complement area proves full coverage.
    return {'target_square_side':str(side),'uncovered_area':str(uncovered_area),'method':'Exact rational convex clipping of target complement by every square; closedness turns zero uncovered area into full coverage. Independent of vertical arrangement sweep.'}
