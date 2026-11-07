"""Independent strip-cover and boundary-cut audit of simple perfect squared squares."""
from math import gcd
from functools import reduce


def audit(s):
    tiles=[tuple(q) for q in s['squares']];assert len(tiles)==38
    assert all(len(q)==3 and all(type(v) is int for v in q) and q[2]>0 for q in tiles)
    S=max(x+a for x,y,a in tiles);assert S==max(y+a for x,y,a in tiles)==s['side']
    assert all(0<=x<x+a<=S and 0<=y<y+a<=S for x,y,a in tiles)
    sizes=[a for x,y,a in tiles];assert len(set(sizes))==38 and reduce(gcd,sizes)==1
    xs=sorted({v for x,y,a in tiles for v in (x,x+a)});ys=sorted({v for x,y,a in tiles for v in (y,y+a)})
    assert xs[0]==ys[0]==0
    for l,r in zip(xs,xs[1:]):
        intervals=sorted((y,y+a) for x,y,a in tiles if 2*x<l+r<2*(x+a))
        end=0
        for a,b in intervals:assert a==end;end=b
        assert end==S
    assert sum(a*a for a in sizes)==S*S
    checked=0
    # Any rectangular subdissection has x/y boundaries on tile edges. For a
    # fixed x-band, eligible whole tiles fill a y-slab exactly when their
    # disjoint horizontal section lengths sum to the band width. At the two
    # horizontal cuts no eligible tile may cross. This is a length/cut proof,
    # independent of the formal contained-area mask enumeration.
    for i,l in enumerate(xs):
        for r in xs[i+1:]:
            eligible=[q for q in tiles if l<=q[0] and q[0]+q[2]<=r]
            if len(eligible)<2:continue
            bad=[0]
            for a,b in zip(ys,ys[1:]):
                width=sum(z for x,y,z in eligible if 2*y<a+b<2*(y+z))
                bad.append(bad[-1]+(width!=r-l))
            cuts=[i for i,v in enumerate(ys) if not any(y<v<y+a for x,y,a in eligible)]
            for p,a in enumerate(cuts):
                for b in cuts[p+1:]:
                    checked+=1
                    if bad[a]!=bad[b]:continue
                    count=sum(ys[a]<=y and y+z<=ys[b] for x,y,z in eligible)
                    if count<2:continue
                    assert (l,r,ys[a],ys[b])==(0,S,0,S),'proper rectangular subdissection'
    return {'outer_side':S,'area_sum':sum(a*a for a in sizes),'order':38,'primitive_gcd':reduce(gcd,sizes),'cut_rectangles_checked':checked,'method':'Exact full vertical-section coverage and horizontal-length/cut certificates for every candidate rectangle; distinct sizes and primitive gcd independently checked.'}
