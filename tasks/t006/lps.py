"""Explicit LPS graph X^(5,37), with two generator matchings removed."""
from collections import deque

Q=37
I=6  # I^2 = -1 modulo 37.

def _norm(m):
    for x in m:
        if x % Q:
            inv=pow(x,-1,Q)
            return tuple((y*inv)%Q for y in m)
    raise ValueError('zero matrix')


def _mul(a,b):
    a00,a01,a10,a11=a; b00,b01,b10,b11=b
    return _norm(((a00*b00+a01*b10)%Q,(a00*b01+a01*b11)%Q,
                  (a10*b00+a11*b10)%Q,(a10*b01+a11*b11)%Q))


def _generators():
    out=[]
    for axis in range(3):
        for sign in (1,-1):
            v=[0,0,0]; v[axis]=2*sign
            a1,a2,a3=v; a0=1
            out.append(_norm(((a0+I*a1)%Q,(a2+I*a3)%Q,
                              (-a2+I*a3)%Q,(a0-I*a1)%Q)))
    return out


def _det_character(m):
    a,b,c,d=m
    det=(a*d-b*c)%Q
    return pow(det,18,Q)


def build_graph(drop=(0,2)):
    """Build a connected 4-regular graph by deleting two 1-factors."""
    gens=_generators()
    identity=(1,0,0,1)
    vertices=[identity]; index={identity:0}; queue=deque([0]); transitions=[]
    while queue:
        u=queue.popleft(); m=vertices[u]; row=[]
        for g in gens:
            z=_mul(m,g)
            v=index.get(z)
            if v is None:
                v=len(vertices); index[z]=v; vertices.append(z); queue.append(v)
            row.append(v)
        transitions.append(row)
    n=len(vertices)
    if n != Q*(Q*Q-1):
        raise ValueError(f'unexpected generated group order {n}')
    # Each generator maps one bipartition class bijectively to the other.
    left=[_det_character(m)==1 for m in vertices]
    # The chosen indices must come from distinct inverse pairs (0,1),(2,3),(4,5).
    removed=set()
    for u in range(n):
        if left[u]:
            for gi in drop:
                v=transitions[u][gi]
                removed.add((min(u,v),max(u,v)))
    edges=set()
    for u,row in enumerate(transitions):
        for v in row:
            e=(min(u,v),max(u,v))
            if e not in removed:
                edges.add(e)
    return {'vertices':n,'edges':[list(e) for e in sorted(edges)]}
