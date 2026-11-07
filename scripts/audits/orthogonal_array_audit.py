"""Independent array proof by row-space completeness and projection ranks."""
from collections import Counter
from itertools import combinations
from math import comb


def audit(s):
    rows=s['rows'];assert rows and all(type(v)is int and 0<=v<1<<63 for v in rows)
    n=len(rows);assert n%16==0 and n>=2032
    multiplicities=Counter(rows);pivots={}
    for original in multiplicities:
        v=original
        while v:
            k=v.bit_length()-1
            if k not in pivots:pivots[k]=v;break
            v^=pivots[k]
    basis=list(pivots.values());dimension=len(basis)
    if len(multiplicities)==1<<dimension and len(set(multiplicities.values()))==1:
        # Every distinct submitted row lies in this span, whose cardinality
        # equals the submitted distinct-row count. Thus the whole span is
        # present, with the same multiplicity at every point.
        columns=[sum(((b>>j)&1)<<i for i,b in enumerate(basis)) for j in range(63)]
        checked=0
        for i,j,k in combinations(range(63),3):
            a,b,c=columns[i],columns[j],columns[k]
            assert a and b and a!=b and c not in (0,a,b,a^b)
            span={0,a,b,c,a^b,a^c,b^c,a^b^c}
            for d in columns[k+1:]:
                assert d not in span
                checked+=1
        assert checked==comb(63,4)
        method='Exact completeness of the submitted binary linear row space, equal multiplicities, and independent rank4 of all four-column projections. Surjective linear projections give every pattern N/16 times; no parity-character row counts are reused.'
    else:
        # Direct16-pattern fallback covers general nonlinear candidate arrays.
        cols=[sum(((v>>j)&1)<<i for i,v in enumerate(rows)) for j in range(63)];mask=(1<<n)-1;checked=0
        for i,j,k in combinations(range(63),3):
            patterns=[mask]
            for col in (cols[i],cols[j],cols[k]):
                patterns=[part&choice for part in patterns for choice in (col,mask^col)]
            assert all(v.bit_count()==n//8 for v in patterns)
            for col in cols[k+1:]:
                assert all((v&col).bit_count()==n//16 and (v&(mask^col)).bit_count()==n//16 for v in patterns)
                checked+=1
        method='Direct exact intersections count all16patterns on every four-column projection, independently of formal XOR characters.'
    return {'row_count':n,'distinct_rows':len(multiplicities),'linear_span_dimension':dimension,'four_column_projections':checked,'rao_lower_bound':2032,'method':method}
