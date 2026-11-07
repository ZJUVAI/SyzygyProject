"""Exact algebraic cosine chords and integer Floyd audit for regular 120-gons."""
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import sympy as sp


def mul(a,b):
    v=[a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1]];return min(v),max(v)


@lru_cache(None)
def chords():
    x=sp.Symbol('x');p=sp.Poly(x**16-16*x**14+105*x**12-364*x**10+714*x**8-784*x**6+440*x**4-96*x**2+1,x)
    roots=p.intervals(eps=sp.Rational(1,10**100));(lo,hi),_=roots[-1]
    a,b=F(lo),F(hi)
    # 2cos(pi/60) is the largest conjugate: all conjugates are 2cos(k*pi/60)
    # for k coprime to 120; k=1 gives the unique largest real value.
    assert F(199,100)<a<b<2
    old=sp.Poly(2,x);cur=sp.Poly(x,x);S=10**60;out={0:(0,0)}
    for k in range(1,61):
        if k>1:old,cur=cur,(sp.Poly(x,x)*cur-old).rem(p)
        interval=(F(0),F(0))
        for c in cur.all_coeffs():
            l,h=mul(interval,(a,b));interval=(l+F(c),h+F(c))
        l2,h2=2-interval[1],2-interval[0];assert l2>0
        l=isqrt(l2.numerator*S*S//l2.denominator);h=isqrt(h2.numerator*S*S//h2.denominator)
        if F(h,S)**2<h2:h+=1
        out[k]=(l,h)
    return out


def audit_edges(edges):
    n=120;E={tuple(sorted(e)) for e in edges};assert len(E)==len(edges)==237
    assert all(type(a) is int and type(b) is int and 0<=a<b<n for a,b in E)
    assert all(tuple(sorted((i,(i+1)%n))) in E for i in range(n))
    for a,b in E:
        for c,d in E:
            assert not (a<c<b<d or c<a<d<b),'crossing diagonals'
    C=chords();inf=10**100;L=[[inf]*n for _ in range(n)];H=[[inf]*n for _ in range(n)]
    for i in range(n):L[i][i]=H[i][i]=0
    for a,b in E:
        k=min(b-a,n-(b-a));l,h=C[k];L[a][b]=L[b][a]=l;H[a][b]=H[b][a]=h
    for D in (L,H):
        for k in range(n):
            row=D[k]
            for i in range(n):
                di=D[i];v=di[k]
                for j in range(n):
                    alt=v+row[j]
                    if alt<di[j]:di[j]=alt
    low=F(0);high=F(0)
    for i in range(n):
        for j in range(i+1,n):
            k=min(j-i,n-(j-i));l,h=C[k];low=max(low,F(L[i][j],h));high=max(high,F(H[i][j],l))
    return {'ratio_interval':[str(low),str(high)],'edges':len(E),'method':'Cyclotomic cosine minimal polynomial, exact rational Horner and square-root chord bounds, all-pairs integer Floyd-Warshall.'}
