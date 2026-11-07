"""Independent row-interval certificate for P1 rectangle tilings."""
from mathbench.registry import ROOT
import json


def audit(solution):
    raw=json.loads((ROOT/'tasks/t099/data/source/11P1.json').read_text())
    shape=[tuple(v) for v in raw['cells']]
    expected={(x,0) for x in range(5)}|{(x,y) for x in range(3) for y in (1,2)}
    assert len(shape)==11 and set(shape)==expected
    W,H=(solution['width'],solution['height']) if 'width' in solution else solution['rectangle'];assert type(W)is int and type(H)is int and min(W,H)>0
    pieces=solution['placements'];assert len(pieces)*11==W*H
    # Gaussian-integer units, optionally conjugated. These are independent
    # of the formal checker's three-bit swap/sign implementation.
    transforms=[(1,0,False),(0,1,True),(-1,0,True),(0,1,False),(1,0,True),(0,-1,False),(-1,0,False),(0,-1,True)]
    rows={}
    for piece in pieces:
        o,X,Y=piece['orientation'],piece['x'],piece['y']
        assert all(type(v)is int for v in (o,X,Y)) and 0<=o<8
        a,b,conjugate=transforms[o];transformed=[]
        for x,y in shape:
            if conjugate:y=-y
            transformed.append((a*x-b*y,b*x+a*y))
        mx=min(x for x,y in transformed);my=min(y for x,y in transformed)
        tile_rows={}
        for x,y in transformed:
            xx,yy=X+x-mx,Y+y-my
            assert 0<=xx<W and 0<=yy<H
            tile_rows.setdefault(yy,[]).append(xx)
        for y,xs in tile_rows.items():
            xs.sort();assert xs==list(range(xs[0],xs[-1]+1))
            rows.setdefault(y,[]).append((xs[0],xs[-1]+1))
    assert len(rows)==H
    interval_count=0
    for intervals in rows.values():
        end=0
        for a,b in sorted(intervals):
            assert a==end;end=b;interval_count+=1
        assert end==W
    return {'tile_count':len(pieces),'rectangle':[W,H],'covered_area':W*H,'row_intervals':interval_count,
        'method':'Independent Gaussian-integer D4 transformations and complete sorted row-interval partitions; all gaps and overlaps excluded by exact integer endpoints.'}
