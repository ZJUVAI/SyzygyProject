"""Independent exact vertical-section test for polygon-packing witnesses."""
from fractions import Fraction as F
from collections import Counter
import json
from mathbench.registry import ROOT


def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def sections(poly,x):
    ys=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if min(a[0],b[0])<x<max(a[0],b[0]):
            ys.append(a[1]+(x-a[0])*F(b[1]-a[1],b[0]-a[0]))
    ys.sort();assert len(ys)%2==0
    return list(zip(ys[::2],ys[1::2]))


def disjoint_interiors(p,q):
    # Vertex x values and every edge crossing partition the arrangement into
    # slabs. In one open slab the order of all boundary lines cannot change.
    cuts={F(a[0]) for a in p+q}
    for a,b in zip(p,p[1:]+p[:1]):
        u=(b[0]-a[0],b[1]-a[1])
        for c,d in zip(q,q[1:]+q[:1]):
            v=(d[0]-c[0],d[1]-c[1]);den=u[0]*v[1]-u[1]*v[0]
            if den:
                w=(c[0]-a[0],c[1]-a[1]);t=F(w[0]*v[1]-w[1]*v[0],den);s=F(w[0]*u[1]-w[1]*u[0],den)
                if 0<=t<=1 and 0<=s<=1:cuts.add(a[0]+t*u[0])
    xs=sorted(cuts)
    for l,r in zip(xs,xs[1:]):
        x=(l+r)/2
        for a,b in sections(p,x):
            for c,d in sections(q,x):
                assert min(b,d)<=max(a,c),'positive-area overlap'


def audit(solution):
    path=ROOT/'tasks/t093/data/source/random_cf2_74ae2d30_50.cgshop2024_instance.json'
    data=json.loads(path.read_text());container=list(zip(data['container']['x'],data['container']['y']))
    signs=[cross(container[i-1],container[i],container[(i+1)%len(container)]) for i in range(len(container))]
    assert all(s>=0 for s in signs) or all(s<=0 for s in signs)
    orientation=1 if sum(signs)>0 else -1
    counts=Counter();placed=[];value=0
    ids=solution['item_indices'];xs=solution['x_translations'];ys=solution['y_translations'];assert len(ids)==len(xs)==len(ys)
    for idx,dx,dy in zip(ids,xs,ys):
        assert all(type(v) is int for v in (idx,dx,dy)) and 0<=idx<len(data['items'])
        item=data['items'][idx];counts[idx]+=1;assert counts[idx]<=item['quantity']
        p=[(x+dx,y+dy) for x,y in zip(item['x'],item['y'])]
        for a,b in zip(container,container[1:]+container[:1]):
            assert all(orientation*cross(a,b,v)>=0 for v in p),'outside convex container'
        for q in placed:disjoint_interiors(p,q)
        placed.append(p);value+=item['value']
    return {'packed_value':value,'placed_items':len(placed),'method':'Exact rational vertical sections in all arrangement slabs; convex-container halfplanes; no triangulation or triangle clipping.'}
