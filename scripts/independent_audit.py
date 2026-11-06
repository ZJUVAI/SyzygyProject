"""Main-review cross-checks, separate from task checker implementations."""
import itertools
import json
import math
from fractions import Fraction as F



def independent_quantity(task, s, config=None):
    if task == "T001":
        p = [[F(x) for x in row] for row in s["centers"]]; r = F(s["radius"])
        margin = min((x-u)**2+(y-v)**2-4*r*r for (x,y),(u,v) in itertools.combinations(p,2))
        assert margin >= 0
        return {"radius": str(r), "smallest_squared_pair_margin": str(margin)}
    if task == "T002":
        import sympy as sp
        def q(x): return sp.sympify(str(x).replace('sqrt2','sqrt(2)'))
        xs, ys = [], []
        for p in s['squares']:
            x,y,t = (q(p[k]) for k in ('x','y','t'))
            c=(1-t*t)/(1+t*t); sn=2*t/(1+t*t)
            for a,b in itertools.product((-1,1),repeat=2):
                xs.append(sp.expand(x+(a*c-b*sn)/2)); ys.append(sp.expand(y+(a*sn+b*c)/2))
        side=max(sp.simplify(max(v)-min(v)) for v in (xs,ys))
        if config is None or config['id']=='T002-C01':
            assert sp.simplify(side-(7+3*sp.sqrt(2))/2)==0
        return {"bounding_side": str(side)}
    if task == "T005":
        return {"sum_radii": str(sum((F(c['r']) for c in s['circles']),F(0)))}
    if task == "T009":
        import mpmath as mp
        with mp.workdps(80):
            p=[[mp.mpf(str(F(x).numerator))/F(x).denominator for x in v] for v in s['points']]
            cosine=max(sum(x*y for x,y in zip(a,b))/mp.sqrt(sum(x*x for x in a)*sum(y*y for y in b)) for a,b in itertools.combinations(p,2))
            return {"minimum_angle_80_digits": mp.nstr(mp.acos(cosine),80)}
    if task == "T014":
        p=[[F(x) for x in v] for v in s['points']]
        area=min(abs(a[0]*b[1]+b[0]*c[1]+c[0]*a[1]-a[1]*b[0]-b[1]*c[0]-c[1]*a[0])/2 for a,b,c in itertools.combinations(p,3))
        if config is None or config['id']=='T014-C01': assert area==F(1,27)
        return {"minimum_triangle_area":str(area),"triangles":math.comb(len(p),3)}
    if task == "T035":
        import networkx as nx
        g=nx.Graph();g.add_nodes_from(range(s['vertices']));g.add_edges_from(s['edges'])
        assert nx.is_connected(g) and set(dict(g.degree()).values())=={4}
        girth=nx.girth(g); assert girth>=10
        return {"order":len(g),"networkx_girth":girth}
    if task == "T044":
        differences=[abs(a-b) for a,b in itertools.combinations(s['marks'],2)]
        expected=math.comb(len(s['marks']),2)
        assert len(differences)==len(set(differences))==expected and min(differences)>0
        return {"distinct_positive_differences":expected,"span":max(s['marks'])-min(s['marks'])}
    if task == "T057":
        a=s['set']; ns=len({x+y for x,y in itertools.product(a,repeat=2)});nd=len({x-y for x,y in itertools.product(a,repeat=2)})
        return {"cardinality":len(a),"sumset":ns,"difference_set":nd,"ratio":math.log(ns/len(a))/math.log(nd/len(a))}
    if task == "T060":
        masks=[sum(1<<x for x in b) for b in s['blocks']]
        for q in itertools.combinations(range(24),4):
            mask=sum(1<<x for x in q);assert any(mask&b==mask for b in masks)
        return {"blocks":len(masks),"four_subsets":10626}
    if task == "T066":
        rows=[sum(x<<i for i,x in enumerate(row)) for row in s['generator_matrix']]
        space={0}
        for row in rows: space |= {x^row for x in list(space)}
        assert len(space)==32768
        return {"codewords":len(space),"minimum_distance":min(x.bit_count() for x in space if x)}
    if task == "T067":
        words=s['codewords']; d=min((a^b).bit_count() for a,b in itertools.combinations(words,2))
        assert d>=6
        return {"codewords":len(words),"minimum_distance":d}
    if task == "T073":
        a=s['sequence']; bits=sum((x==1)<<i for i,x in enumerate(a))
        correlations=[len(a)-k-2*((bits^(bits>>k))&((1<<(len(a)-k))-1)).bit_count() for k in range(1,len(a))]
        return {"energy":sum(x*x for x in correlations),"lags":len(correlations)}
    if task in ('T079','T080','T081'):
        a=[F(x) for x in s['coefficients']];b=[F(0)]*(2*len(a)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(a): b[i+j]+=x*y
        mass=sum(a)
        if task=='T080': value=(2*sum(x*x for x in b)+sum(x*y for x,y in zip(b,b[1:])))/(3*max(b)*mass*mass)
        else: value=2*len(a)*max(abs(x) for x in b)/(mass*mass)
        return {"exact_objective":str(value),"convolution_entries":len(b)}
    if task == 'T082':
        a=[F(x) for x in s['heights']];h=F(2,51); values=[]
        # Integrate segment intersections directly; no checker lag function.
        for lag in range(-51,52):
            shift=lag*h;value=F(0)
            for i,x in enumerate(a):
                for j,y in enumerate(a):
                    width=max(F(0),min((i+1)*h,(j+1)*h-shift)-max(i*h,j*h-shift))
                    value+=width*x*(1-y)
            values.append(value)
        assert h*sum(a)==1
        return {"maximum_overlap":str(max(values)),"integral":"1","knots_including_zero_exterior":103}
    if task == 'N001':
        words=s['words']
        for a,b in itertools.combinations(words,2): assert any((x-y)%7 not in (0,1,6) for x,y in zip(a,b))
        return {"independent_words":len(words),"pairs":len(words)*(len(words)-1)//2}
    if task == 'T089':
        from sympy import Matrix
        return {"absolute_determinant":str(abs(Matrix(s['matrix']).det(method='domain-ge')))}
    if task == 'T099':
        a=s['tuple'];primes=[p for p in range(2,344) if all(p%d for d in range(2,math.isqrt(p)+1))]
        assert len(set(a))==343
        missing={str(p):next(r for r in range(p) if r not in {x%p for x in a}) for p in primes}
        return {"diameter":max(a)-min(a),"primes":len(primes),"missing_residues":missing}
    if task == 'T097':
        a=s['chain'];seen={1};assert a[0]==1
        for value in a[1:]:
            assert value>max(seen) and any(value-x in seen for x in seen);seen.add(value)
        target=(config or {}).get('parameters',{}).get('target','2^192-2^64-3')
        expected={'2^192-2^64-3':2**192-2**64-3,'2^221-5':2**221-5,'2^521-3':2**521-3}[target]
        assert a[-1]==expected
        return {"additions":len(a)-1,"target":str(a[-1])}
    raise ValueError(task)


def broken(task, solution):
    s=json.loads(json.dumps(solution))
    if task in ('T079','T080','T081'): s['coefficients']=[0]*len(s['coefficients'])
    elif task=='T082': s['heights'][0]='2'
    elif task=='T001': s['centers'][1]=s['centers'][0]
    elif task=='T005': s['circles'][1]=s['circles'][0]
    elif task=='T002': s['squares'][1]=s['squares'][0]
    elif task in ('T009','T014'): s['points'][1]=s['points'][0]
    elif task=='T035': s['edges'].pop()
    elif task=='T060': s['blocks']=[]
    elif task=='T066': s['generator_matrix'][1]=s['generator_matrix'][0]
    elif task=='T089': s['matrix'][0][0]=0
    elif task=='T073': s['sequence'][0]=0
    else:
        key={'T044':'marks','T057':'set','T067':'codewords','N001':'words','T099':'tuple','T097':'chain'}[task]
        s[key][1]=s[key][0]
    return s
