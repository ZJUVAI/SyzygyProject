"""Sol's Fraction-based planar-mesh audit, separate from the scaled-integer checker."""
import json,itertools
from fractions import Fraction as F
from functools import cmp_to_key
from mathbench.registry import ROOT


def audit(s):
    path=ROOT/'tasks/t064/data/source/ortho40.instance.json'
    instance=json.loads(path.read_text())
    p=list(zip(map(F,instance['points_x']),map(F,instance['points_y'])))+list(zip(map(F,s['steiner_points_x']),map(F,s['steiner_points_y'])))
    assert len(p)==len(set(p))==40+len(s['steiner_points_x'])
    edges={tuple(sorted(e)) for e in s['edges']};assert len(edges)==len(s['edges'])
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def on(a,b,c):return cross(a,b,c)==0 and min(a[0],b[0])<=c[0]<=max(a[0],b[0]) and min(a[1],b[1])<=c[1]<=max(a[1],b[1])
    for (u,v),(w,z) in itertools.combinations(edges,2):
     a,c,d,e=p[u],p[v],p[w],p[z]
     shared={u,v}&{w,z}
     if shared:
      joint=next(iter(shared));other1=next(iter({u,v}-{joint}));other2=next(iter({w,z}-{joint}));assert not on(p[joint],p[other1],p[other2]) and not on(p[joint],p[other2],p[other1]);continue
     assert not any((on(a,c,d),on(a,c,e),on(d,e,a),on(d,e,c)))
     assert not(cross(a,c,d)*cross(a,c,e)<0 and cross(d,e,a)*cross(d,e,c)<0)
    adj=[[] for _ in p]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    reached={0};todo=[0]
    while todo:
     for v in adj[todo.pop()]:
      if v not in reached:reached.add(v);todo.append(v)
    assert len(reached)==len(p)
    def compare(center,u,v):
     x,y=p[u][0]-p[center][0],p[u][1]-p[center][1];a,c=p[v][0]-p[center][0],p[v][1]-p[center][1]
     h1=int(y<0 or y==0 and x<0);h2=int(c<0 or c==0 and a<0)
     if h1!=h2:return h1-h2
     determinant=x*c-y*a
     assert determinant
     return -1 if determinant>0 else 1
    for u in range(len(p)):adj[u].sort(key=cmp_to_key(lambda a,c:compare(u,a,c)))
    seen=set();faces=[]
    for edge in itertools.chain(edges,((v,u) for u,v in edges)):
     if edge in seen:continue
     current=edge;face=[]
     while current not in seen:
      seen.add(current);u,v=current;face.append(u);current=(v,adj[v][(adj[v].index(u)-1)%len(adj[v])])
     assert current==edge
     area=sum(p[u][0]*p[v][1]-p[v][0]*p[u][1] for u,v in zip(face,face[1:]+face[:1]))
     if area>0:
      assert len(face)==3
      for i,j,k in ((0,1,2),(1,0,2),(2,0,1)):
       a,c,d=(p[face[x]] for x in (i,j,k));assert sum((x-z)*(y-z) for x,y,z in zip(c,d,a))>=0
      faces.append((face,area))
    poly=instance['region_boundary'];area=sum(p[u][0]*p[v][1]-p[v][0]*p[u][1] for u,v in zip(poly,poly[1:]+poly[:1]));assert sum(a for _,a in faces)==abs(area)

    for u,v in zip(poly,poly[1:]+poly[:1]):
     a,c=p[u],p[v];axis=0 if a[0]!=c[0] else 1
     intervals=[]
     for w,z in edges:
      if on(a,c,p[w]) and on(a,c,p[z]):
       intervals.append(tuple(sorted(((p[w][axis]-a[axis])/(c[axis]-a[axis]),(p[z][axis]-a[axis])/(c[axis]-a[axis])))))
     intervals.sort();endpoint=F(0)
     for left,right in intervals:assert left==endpoint;endpoint=right
     assert endpoint==1
    return {'steiner_count':len(p)-40,'triangles':len(faces),'edges':len(edges),'exact_doubled_area':str(abs(area))}
