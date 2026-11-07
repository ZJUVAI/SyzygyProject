"""Independent rational convex-cover proof by diagonal subdivision and complements."""
from fractions import Fraction as F
from scripts.audits.square_cover_audit import clip, area, cross


def turn(a,b,c):return cross((b[0]-a[0],b[1]-a[1]),(c[0]-a[0],c[1]-a[1]))


def on(a,b,c):return turn(a,b,c)==0 and min(a[0],b[0])<=c[0]<=max(a[0],b[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])


def meets(a,b,c,d):
    v,w,x,y=turn(a,b,c),turn(a,b,d),turn(c,d,a),turn(c,d,b)
    return (v*w<0 and x*y<0) or any((v==0 and on(a,b,c),w==0 and on(a,b,d),x==0 and on(c,d,a),y==0 and on(c,d,b)))


def inside(poly,p):
    count=0
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if on(a,b,p):return True
        if (a[1]>p[1])!=(b[1]>p[1]):
            hit=a[0]+(p[1]-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if hit>p[0]:count+=1
    return count%2==1


def triangulate(p):
    p=list(p)
    # Remove only boundary points strictly between their two neighbours.
    again=True
    while again and len(p)>3:
        again=False
        for i in range(len(p)):
            if on(p[i-1],p[(i+1)%len(p)],p[i]):p.pop(i);again=True;break
    assert area(p)>0
    signed=sum(cross(a,b) for a,b in zip(p,p[1:]+p[:1]))
    if signed<0:p.reverse()
    if len(p)==3:return [p]
    n=len(p)
    for gap in range(2,n-1):
        for i in range(n-gap):
            j=i+gap;a,b=p[i],p[j]
            if any(on(a,b,c) for k,c in enumerate(p) if k not in (i,j)):continue
            if any(meets(a,b,p[k],p[(k+1)%n]) for k in range(n) if not {i,j}&{k,(k+1)%n}):continue
            midpoint=((a[0]+b[0])/2,(a[1]+b[1])/2)
            if not inside(p,midpoint):continue
            left=triangulate(p[i:j+1]);right=triangulate(p[j:]+p[:i+1])
            assert sum(map(area,left+right),F(0))==area(p)
            return left+right
    raise AssertionError('No interior diagonal found')


def audit_polygons(polygon,covers):
    p=[tuple(map(F,v)) for v in polygon];n=len(p)
    assert len(set(p))==n
    for i in range(n):
        for j in range(i+1,n):
            if {i,(i+1)%n}&{j,(j+1)%n}:continue
            assert not meets(p[i],p[(i+1)%n],p[j],p[(j+1)%n])
    triangles=triangulate(p);normalized=[]
    for raw in covers:
        q=[tuple(map(F,v)) for v in raw];assert len(q)>=3 and area(q)>0 and len(set(q))==len(q)
        signed=sum(cross(a,b) for a,b in zip(q,q[1:]+q[:1]))
        if signed<0:q.reverse()
        assert all(turn(a,b,v)>=0 for a,b in zip(q,q[1:]+q[:1]) for v in q)
        total=F(0)
        for tri in triangles:
            part=q
            for a,b in zip(tri,tri[1:]+tri[:1]):part=clip(part,a,b,True)
            total+=area(part)
        assert total==area(q),'Cover protrudes outside target'
        normalized.append(q)
    complement=triangles
    for q in normalized:
        new=[]
        for p in complement:
            rest=p
            for a,b in zip(q,q[1:]+q[:1]):
                if not rest:break
                outside=clip(rest,a,b,False)
                if len(outside)>=3 and area(outside)>0:new.append(outside)
                rest=clip(rest,a,b,True)
        complement=new
    uncovered=sum(map(area,complement),F(0));assert uncovered==0
    return {'polygon_count':len(covers),'target_area':str(sum(map(area,triangles),F(0))),'uncovered_area':str(uncovered),'method':'Independent rational recursive interior diagonals, full cover containment areas, and iterative convex-complement clipping; closedness proves pointwise coverage.'}
