"""Independent cycle-space dimension and straight-line planarity audit."""
from mathbench.registry import ROOT
import json
from scripts.audits.convex_cover_audit import meets, on


def audit(s):
    raw=json.loads((ROOT/'tasks/t095/data/source/uniform-0000500-1.instance.json').read_text())
    points=[]
    for i,p in enumerate(raw['points']):
        assert p['i']==i and int(p['x'])==p['x'] and int(p['y'])==p['y']
        points.append((int(p['x']),int(p['y'])))
    assert len(points)==len(set(points))==500
    edges=[tuple(sorted((e['i'],e['j']))) for e in s['edges']]
    assert len(edges)==len(set(edges)) and all(type(a) is int and type(b) is int and 0<=a<b<500 for a,b in edges)
    parents=list(range(500));cycles=0
    def find(a):
        while parents[a]!=a:parents[a]=parents[parents[a]];a=parents[a]
        return a
    for i,(a,b) in enumerate(edges):
        u,v=find(a),find(b)
        if u==v:cycles+=1
        else:parents[u]=v
        for j,p in enumerate(points):
            if j not in (a,b):assert not on(points[a],points[b],p)
        for c,d in edges[:i]:
            if {a,b}&{c,d}:continue
            assert not meets(points[a],points[b],points[c],points[d])
    assert len({find(i) for i in range(500)})==1
    # For a connected plane graph, the dimension of the cycle space is the
    # number of bounded faces. This counts redundant union-find joins rather
    # than traversing directed face boundaries as the formal checker does.
    return {'face_count':cycles,'point_count':500,'edge_count':len(edges),'method':'Exact straight-line planarity and point-on-edge checks; union-find fundamental cycle-space dimension, independent of formal geometric face walks.'}
