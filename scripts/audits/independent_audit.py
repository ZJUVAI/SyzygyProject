"""Main-review cross-checks, separate from task checker implementations."""
import itertools
import json
import math
from fractions import Fraction as F

from mathbench.registry import ROOT

def independent_quantity(task, s, config=None):
    if task == 'T099':
        from scripts.audits.polyomino_rectangle_audit import audit
        return audit(s)
    if task == 'T100':
        import numpy as np
        edges=s['edges'];assert len(edges)==700
        A=np.zeros((50,50),dtype=np.int64);seen=set()
        for edge in edges:
            assert len(edge)==2
            u,v=edge;assert type(u)is int and type(v)is int and 0<=u<50 and 0<=v<50 and u!=v
            pair=tuple(sorted(edge));assert pair not in seen;seen.add(pair)
            A[u,v]=A[v,u]=1
        trace=int(np.trace((A@A)@A));assert trace%6==0
        return {'triangle_count':trace//6,'edge_count':len(seen),'vertex_count':50,'method':'Integer adjacency-matrix cubic trace divided by six; matrix entries and integer overflow bound independently checked (50 cubed is below 2^63).'}
    if task == 'T098':
        from scripts.audits.perfect_square_audit import audit
        return audit(s)
    if task == 'T096':
        from scripts.audits.ovals_audit import audit
        return audit(s)
    if task == 'T095':
        from scripts.audits.convex_partition_audit import audit
        return audit(s)
    if task == 'T094':
        from scripts.audits.regular_dilation_audit import audit_edges
        return audit_edges(s['edges'])
    if task == 'T097':
        from scripts.audits.convex_cover_audit import audit_polygons
        data=json.loads((ROOT/'tasks/t097/data/source/socg_fixed92.instance.json').read_text())
        assert not data['holes']
        assert list(map(F,s['algebraic_field']['minimal_polynomial']))==[0,1]
        polygon=[(v['x'],v['y']) for v in data['outer_boundary']]
        covers=[[(F(x[0]) if x else F(0),F(y[0]) if y else F(0)) for x,y in q] for q in s['polygons']]
        return audit_polygons(polygon,covers)
    if task == 'T092':
        from scripts.audits.spherical_harmonic_audit import audit
        return audit(s)
    if task == 'T093':
        from scripts.audits.polygon_packing_audit import audit
        return audit(s)
    if task == 'T091':
        from scripts.audits.orthogonal_array_audit import audit
        return audit(s)
    if task == 'T090':
        a=s['sequence'];assert len(a)==64 and all(type(v)is int and abs(v)==1 for v in a)
        mask=(1<<64)-1;bits=sum((v==1)<<i for i,v in enumerate(a));corr=[64]
        for k in range(1,64):
            rotated=((bits<<k)|(bits>>(64-k)))&mask
            corr.append(64-2*(bits^rotated).bit_count())
        assert sum(corr)==sum(a)**2
        return {'energy':sum(v*v for v in corr[1:]),'correlations':corr,'peak_sidelobe':max(map(abs,corr[1:])),'sum_of_signs':sum(a),'method':'Cyclic bit rotation and XOR Hamming weights; independently verifies sum of all cyclic correlations equals squared sign sum.'}
    if task == 'T089':
        from scripts.audits.sign_uncertainty_audit import audit
        return audit(s)
    if task == 'T088':
        rows=(ROOT/'tasks/t088/data/source/arc130.mtx.rnd').read_text().splitlines()
        assert list(map(int,rows[1].split()))==[130,130,715]
        edges=[tuple(map(int,line.split())) for line in rows[2:]]
        assert len(edges)==len(set(tuple(sorted(e)) for e in edges))==715
        assert all(1<=a<=130 and 1<=b<=130 and a!=b for a,b in edges)
        order=s['ordering'];assert sorted(order)==list(range(1,131))
        cuts=[];left=set()
        for v in order[:-1]:
            left.add(v);cuts.append(sum((a in left)!=(b in left) for a,b in edges))
        degrees=[sum(v in e for e in edges) for v in range(1,131)]
        assert max(degrees)==124
        return {'cutwidth':max(cuts),'cut_profile':cuts,'maximum_degree_lower_bound':62,'method':'Independent direct set bipartition edge counts for every prefix; degree/2 lower bound, integer arithmetic.'}
    if task == 'T087':
        a=list(map(F,s['heights']));assert len(a)==480 and min(a)>=0 and sum(a)>0
        D=math.lcm(*(v.denominator for v in a));h=[int(v*D) for v in a]
        B=sum(x*x for x in h)+1
        left=sum(v*B**i for i,v in enumerate(h));right=sum(v*B**i for i,v in enumerate(reversed(h)))
        product=left*right;coeff=[]
        for _ in range(959):coeff.append(product%B);product//=B
        assert product==0
        d=F(13,4800);lag=369;f=F(3,13)
        values=[F(coeff[479+k]) for k in range(lag+1)]
        values.append((1-f)*coeff[479+lag]+f*coeff[480+lag])
        return {'minimum_autocorrelation_ratio':str(min(values)/(d*sum(h)**2)),'minimum_autocorrelation':str(d*min(values)/(D*D)),'l1_mass':str(d*sum(h)/D),'method':'exact integer Kronecker polynomial multiplication for all correlation coefficients, plus exact endpoint interpolation; no sampling'}
    if task == 'T085':
        from scripts.audits.disk_cover_audit import audit
        return audit(s)
    if task == 'T086':
        from scripts.audits.duchi_audit import audit
        return audit(s)
    if task == 'T084':
        from collections import defaultdict
        a=[int(v) for v in s['elements']];assert len(a)==len(set(a))==31
        coeff=defaultdict(int)
        for x,y,z in itertools.product(a,repeat=3):coeff[x+y+z]+=1
        for x,y in itertools.product(a,repeat=2):coeff[x+2*y]+=3
        for x in a:coeff[3*x]+=2
        assert len(coeff)==5456 and set(coeff.values())=={6}
        return {'diameter':max(a)-min(a),'triple_sums':len(coeff),'counting_lower_bound':1819,'method':'Newton complete-symmetric identity h3=(p1^3+3p1*p2+2p3)/6, exact sparse polynomial coefficients all equal one'}
    if task == 'T083':
        from scripts.audits.triangle_packing_audit import audit
        return audit(s)
    if task == 'T082':
        armies=[s['white'],s['black']]
        assert len(armies[0])==len(armies[1])
        line_sets=[]
        for army in armies:
            pts=[tuple(v) for v in army]
            assert len(pts)==len(set(pts)) and all(len(v)==2 and all(type(x)is int and 0<=x<30 for x in v) for v in pts)
            line_sets.append([{f(r,c) for r,c in pts} for f in (lambda r,c:r,lambda r,c:c,lambda r,c:r-c,lambda r,c:r+c)])
        assert all(not(a&b) for a,b in zip(*line_sets))
        return {'army_size':len(armies[0]),'finite_upper_bound':225,'method':'disjoint occupied line labels in each of four queen directions; independent of pairwise attacks'}
    if task == 'T081':
        p=[tuple(map(F,v)) for v in s['points']]
        assert len(p)==12 and len(set(p))==12 and all(len(v)==2 for v in p)
        norm=[sum(c*c for c in v) for v in p]
        distances=[norm[i]+norm[j]-2*sum(a*b for a,b in zip(p[i],p[j])) for i,j in itertools.combinations(range(12),2)]
        assert min(distances)>0
        return {'distance_ratio':str(max(distances)/min(distances)),'minimum_squared_distance':str(min(distances)),'maximum_squared_distance':str(max(distances)),'pairs_checked':len(distances),'method':'exact Gram matrix identity for every pair, independently reconstructed from rational coordinates'}
    if task == 'T079':
        p=31
        projective=set()
        for v in itertools.product(range(p),repeat=3):
            if any(v):
                last=max(i for i in range(3) if v[i]);inv=pow(v[last],-1,p)
                projective.add(tuple(x*inv%p for x in v))
        assert len(projective)==993
        seen=set();mask=bytearray(p**3)
        for line in s['lines']:
            v=tuple(line['direction']);o=tuple(line['origin'])
            assert v in projective and v not in seen;seen.add(v)
            assert len(o)==3 and all(type(x)is int and 0<=x<p for x in o)
            a,b,c=o
            for _ in range(p):
                mask[(a*p+b)*p+c]=1
                a,b,c=(a+v[0])%p,(b+v[1])%p,(c+v[2])%p
            assert (a,b,c)==o
        assert seen==projective
        return {'union_cardinality':sum(mask),'directions_checked':993,'line_incidences_checked':30783,'bukh_chao_lower_bound':math.ceil(F(31**5,61**2)),'method':'projectivize every nonzero vector; repeated modular additions and dense finite-space bitmap'}
    if task == 'T078':
        from scripts.audits.lattice_audit import audit
        return audit(s)
    if task in ('T077', 'T080'):
        a=s['set'];assert 2<=len(a)<=512 and len(a)==len(set(a))
        assert all(type(v)is int and (-1000000 if task=='T077' else 0)<=v<=1000000 for v in a)
        sums=sorted(x+y for x,y in itertools.combinations_with_replacement(a,2))
        diffs=sorted(x-y for x,y in itertools.product(a,repeat=2))
        ns=sum(i==0 or v!=sums[i-1] for i,v in enumerate(sums))
        nd=sum(i==0 or v!=diffs[i-1] for i,v in enumerate(diffs))
        def log_bounds(n):
            def series(z):
                power=z;total=F(0)
                for j in range(110):total+=2*power/(2*j+1);power*=z*z
                return total,total+2*power/(221*(1-z*z))
            k=n.bit_length()-1;u=F(n,2**k)
            l,h=series((u-1)/(u+1));l2,h2=series(F(1,3))
            return l+k*l2,h+k*h2
        dl,dh=log_bounds(nd);sl,sh=log_bounds(ns)
        interval=(dl/sh,dh/sl)
        if task=='T080':
            q=2*max(a)+1;assert 0 in a and nd<q
            ql,qh=log_bounds(q)
            bounds=[n/d for n in (dl-sh,dh-sl) for d in (ql,qh)]
            interval=(F(1)+min(bounds),F(1)+max(bounds)) if nd!=ns else (F(1),F(1))
        return {'ratio_interval':list(map(str,interval)),'sumset_size':ns,'difference_set_size':nd,'cardinality':len(a),'method':'sorted pair values and exact rational atanh series with geometric remainder, independent of mpmath intervals'}
    if task == 'T075':
        edges=[tuple(sorted(e)) for e in s['edges']]
        assert len(edges)==len(set(edges)) and all(len(set(e))==3 and all(type(v)is int and 0<=v<36 for v in e) for e in edges)
        links=[[[False]*36 for _ in range(36)] for _ in range(36)]
        for a,b,c in edges:
            for v,u,w in [(a,b,c),(b,a,c),(c,a,b)]:links[v][u][w]=links[v][w][u]=True
        # K4-minus is equivalent to a triangle in one vertex link graph.
        for v in range(36):
            for a,b,c in itertools.combinations([u for u in range(36) if u!=v],3):
                assert not (links[v][a][b] and links[v][b][c] and links[v][a][c])
        return {'edge_count':len(edges),'link_graphs_checked':36,'double_counting_upper_bound':3570,'method':'all vertex links triangle-free, independent of formal four-set loads'}
    if task == 'T076':
        a=[int(v) for v in s['elements']]
        count = config['parameters']['element_count']
        assert len(a)==len(set(a))==count and min(a)>0
        sums=[0]
        for v in a:sums=sums+[x+v for x in sums]
        assert len(sums)==len(set(sums))==1<<count
        return {'largest_element':max(a),'subset_sums_checked':len(sums),'method':'direct recursively doubled integer sum list, no modular fingerprints or Gray traversal'}
    if task == 'T074':
        p=[tuple(F(str(v)) for v in row) for row in s['points']]
        assert len(p)==len(set(p))==12
        def det(a,b,c):
            return a[0]*b[1]+b[0]*c[1]+c[0]*a[1]-a[1]*b[0]-b[1]*c[0]-c[1]*a[0]
        triangles=[abs(det(*triple)) for triple in itertools.combinations(p,3)]
        assert min(triangles)>0
        # Enumerate oriented support edges directly, without a convex-hull walk.
        edges=[(a,b) for a,b in itertools.permutations(p,2) if all(c in (a,b) or det(a,b,c)>0 for c in p)]
        area2=sum(a[0]*b[1]-a[1]*b[0] for a,b in edges)
        assert area2>0
        return {'area_ratio':str(min(triangles)/area2),'minimum_triangle_area':str(min(triangles)/2),'hull_area':str(area2/2),'support_edges':len(edges),'triangles_checked':220}
    if task == 'T073':
        import sympy as sp
        x=sp.Symbol('x');poly=sum(int(c)*x**i for i,c in enumerate(s['minimal_polynomial']))
        lo,hi=map(sp.Rational,s['isolating_interval'])
        roots=[r for r in sp.real_roots(poly) if bool(r>lo) and bool(r<hi)]
        assert len(roots)==1
        a=roots[0]
        points=[tuple(sp.expand(sum(sp.Rational(c)*a**i for i,c in enumerate(v))) for v in p) for p in s['points']]
        assert len(set(points))==len(points)
        assert all(sp.simplify(sum(v*v for v in p)-1)==0 for p in points)
        checked=0
        for e in itertools.product(range(6),repeat=4):
            if sum(e)>5:continue
            total=sp.expand(sum(math.prod(p[j]**e[j] for j in range(4)) for p in points))
            target=sp.Rational(0)
            if not any(v%2 for v in e):
                # Independent Dirichlet sphere moment via rising factorials.
                k=[v//2 for v in e]
                target=sp.prod(sp.rf(sp.Rational(1,2),v) for v in k)/sp.rf(2,sum(k))
            assert sp.simplify(total-len(points)*target)==0
            checked+=1
        assert checked==126
        return {'point_count':len(points),'monomials_checked':checked,'method':'symbolic real-root coordinates and Dirichlet rising-factorial sphere moments'}
    if task == 'T072':
        a=s['elements'];assert len(a)==len(set(a))==32 and all(type(x) is int and x>0 for x in a)
        sums=sorted(x+y for x,y in itertools.combinations_with_replacement(a,2))
        products=sorted(x*y for x,y in itertools.combinations_with_replacement(a,2))
        ns=sum(i==0 or x!=sums[i-1] for i,x in enumerate(sums))
        np=sum(i==0 or x!=products[i-1] for i,x in enumerate(products))
        return {'max_size':max(ns,np),'sumset_size':ns,'productset_size':np,'unordered_pairs_with_replacement':528}
    if task == 'T071':
        words=s['codewords'];assert len(words)==len(set(words))
        assert all(type(w) is int and 0<=w<65536 for w in words)
        owners={}
        for word in words:
            text=format(word,'016b')
            outputs={text[:i]+text[i+1:] for i in range(16)}
            for output in outputs:
                assert output not in owners;owners[output]=word
        return {'code_size':len(words),'distinct_outputs':len(owners),'method':'independent string slicing at each deletion index, with per-word duplicates removed'}
    if task == 'T070':
        squares=s['squares'];area=0;sides=[]
        for i,(x,y,d) in enumerate(squares):
            assert all(type(v) is int for v in (x,y,d)) and 0<d<1000
            assert 0<=x<=1000-d and 0<=y<=1000-d
            area+=d*d;sides.append(d)
            for a,b,c in squares[:i]:assert x+d<=a or a+c<=x or y+d<=b or b+c<=y
        assert area==1000000 and math.gcd(*sides)==1
        return {'square_count':len(squares),'total_area':area,'gcd':1,'method':'independent pairwise exact rectangle separation plus full area'}
    if task == 'T069':
        rows=(ROOT/'tasks/t069/data/source/mona-lisa100K.tsp').read_text().split('NODE_COORD_SECTION',1)[1].split('EOF',1)[0].splitlines()
        points={}
        for row in rows:
            if row.strip():
                i,x,y=map(int,row.split());points[i-1]=(x,y)
        tour=s['tour'];assert len(tour)==100000 and set(tour)==set(range(100000))
        total=0
        for a,b in zip(tour,tour[1:]+tour[:1]):
            x,y=points[a];u,v=points[b];q=(x-u)**2+(y-v)**2
            # Binary-search the rounded distance directly via midpoint inequalities.
            lo,hi=0,40000
            while lo<hi:
                mid=(lo+hi)//2
                if 4*q<(2*mid+1)**2:hi=mid
                else:lo=mid+1
            total+=lo
        return {'tour_cost':total,'independent_method':'binary search integer rounding thresholds, direct raw TSPLIB parse','closed_edges_checked':100000}
    if task == 'T068':
        words=s['codewords'];assert len(words)==len(set(words))
        assert all(type(w) is int and 0<=w<1024 for w in words)
        distances=[min((x^w).bit_count() for w in words) for x in range(1024)]
        assert max(distances)<=1
        return {'code_size':len(words),'words_checked':1024,'maximum_distance':max(distances),'sphere_bound':94}
    if task == 'T067':
        seen=set();blocks=set()
        for word in s['codewords']:
            assert type(word) is str and len(word)==17 and set(word)<={'0','1'}
            positions=tuple(i for i,c in enumerate(word) if c=='1')
            assert len(positions)==5 and positions not in seen;seen.add(positions)
            for subset in itertools.combinations(positions,4):
                assert subset not in blocks;blocks.add(subset)
        assert len(blocks)==5*len(seen)<=math.comb(17,4)
        return {'code_size':len(seen),'distinct_four_subsets':len(blocks),'packing_bound':math.comb(17,4)//5}
    if task == 'T066':
        from scripts.audits.orchard_audit import audit
        return audit(s)
    if task == 'T065':
        # Saved-run audit for rational seeds and reconstructed triangular-lattice patches.
        # Formal validation accepts arbitrary real algebraic coordinate fields.
        points=[]
        if s['minimal_polynomial']==[0,1]:
            for point in s['points']:
                assert len(point['x'])==len(point['y'])==1
                points.append((F(point['x'][0]),F(point['y'][0]),F(0)))
        else:
            assert s['minimal_polynomial']==[64,0,-28,0,1]
            assert list(map(F,s['isolating_interval']))==[F(5),F(51,10)]
            # alpha=sqrt(3)+sqrt(11); alpha^3-20alpha=16sqrt(3).
            for point in s['points']:
                x=list(map(F,point['x']));y=list(map(F,point['y']))
                assert len(x)==len(y)==4 and x[1:]==[0,0,0]
                assert y[0]==y[2]==0 and y[1]==-20*y[3]
                points.append((x[0],F(0),16*y[3]))
        assert len(points)==len(set(points))==100
        count=0
        for (x,y,z),(a,b,c) in itertools.combinations(points,2):
            dx=x-a;dy=y-b;dz=z-c
            # Coordinates (x,y+z*sqrt(3)): irrational coefficient must vanish.
            if dx*dx+dy*dy+3*dz*dz==1 and 2*dy*dz==0:count+=1
        return {'unit_pairs':count,'unordered_pairs_checked':4950,'method':'independent Q(sqrt(3)) norm expansion for saved witnesses'}
    if task == 'T064':
        from scripts.audits.nonobtuse_audit import audit
        return audit(s)
    if task == 'T062':
        values=s['elements'];assert len(values)==len(set(values))
        assert all(type(v) is int and 1<=v<=42025 for v in values)
        mask=sum(1<<(v-1) for v in values)
        for root in range(1,205):assert not mask&(mask<<(root*root))
        assert mask.bit_count()==len(values)
        return {'cardinality':len(values),'positive_square_shifts_checked':204}
    if task == 'T063':
        coefficients=s['coefficients_ascending']
        assert len(coefficients)==101 and all(type(a) is int for a in coefficients)
        assert math.gcd(*coefficients)==1 and coefficients[-1]!=0
        # Saved simple/search witnesses are Eisenstein binomials: exact M(x^100-p)=p.
        if coefficients[-1]==1 and all(a==0 for a in coefficients[1:-1]) and coefficients[0]<-1:
            prime=-coefficients[0]
            assert all(prime%d for d in range(2,math.isqrt(prime)+1))
            return {'mahler_interval':[str(prime),str(prime)],'method':'Eisenstein binomial with all roots of modulus p^(1/100)'}
        # Independent modular degree obstruction: mod 2 factors have degrees 50,50;
        # mod 13 factors have degrees 12,88. No nontrivial rational factor degree fits both.
        import sympy as sp
        x=sp.Symbol('x');possible=set(range(101));modular_degrees={}
        for prime in (2,13):
            modular=sp.Poly.from_list(list(reversed(coefficients)),x,modulus=prime)
            factors=modular.factor_list()[1];degrees=[]
            for factor,multiplicity in factors:degrees.extend([factor.degree()]*multiplicity)
            sums={0}
            for degree in degrees:sums|={v+degree for v in tuple(sums)}
            possible&=sums;modular_degrees[str(prime)]=degrees
        assert possible=={0,100}
        # Separate exact root enclosure: interpolation matrix and column Gershgorin.
        # This audits saved database witnesses; the formal checker accepts general certificates.
        D=10**24;radius=F(1,10**20);centers=[]
        for disk in s['root_disks']:
            a,b=F(disk['center_real']),F(disk['center_imag'])
            assert (a*D).denominator==(b*D).denominator==1
            centers.append((int(a*D),int(b*D)))
        assert len(centers)==100
        lower=upper=F(abs(coefficients[-1]))
        for j,(a,b) in enumerate(centers):
            real=coefficients[-1];imag=0;power=D
            for coefficient in reversed(coefficients[:-1]):
                real,imag=real*a-imag*b+coefficient*power,real*b+imag*a
                power*=D
            distance_product=1
            for k,(x,y) in enumerate(centers):
                if k==j:continue
                distance=math.isqrt((a-x)**2+(b-y)**2)
                assert F(distance,D)>2*radius
                distance_product*=distance
            # A=diag(c)-1*w^T has characteristic polynomial p/leading coefficient.
            # Its jth column Gershgorin disk fits within |z-c_j| < n|w_j| < radius.
            assert 100*(abs(real)+abs(imag))*radius.denominator < abs(coefficients[-1])*D*distance_product*radius.numerator
            norm=math.isqrt(a*a+b*b);lo=F(norm,D)
            hi=lo if norm*norm==a*a+b*b else F(norm+1,D)
            lower*=max(F(1),lo-radius);upper*=max(F(1),hi+radius)
        assert lower>1
        return {'mahler_interval':[str(lower),str(upper)],'method':'exact interpolation matrix, 100 disjoint Gershgorin disks','irreducibility_modular_degrees':modular_degrees}
    if task == 'T061':
        from collections import defaultdict
        edges={tuple(sorted(e)) for e in s['edges']}
        assert s['vertices']==100 and len(edges)==len(s['edges'])
        neighbors=[set() for _ in range(100)]
        for a,b in edges:
            assert type(a) is int and type(b) is int and 0<=a<b<100
            neighbors[a].add(b);neighbors[b].add(a)
        # A C6 has two internally disjoint 3-edge paths between opposite vertices.
        triples=defaultdict(list)
        for u in range(100):
            for a in neighbors[u]:
                for b in neighbors[a]-{u}:
                    for v in neighbors[b]-{u,a}:
                        if u<v:triples[u,v].append((a,b))
        for paths in triples.values():
            for i,(a,b) in enumerate(paths):
                assert all(len({a,b,c,d})<4 for c,d in paths[i+1:])
        missing=0
        for u in range(100):
            for v in range(u+1,100):
                if (u,v) in edges:continue
                # Meet two edges from u with three edges from v, with six distinct vertices.
                found=False
                for a in neighbors[u]-{v}:
                    for b in neighbors[a]-{u,v}:
                        paths=triples.get((b,v) if b<v else (v,b),())
                        if any(len({u,a,b,c,d,v})==6 for c,d in paths):
                            found=True;break
                    if found:break
                assert found,(u,v)
                missing+=1
        return {'edge_count':len(edges),'missing_pairs_checked':missing,'simple_c6_free':True}
    if task == 'T060':
        import ast
        expression=s['expression'];tree=ast.parse(expression,mode='eval')
        def walk(node):
            if isinstance(node,ast.Constant):
                assert type(node.value) is int and node.value==1
                return 1,1
            assert isinstance(node,ast.BinOp) and type(node.op) in (ast.Add,ast.Mult)
            a,k=walk(node.left);b,l=walk(node.right)
            return (a+b if isinstance(node.op,ast.Add) else a*b),k+l
        value,ones=walk(tree.body);assert value==2**61-1
        # Independently maximize all binary root splits through 115 leaves.
        extrema=[0,1]
        for k in range(2,116):
            extrema.append(max(max(extrema[j]+extrema[k-j],extrema[j]*extrema[k-j]) for j in range(1,k)))
        assert extrema[115]==1801135623563989452<value
        return {'one_count':ones,'exact_value':value,'strict_lower_bound':116}
    if task == 'T058':
        rounds=s['rounds'];assert 1<=len(rounds)<=8
        opponents=[0]*35
        for groups in rounds:
            assert len(groups)==7
            occupied=0
            for group in groups:
                assert len(group)==5 and len(set(group))==5
                assert all(type(v) is int and 0<=v<35 for v in group)
                mask=sum(1<<v for v in group);assert not occupied&mask;occupied|=mask
                for player in group:
                    others=mask^(1<<player)
                    assert not opponents[player]&others
                    opponents[player]|=others
            assert occupied==(1<<35)-1
        assert all(mask.bit_count()==4*len(rounds) for mask in opponents)
        return {'round_count':len(rounds),'distinct_pairs':sum(m.bit_count() for m in opponents)//2}
    if task == 'T059':
        import gzip
        vertices=s['vertices'];assert all(type(v) is int and 0<=v<2000 for v in vertices)
        assert len(vertices)==len(set(vertices))
        needed={tuple(sorted(pair)) for pair in itertools.combinations(vertices,2)}
        found=set();edges=0
        path=ROOT/'tasks/t059/data/source/C2000.9.clq.gz'
        with gzip.open(path,'rt') as stream:
            for line in stream:
                if line.startswith('e '):
                    _,a,b=line.split();pair=tuple(sorted((int(a)-1,int(b)-1)));edges+=1
                    if pair in needed:found.add(pair)
        assert edges==1799532 and found==needed
        return {'clique_cardinality':len(vertices),'required_edges_found':len(found)}
    if task == 'T057':
        path=ROOT/'tasks/t057/data/source/X-n1001-k43.vrp'
        coords={};demands={};mode=None
        for raw in path.read_text().splitlines():
            line=raw.strip()
            if line in ('NODE_COORD_SECTION','DEMAND_SECTION','DEPOT_SECTION'):mode=line;continue
            if mode=='NODE_COORD_SECTION':i,x,y=map(int,line.split());coords[i]=(x,y)
            elif mode=='DEMAND_SECTION':i,d=map(int,line.split());demands[i]=d
            elif mode=='DEPOT_SECTION':break
        routes=s['routes'];assert sorted(sum(routes,[]))==list(range(2,1002))
        assert sum(demands.values())==5557
        cost=0;maximum_load=0
        for route in routes:
            load=sum(demands[v] for v in route);assert load<=131;maximum_load=max(maximum_load,load)
            points=[1]+route+[1]
            for u,v in zip(points,points[1:]):
                square=sum((a-b)**2 for a,b in zip(coords[u],coords[v]));lo=0;hi=2048
                # Binary-search nearest-integer distance using only squares.
                while lo<hi:
                    mid=(lo+hi)//2
                    if 4*square<(2*mid+1)**2:hi=mid
                    else:lo=mid+1
                cost+=lo
        assert len(routes)>=(5557+130)//131
        return {'route_cost':cost,'routes':len(routes),'maximum_load':maximum_load}
    if task == 'T055':
        assignment=s['assignment'];assert len(assignment)==1630 and all(type(v) is bool for v in assignment)
        bits=sum(v<<i for i,v in enumerate(assignment));hard=0;soft=0;cost=0
        path=ROOT/'tasks/t055/data/source/b4794d123e18a908924d3d33cdeeae3b.wcnf'
        for line in path.read_text().splitlines():
            fields=line.split()
            if not fields or fields[0].startswith(('c','p','%')):continue
            assert fields[-1]=='0';positive=negative=0
            for literal in map(int,fields[1:-1]):
                if literal>0:positive|=1<<(literal-1)
                else:negative|=1<<(-literal-1)
            satisfied=bool(bits&positive or ~bits&negative)
            if fields[0]=='h':assert satisfied;hard+=1
            else:
                weight=int(fields[0]);soft+=weight*satisfied;cost+=weight*(not satisfied)
        assert hard==6150 and soft+cost==649
        return {'satisfied_soft_weight':soft,'unsatisfied_soft_weight':cost,'hard_clauses':hard}
    if task == 'T056':
        operations=json.loads((ROOT/'tasks/t056/data/source/ta41_instance.json').read_text())['operations']
        orders=s['machine_orders']
        assert len(orders)==20 and all(sorted(o)==list(range(30)) for o in orders)
        job_index=[0]*30;machine_index=[0]*20;job_ready=[0]*30;machine_ready=[0]*20
        remaining=600
        # Dispatch only an operation which is next in both its job and machine.
        # This uses two resource clocks, rather than building a precedence DAG.
        while remaining:
            progress=False
            for j in range(30):
                if job_index[j]==20: continue
                machine,duration=operations[j][job_index[j]]
                if machine_index[machine]>=30 or orders[machine][machine_index[machine]]!=j:continue
                finish=max(job_ready[j],machine_ready[machine])+duration
                job_ready[j]=machine_ready[machine]=finish
                job_index[j]+=1;machine_index[machine]+=1;remaining-=1;progress=True
            assert progress,'precedence deadlock'
        return {'makespan':max(job_ready),'operations_dispatched':600}
    if task == 'T054':
        length = config['parameters']['length']
        signs=s['sequence'];assert len(signs)==length and all(type(x) is int and x in (-1,1) for x in signs)
        bits=sum((x==1)<<i for i,x in enumerate(signs))
        # Bit XOR counts mismatches; no multiply-and-sum correlation loop.
        values=[length-k-2*(((bits^(bits>>k))&((1<<(length-k))-1)).bit_count()) for k in range(1,length)]
        return {'peak_sidelobe':max(map(abs,values)),'energy':sum(x*x for x in values),'correlations':values}
    if task == 'T053':
        factors=s['factors']
        assert len(factors)==100000 and all(type(x) is int and x>0 for x in factors)
        # Divide each factor using an independent smallest-prime-factor sieve.
        n=100000
        spf=list(range(n+1))
        for p in range(2,math.isqrt(n)+1):
            if spf[p]==p:
                for j in range(p*p,n+1,p):
                    if spf[j]==j: spf[j]=p
        residuals={p:0 for p in range(2,n+1) if spf[p]==p}
        for value in factors:
            for p in residuals:
                if p*p>value: break
                while value%p==0:
                    residuals[p]+=1;value//=p
            if value>1:
                assert value in residuals
                residuals[value]+=1
        for p,exponent in residuals.items():
            expected=0;power=p
            while power<=n: expected+=n//power;power*=p
            assert exponent==expected
        return {'minimum_factor':min(factors),'factor_count':n,'prime_exponents_checked':len(residuals)}
    if task == 'T051':
        import numpy as np
        signs=np.array(s['sequence'],dtype=np.int64)
        assert all(type(x) is int and x in (-1,1) for x in s['sequence'])
        n=len(signs);maximum=0;count=0
        for d in range(1,n+1):
            sums=np.cumsum(signs[d-1::d],dtype=np.int64)
            maximum=max(maximum,int(np.max(np.abs(sums))))
            count+=len(sums)
        assert maximum<=3
        return {'sequence_length':n,'discrepancy':maximum,'prefixes_checked':count}
    if task == 'T052':
        import numpy as np
        words=s['codewords']; a=np.array(words,dtype=np.int16)
        assert all(sorted(w)==list(range(12)) for w in words)
        assert len({tuple(w) for w in words})==len(words)
        minimum=12
        for i in range(len(words)-1):
            matches=np.count_nonzero(a[i+1:]==a[i],axis=1)
            minimum=min(minimum,12-int(matches.max()))
        assert minimum>=9
        return {'code_size':len(words),'minimum_distance':minimum}
    if task == 'T050':
        path=s['vertices']
        dimension = config['parameters']['dimension']
        vertex_count = 1 << dimension
        assert len(path)==len(set(path)) and len(path)>=2
        assert all(type(v) is int and 0<=v<vertex_count for v in path)
        selected=set(path)
        total_degree=0
        for i,v in enumerate(path):
            induced_neighbors={v^(1<<bit) for bit in range(dimension)} & selected
            required=set(path[max(0,i-1):i]+path[i+1:i+2])
            assert induced_neighbors==required
            total_degree+=len(induced_neighbors)
        assert total_degree%2==0 and total_degree//2==len(path)-1
        # Count selected neighbors via all coordinate flips, rather than
        # the checker's Hamming-distance loop over every vertex pair.
        crossing = (dimension - 2) * len(path) + 2
        assert crossing <= dimension * (vertex_count - len(path))
        upper = (dimension * vertex_count - 2) // (2 * dimension - 2) - 1
        return {'induced_path_edges': total_degree//2, 'neighbor_memberships_checked': dimension*len(path),
                'crossing_edges': crossing, 'analytic_edge_upper_bound': upper}
    if task == 'T049':
        polynomial=s['minimal_polynomial']
        if polynomial==[0,1]:
            points=[(F(point['x'][0]),F(point['y'][0])) for point in s['points']]
            norm=lambda u,v:u*u+v*v
        else:
            assert polynomial==[-3,0,1]
            assert all(all(F(v)==0 for v in point['x'][1:]) and F(point['y'][0])==0
                       for point in s['points'])
            points=[(F(point['x'][0]),F(point['y'][1])) for point in s['points']]
            norm=lambda u,v:u*u+3*v*v
        assert len(points)==len(set(points))==91
        # Use displacement vectors in the saved rational/triangular lattices,
        # rather than quotient-field multiplication of coordinate polynomials.
        displacements={(x-u,y-v) for x,y in points for u,v in points if (x,y)!=(u,v)}
        distances={norm(u,v) for u,v in displacements}
        assert min(distances)>0
        return {'distance_count': len(distances), 'ordered_displacement_types': len(displacements),
                'audit_scope': 'Saved rational and triangular-lattice witnesses; checker permits all real algebraic fields'}
    if task == 'T048':
        import numpy as np
        wires = config['parameters']['inputs']
        inputs=np.arange(1<<wires,dtype=np.uint32)
        expected=np.array([((1<<word.bit_count())-1)<<(wires-word.bit_count())
                           for word in range(1<<wires)],dtype=np.uint32)
        for a,b in s['comparators']:
            assert type(a) is type(b) is int and 0 <= a < b < wires
            swap=((inputs>>a)&1)>((inputs>>b)&1)
            inputs[swap]^=np.uint32((1<<a)|(1<<b))
        # One packed integer per input, in contrast to the task checker's
        # one giant bit vector per wire and AND/OR simulation.
        assert np.array_equal(inputs,expected)
        return {'comparator_count': len(s['comparators']),
                'binary_words_simulated': 1<<wires, 'arithmetic': 'exact uint32 conditional swaps'}
    if task == 'T047':
        basis = s['basis']
        assert len(basis)==len(set(basis)) and all(type(x) is int for x in basis)
        selected=set(basis)
        witnesses=0
        # Enumerate required translations and find a pair for each distance,
        # independently of the checker's forward pair scan and byte array.
        for distance in range(1,6167):
            assert any(x+distance in selected for x in basis)
            witnesses+=1
        return {'difference_basis_size': len(basis), 'required_translations_checked': witnesses,
                'span': max(basis)-min(basis)}
    if task == 'T046':
        coefficients = list(map(F,s['coefficients']))
        while len(coefficients)>1 and coefficients[-1]==0: coefficients.pop()
        assert len(coefficients)<=147 and any(coefficients)
        def divide(poly,root):
            if len(poly)==1: return None
            quotient = [F()]*(len(poly)-1)
            quotient[-1] = poly[-1]
            for k in range(len(poly)-2,0,-1):
                quotient[k-1] = poly[k]+root*quotient[k]
            return quotient if poly[0]+root*quotient[0]==0 else None
        powers=[]
        for root in (F(0),F(1),F(1,2)):
            exponent=0
            while (quotient:=divide(coefficients,root)) is not None:
                coefficients=quotient
                exponent+=1
            powers.append(exponent)
        assert len(coefficients)==1, 'Saved-run audit supports the verified three-factor family only'
        a,c,b=powers
        multiplier=abs(coefficients[0])/2**b
        if b==0:
            norm=multiplier if a+c==0 else multiplier*F(a,a+c)**a*F(c,a+c)**c
        else:
            assert a==c and b%2==0
            t=F(a,4*a+2*b)
            norm=multiplier*t**a*(1-4*t)**(b//2)
        # Differentiate the factored form analytically, independently of
        # Bernstein control coefficients and dyadic subdivision.
        return {'exact_supnorm': str(norm), 'root_multiplicities_0_1_half': powers,
                'audit_scope': 'Analytic norm of saved factor-family witnesses, not a restriction on candidate inputs'}
    if task == 'T045':
        raw = (ROOT / 'tasks/t045/data/source/gd96a.rmf').read_text().splitlines()
        assert raw[0].split() == ['p','ghct','1096','1676']
        neighbors = {i: [] for i in range(1,1097)}
        for line in raw[1:]:
            kind,a,b,weight = line.split()
            assert kind == 'e' and int(weight) == 1
            a,b = int(a),int(b)
            neighbors[a].append(b)
            neighbors[b].append(a)
        order = s['ordering']
        assert len(order) == 1096 and set(order) == set(neighbors)
        seen = set()
        cut = total = 0
        # Every edge contributes to exactly one cut for every unit of its
        # span. Sum all prefix cut sizes instead of absolute positions.
        for vertex in order:
            back = sum(v in seen for v in neighbors[vertex])
            cut += len(neighbors[vertex])-2*back
            seen.add(vertex)
            total += cut
        assert cut == 0
        return {'linear_arrangement_cost': total, 'prefix_cuts_checked': 1096,
                'original_edges_checked': 1676}
    if task == 'T044':
        n = s['n']
        assert type(n) is int and 1 <= n <= 94
        distances = [[0 if i == j else n+1 for j in range(n)] for i in range(n)]
        degree = [0]*n
        unique = set()
        for a,b in s['edges']:
            assert type(a) is type(b) is int and 0 <= a < n and 0 <= b < n and a != b
            edge = tuple(sorted((a,b)))
            assert edge not in unique
            unique.add(edge)
            distances[a][b] = distances[b][a] = 1
            degree[a] += 1
            degree[b] += 1
        assert max(degree) <= 3
        # Floyd-Warshall min-plus closure, independent of per-source BFS.
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    distances[i][j] = min(distances[i][j],distances[i][k]+distances[k][j])
        diameter = max(map(max,distances))
        assert diameter <= 5
        return {'order': n, 'floyd_warshall_diameter': diameter,
                'edge_count': len(unique), 'maximum_degree': max(degree)}
    if task == 'T043':
        used_lines = set()
        for codeword in s['codewords']:
            rows = codeword if all(type(x) is int for x in codeword) else [
                sum(x << j for j,x in enumerate(row)) for row in codeword]
            space = {0}
            for row in rows:
                assert 0 <= row < 128
                space |= {v ^ row for v in space}
            assert len(space) == 8
            lines = {tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(space-{0},2)}
            assert len(lines) == 7
            # Count 2-spaces globally, rather than comparing pairwise spans.
            assert used_lines.isdisjoint(lines)
            used_lines.update(lines)
        return {'code_size': len(s['codewords']), 'distinct_two_spaces': len(used_lines),
                'ambient_two_spaces': 127*126//6, 'counting_upper_bound': 381}
    if task == 'T042':
        selected = sorted(s['elements'])
        assert len(selected) == len(set(selected))
        assert all(type(x) is int and 1 <= x <= 212 for x in selected)
        # Enumerate endpoints, not the checker's first/middle pair.
        pairs = 0
        for a,c in itertools.combinations(selected,2):
            assert (a+c)%2 or (a+c)//2 not in selected
            pairs += 1
        return {'cardinality': len(selected), 'endpoint_pairs_checked': pairs}
    if task == 'T041':
        polygons = []
        sides = []
        for square in s['squares']:
            x,y,a,c,d = [F(square[k]) for k in ('x','y','side','cos','sin')]
            assert a > 0 and c*c+d*d == 1
            sides.append(a)
            polygon = [(x+a*(i*c-j*d)/2, y+a*(i*d+j*c)/2)
                       for i,j in ((-1,-1),(1,-1),(1,1),(-1,1))]
            assert all(0 <= u <= 1 and 0 <= v <= 1 for u,v in polygon)
            polygons.append(polygon)
        def turn(a,b,c):
            return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        checked = 0
        # Exact polygon clipping independently measures intersection area;
        # the task checker uses separating axes instead.
        for left,right in itertools.combinations(polygons,2):
            clipped = left[:]
            for a,b in zip(right,right[1:]+right[:1]):
                result = []
                if not clipped: break
                for u,v in zip(clipped,clipped[1:]+clipped[:1]):
                    tu,tv = turn(a,b,u),turn(a,b,v)
                    if tu >= 0: result.append(u)
                    if (tu < 0 <= tv) or (tv < 0 <= tu):
                        ratio = tu/(tu-tv)
                        result.append(tuple(u[k]+ratio*(v[k]-u[k]) for k in range(2)))
                clipped = result
            area2 = sum((u[0]*v[1]-u[1]*v[0] for u,v in
                         zip(clipped,clipped[1:]+clipped[:1])), F()) if clipped else F()
            assert area2 == 0
            checked += 1
        assert len(sides) == 17 and sum(a*a for a in sides) <= 1
        return {'sum_sides': str(sum(sides,F())), 'clipped_pairs': checked}
    if task == 'T040':
        count = config['parameters']['n']
        if 'points' in s:
            points = [tuple(map(F,p)) for p in s['points']]
        else:
            points = []
            for u,v in s['stereographic']:
                u,v = F(u),F(v)
                d = 1+u*u+v*v
                points.append((2*u/d,2*v/d,(1-u*u-v*v)/d))
        assert len(points) == len(set(points)) == count
        assert all(sum(x*x for x in p) == 1 for p in points)
        def det(a,b,c):
            return (a[0]*(b[1]*c[2]-b[2]*c[1])
                    -a[1]*(b[0]*c[2]-b[2]*c[0])
                    +a[2]*(b[0]*c[1]-b[1]*c[0]))
        def sub(a,b): return tuple(x-y for x,y in zip(a,b))
        center = tuple(sum(p[k] for p in points)/count for k in range(3))
        volume6 = F()
        facets = 0
        # For these saved runs verify that every hull facet is triangular.
        # Then sum exact tetrahedra from the interior centroid. This avoids
        # the checker's plane canonicalization and oriented boundary sum.
        for i,j,k in itertools.combinations(range(count),3):
            a,b,c = points[i],points[j],points[k]
            values = [det(sub(b,a),sub(c,a),sub(p,a)) for p in points]
            if not any(values): continue
            if all(v >= 0 for v in values) or all(v <= 0 for v in values):
                assert values.count(0) == 3, 'Independent audit requires triangular saved facets'
                volume6 += abs(det(sub(a,center),sub(b,center),sub(c,center)))
                facets += 1
        assert facets == 2 * count - 4
        return {'volume': str(volume6/6), 'centroid_pyramids': facets,
                'audit_scope': 'Saved simplicial witnesses; coplanar-face cases covered by task tests'}
    if task == 'T039':
        rows = s['rows']
        assert len(rows) == 7 and all(len(row) == 6 for row in rows)
        # Sorting all absolute differences independently checks both intra-row
        # and cross-row collisions, without the task's incremental set.
        differences = sorted(abs(a-b) for row in rows for a,b in itertools.combinations(row, 2))
        assert len(differences) == 105 and differences[0] > 0
        assert all(a < b for a,b in zip(differences, differences[1:]))
        return {'scope': differences[-1], 'distinct_positive_differences': 105,
                'sum_positive_differences': sum(differences)}
    if task == 'T038':
        squares = s['squares']
        # Convert to the equivalent strength-two orthogonal array. This single
        # projection test includes row/column Latin conditions and MOLS pairs.
        rows = [(i, j, *(square[i][j] for square in squares))
                for i in range(12) for j in range(12)]
        checked = 0
        for a, b in itertools.combinations(range(2+len(squares)), 2):
            assert {(row[a], row[b]) for row in rows} == set(itertools.product(range(12), repeat=2))
            checked += 1
        return {'square_count': len(squares), 'orthogonal_array_rows': 144,
                'two_column_projections_checked': checked}
    if task == 'T037':
        vectors = []
        for row in s['directions']:
            rational = list(map(F, row))
            assert len(rational) == 5
            denominator = math.lcm(*(x.denominator for x in rational))
            integer = [int(x*denominator) for x in rational]
            divisor = math.gcd(*integer)
            assert divisor > 0
            vectors.append(tuple(x//divisor for x in integer))
        checked = 0
        for u, v in itertools.combinations(vectors, 2):
            dot = sum(x*y for x, y in zip(u, v))
            # Integer homogeneous representatives: 2*dot is an integer, so
            # comparing it with floor(sqrt(norm_product)) is exact.
            product = sum(x*x for x in u)*sum(x*x for x in v)
            assert dot <= 0 or 2*dot <= math.isqrt(product)
            checked += 1
        return {'direction_count': len(vectors), 'integer_pair_checks': checked,
                'primitive_integer_directions': len(set(vectors))}
    if task == 'T036':
        points = [tuple(map(F, point)) for point in s['points']]
        def turn(a, b, c):
            return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        assert len(points) == 28 and len(set(points)) == 28
        assert all(turn(*triple) for triple in itertools.combinations(points, 3))
        convex = 0
        for subset in itertools.combinations(points, 4):
            ordered = sorted(subset)
            total = 0
            for order in (ordered, list(reversed(ordered))):
                chain = []
                for point in order:
                    while len(chain) >= 2 and turn(chain[-2], chain[-1], point) <= 0:
                        chain.pop()
                    chain.append(point)
                total += len(chain)-1
            convex += total == 4
        return {'crossings': convex, 'quadruples_checked': math.comb(28,4)}
    if task == 'T035':
        points = [tuple(map(F, point)) for point in s['points']]
        def turn(a, b, c):
            return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        assert len(set(points)) == len(points)
        assert all(turn(*triple) for triple in itertools.combinations(points, 3))
        convex_four = set()
        for indices in itertools.combinations(range(len(points)), 4):
            ordered = sorted(points[i] for i in indices)
            chains = []
            for order in (ordered, list(reversed(ordered))):
                hull = []
                for point in order:
                    while len(hull) >= 2 and turn(hull[-2], hull[-1], point) <= 0:
                        hull.pop()
                    hull.append(point)
                chains.append(hull)
            if len(chains[0])+len(chains[1])-2 == 4:
                convex_four.add(indices)
        checked = 0
        # Independent exhaustive subset certificate: a nonconvex set in general
        # position has a point in a triangle, hence a nonconvex four-subset.
        for subset in itertools.combinations(range(len(points)), 7):
            assert any(quad not in convex_four for quad in itertools.combinations(subset, 4))
            checked += 1
        return {'point_count': len(points), 'seven_subsets_checked': checked,
                'convex_four_subsets': len(convex_four), 'convex_seven_subsets': 0}
    if task == 'T034':
        colors = s['colors']
        assert s['n'] == len(colors)
        checked = 0
        # Enumerate by last term, independently of the task's start/step loops.
        for end in range(6, len(colors)):
            for step in range(1, end//6+1):
                assert len({colors[end-j*step] for j in range(7)}) == 2
                checked += 1
        return {'prefix_length': len(colors), 'arithmetic_progressions_checked': checked}
    if task == 'T033':
        raw = (ROOT / 'tasks/t033/data/source/G70').read_text().splitlines()
        n, m = map(int, raw[0].split())
        assert (n, m) == (10000, 9999)
        edges = [tuple(map(int, line.split())) for line in raw[1:] if line.strip()]
        assert len(edges) == m and all(w == 1 for _, _, w in edges)
        assert len(s['labels']) == n
        spins = [2*label-1 for label in s['labels']]
        energy = sum(w*spins[u-1]*spins[v-1] for u, v, w in edges)
        assert (sum(w for _, _, w in edges)-energy) % 2 == 0
        return {'cut_weight': (sum(w for _, _, w in edges)-energy)//2,
                'ising_energy': energy, 'original_edges_checked': m}
    if task == 'T032':
        matrix = s['matrix']
        checked = 0
        # The task uses row masks; this audit uses column triples and row sums.
        for columns in itertools.combinations(range(19), 3):
            common_rows = sum(all(matrix[row][col] == 1 for col in columns)
                              for row in range(14))
            assert common_rows < 3
            checked += 1
        return {'ones': sum(sum(row) for row in matrix),
                'column_triples_checked': checked, 'forbidden_submatrices': 0}
    if task == 'T030':
        directory = ROOT / 'tasks/t030/data'
        edges = set()
        for line in (directory / 'source/DSJC1000.5.col').read_text().splitlines():
            fields = line.split()
            if fields and fields[0] == 'e':
                u, v = map(lambda x: int(x)-1, fields[1:])
                edges.add(tuple(sorted((u, v))))
        instance = json.loads((directory / 'instance.json').read_text())
        assert len(edges) == 249826
        assert edges == {tuple(sorted(edge)) for edge in instance['edges']}
        groups = {}
        assert len(s['colors']) == 1000
        for vertex, color in enumerate(s['colors']):
            groups.setdefault(color, []).append(vertex)
        checked = 0
        for vertices in groups.values():
            for pair in itertools.combinations(vertices, 2):
                assert pair not in edges
                checked += 1
        return {'color_count': len(groups), 'within_color_pairs_checked': checked,
                'original_dimacs_edges_matched': len(edges)}
    if task == 'T031':
        word = s['word']
        # Test each required word by independent substring lookup, rather than
        # classifying the candidate's sliding windows as the task checker does.
        for permutation in itertools.permutations('1234567'):
            assert ''.join(permutation) in word
        assert set(word) == set('1234567')
        return {'string_length': len(word), 'required_substrings_checked': 5040}
    if task == 'T028':
        data = json.loads((ROOT /
            'tasks/t028/data/ta051.json').read_text())['processing_times']
        permutation = s['permutation']
        assert sorted(permutation) == list(range(1, 51))
        # Full table in machine order, separate from the rolling job-order checker.
        table = [[0]*51 for _ in range(21)]
        for machine in range(1, 21):
            for position in range(1, 51):
                table[machine][position] = max(table[machine-1][position],
                    table[machine][position-1]) + data[machine-1][permutation[position-1]-1]
        return {'makespan': table[20][50], 'operations': 1000}
    if task == 'T029':
        terms = [(list(map(F, term['alpha'])), list(map(F, term['beta'])),
                  list(map(F, term['gamma']))) for term in s['terms']]
        # All pairs of input basis matrices determine a bilinear map exactly.
        checked = 0
        for a_index in range(9):
            for b_index in range(9):
                output = [F(0)]*9
                for a, b, g in terms:
                    product = a[a_index]*b[b_index]
                    output = [v + product*c for v, c in zip(output, g)]
                expected = [0]*9
                a_row, a_col = divmod(a_index, 3)
                b_row, b_col = divmod(b_index, 3)
                if a_col == b_row:
                    expected[3*a_row+b_col] = 1
                assert output == expected
                checked += 9
        return {'rank_terms': len(terms), 'basis_pairs': 81,
                'output_coefficients_checked': checked}
    if task == 'T027':
        values = list(map(int, (ROOT /
            'tasks/t027/data/tai256c.dat').read_text().split()))
        n = values[0]
        assert n == 256 and len(values) == 1+2*n*n
        a, b = values[1:1+n*n], values[1+n*n:]
        permutation = s['permutation']
        assert sorted(permutation) == list(range(n))
        inverse = [0]*n
        for facility, location in enumerate(permutation):
            inverse[location] = facility
        # Sum in location order, independently of the checker's facility order.
        cost = sum(b[u*n+v] * a[inverse[u]*n+inverse[v]]
                   for u in range(n) for v in range(n))
        return {'quadratic_cost': cost, 'terms': n*n,
                'inverse_permutation_checked': True}
    if task == 'T026':
        colors = s['colors']
        n = len(colors)
        assert s['n'] == n
        checked = 0
        for x in range(1,n+1):
            for y in range(x,n+1):
                if x+y <= n:
                    assert not (colors[x-1] == colors[y-1] == colors[x+y-1])
                checked += 1
        return {'prefix_length': n, 'pairs_including_equal': checked,
                'monochromatic_sums': 0}
    if task == 'T025':
        points = s['points']
        assert all(len(point) == 7 for point in points)
        checked = 0
        for a, b, c in itertools.combinations(points, 3):
            assert any((x+y+z) % 3 for x,y,z in zip(a,b,c))
            checked += 1
        return {'points': len(points), 'triples_checked': checked,
                'affine_lines': 0}
    if task == 'T024':
        neighbors = [set(row) for row in s['adjacency']]
        assert len(neighbors) == config['parameters']['vertices']
        checked = 0
        for a, b, c, d in itertools.combinations(range(len(neighbors)), 4):
            for u, v, w, x in ((a,b,c,d), (a,b,d,c), (a,c,b,d)):
                assert not (v in neighbors[u] and w in neighbors[v]
                            and x in neighbors[w] and u in neighbors[x])
            checked += 1
        return {'edges': sum(len(row) for row in neighbors)//2,
                'four_subsets_checked': checked, 'four_cycles': 0}
    if task == 'T021':
        points = []
        for u, v in s['points']:
            u, v = F(u), F(v)
            denominator = 1 + u*u + v*v
            point = (2*u/denominator, 2*v/denominator, (1-u*u-v*v)/denominator)
            assert sum(x*x for x in point) == 1
            points.append(point)
        assert len(points) == config['parameters']['n']
        scale = 10**35
        total, pairs = 0, 0
        distances = []
        for a, b in itertools.combinations(points, 2):
            distance = sum((x-y)**2 for x, y in zip(a, b))
            assert distance > 0
            distances.append(distance)
            reciprocal = 1/distance
            # Integer division before isqrt gives floor(scale/sqrt(distance)).
            total += math.isqrt(reciprocal.numerator * scale**2 // reciprocal.denominator)
            pairs += 1
        return {'energy_interval': [str(F(total, scale)), str(F(total+pairs, scale))],
                'pairs': pairs, 'minimum_squared_distance': str(min(distances)),
                'unit_sphere_equations_exact': True}
    if task == 'T022':
        adjacency = [set(row) for row in s['adjacency']]
        count = 0
        for subset in itertools.combinations(range(len(adjacency)), 5):
            edge_count = sum(v in adjacency[u] for u, v in itertools.combinations(subset, 2))
            assert 0 < edge_count < 10
            count += 1
        return {'vertices': len(adjacency), 'edges': sum(map(len, adjacency))//2,
                'five_subsets_checked': count, 'forbidden_subsets': 0}
    if task == 'T023':
        parameters = config['parameters']
        array = s['array']
        required = set(itertools.product(range(parameters['alphabet_size']),
                                         repeat=parameters['strength']))
        count = 0
        for columns in itertools.combinations(range(parameters['columns']), parameters['strength']):
            assert {tuple(row[c] for c in columns) for row in array} == required
            count += 1
        return {'rows': len(array), 'column_subsets': count,
                'required_tuples_per_subset': len(required)}
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
    if task == "T003":
        return {"sum_radii": str(sum((F(c['r']) for c in s['circles']),F(0)))}
    if task == "T004":
        import mpmath as mp
        with mp.workdps(80):
            p=[[mp.mpf(str(F(x).numerator))/F(x).denominator for x in v] for v in s['points']]
            cosine=max(sum(x*y for x,y in zip(a,b))/mp.sqrt(sum(x*x for x in a)*sum(y*y for y in b)) for a,b in itertools.combinations(p,2))
            return {"minimum_angle_80_digits": mp.nstr(mp.acos(cosine),80)}
    if task == "T005":
        p=[[F(x) for x in v] for v in s['points']]
        area=min(abs(a[0]*b[1]+b[0]*c[1]+c[0]*a[1]-a[1]*b[0]-b[1]*c[0]-c[1]*a[0])/2 for a,b,c in itertools.combinations(p,3))
        if config is None or config['id']=='T005-C01': assert area==F(1,27)
        return {"minimum_triangle_area":str(area),"triangles":math.comb(len(p),3)}
    if task == "T006":
        import networkx as nx
        parameters = config['parameters']
        g=nx.Graph();g.add_nodes_from(range(s['vertices']));g.add_edges_from(s['edges'])
        assert nx.is_connected(g) and set(dict(g.degree()).values())=={parameters['degree']}
        girth=nx.girth(g); assert girth>=parameters['girth']
        return {"order":len(g),"networkx_girth":girth}
    if task == "T007":
        differences=[abs(a-b) for a,b in itertools.combinations(s['marks'],2)]
        expected=math.comb(len(s['marks']),2)
        assert len(differences)==len(set(differences))==expected and min(differences)>0
        return {"distinct_positive_differences":expected,"span":max(s['marks'])-min(s['marks'])}
    if task == "T012":
        a=s['set']; ns=len({x+y for x,y in itertools.product(a,repeat=2)});nd=len({x-y for x,y in itertools.product(a,repeat=2)})
        return {"cardinality":len(a),"sumset":ns,"difference_set":nd,"ratio":math.log(ns/len(a))/math.log(nd/len(a))}
    if task == "T008":
        params = config['parameters']
        v, k, t = (params[name] for name in ('v', 'k', 't'))
        blocks = s['blocks']
        assert all(len(set(block)) == k and all(0 <= x < v for x in block)
                   for block in blocks)
        masks = [sum(1 << x for x in block) for block in blocks]
        for subset in itertools.combinations(range(v), t):
            mask = sum(1 << x for x in subset)
            assert any(mask & block == mask for block in masks)
        return {"blocks": len(masks), "subsets_checked": math.comb(v, t), "subset_size": t}
    if task == "T009":
        params = config['parameters']
        matrix = s['generator_matrix']
        assert len(matrix) == params['k'] and all(len(row) == params['n'] for row in matrix)
        rows=[sum(x<<i for i,x in enumerate(row)) for row in matrix]
        space={0}
        for row in rows: space |= {x^row for x in list(space)}
        assert len(space)==1<<params['k']
        return {"codewords":len(space),"minimum_distance":min(x.bit_count() for x in space if x)}
    if task == "T010":
        params = config['parameters']
        words = s['codewords']
        assert len(words) == len(set(words))
        assert all(type(word) is int and 0 <= word < 1 << params['n'] for word in words)
        d = min(((a ^ b).bit_count() for a, b in itertools.combinations(words, 2)), default=None)
        assert d is None or d >= params['distance']
        return {"codewords":len(words),"minimum_distance":d}
    if task == "T013":
        a=s['sequence']; bits=sum((x==1)<<i for i,x in enumerate(a))
        correlations=[len(a)-k-2*((bits^(bits>>k))&((1<<(len(a)-k))-1)).bit_count() for k in range(1,len(a))]
        return {"energy":sum(x*x for x in correlations),"lags":len(correlations)}
    if task in ('T014','T015','T016'):
        a=[F(x) for x in s['coefficients']];b=[F(0)]*(2*len(a)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(a): b[i+j]+=x*y
        mass=sum(a)
        if task=='T015': value=(2*sum(x*x for x in b)+sum(x*y for x,y in zip(b,b[1:])))/(3*max(b)*mass*mass)
        else: value=2*len(a)*max(abs(x) for x in b)/(mass*mass)
        return {"exact_objective":str(value),"convolution_entries":len(b)}
    if task == 'T017':
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
    if task == 'T011':
        words=s['words']
        q = config['parameters']['q']
        power = config['parameters']['power']
        assert all(len(word) == power and all(0 <= x < q for x in word) for word in words)
        for a,b in itertools.combinations(words,2): assert any((x-y)%q not in (0,1,q-1) for x,y in zip(a,b))
        return {"independent_words":len(words),"pairs":len(words)*(len(words)-1)//2}
    if task == 'T018':
        from sympy import Matrix
        return {"absolute_determinant":str(abs(Matrix(s['matrix']).det(method='domain-ge')))}
    if task == 'T019':
        a = s['tuple']
        count = config['parameters']['k']
        assert len(a) == len(set(a)) == count
        primes = [p for p in range(2, count + 1)
                  if all(p % d for d in range(2, math.isqrt(p) + 1))]
        missing = {}
        for prime in primes:
            residues = {x % prime for x in a}
            missing[str(prime)] = next(r for r in range(prime) if r not in residues)
        return {"diameter":max(a)-min(a),"primes":len(primes),"missing_residues":missing}
    if task == 'T020':
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
    if task=='T099': s['placements'][0]['x']=s['width']
    elif task=='T100': s['edges'].append(list(s['edges'][0]))
    elif task=='T098': s['squares'][0][0]=s['side']
    elif task=='T096':
        s.update(rho={'constant':'1','cos':['0','1/2'],'sin':['0','0']},trial={'constant':'1','cos':[],'sin':[]},rho_lower_bound='3/2',series_terms=0)
    elif task=='T095': s['edges'].append(dict(s['edges'][0]))
    elif task=='T094': s['edges']=s['edges'][:-1]
    elif task=='T097': s['polygons']=[]
    elif task=='T092': s['coefficients']=[1]+[0]*230
    elif task=='T093':
        s['item_indices']=[0];s['x_translations']=[10**15];s['y_translations']=[0]
    elif task=='T091': s['rows'][0]^=1
    elif task=='T090': s['sequence'][0]=0
    elif task=='T089': s['coefficients']=[1]
    elif task=='T088': s['ordering'][0]=s['ordering'][1]
    elif task=='T087': s['heights']=[0]*480
    elif task=='T085': s['radius']='100'
    elif task=='T086': s['matrices'][0][0][0]=[-1,0]
    elif task=='T084': s['elements'][1]=s['elements'][0]
    elif task=='T083': s['triangles'][1]=s['triangles'][0]
    elif task=='T082': s['black'][0]=s['white'][0]
    elif task in ('T014','T015','T016'): s['coefficients']=[0]*len(s['coefficients'])
    elif task=='T026': s['colors']=[0]*len(s['colors'])
    elif task in ('T027','T028'): s['permutation'][1]=s['permutation'][0]
    elif task=='T029': s['terms'][1]=s['terms'][0]
    elif task=='T031': s['word']='1234567'
    elif task=='T030': s['colors']=[0]*len(s['colors'])
    elif task=='T033': s['labels'][0]=2
    elif task=='T034': s.update(n=7, colors=[0]*7)
    elif task=='T035': s['points']=[[i,i*i] for i in range(7)]
    elif task=='T036': s['points'][1]=s['points'][0]
    elif task=='T037': s['directions'][1]=s['directions'][0]
    elif task=='T038': s['squares'].append(s['squares'][0])
    elif task=='T072': s['elements'][1]=s['elements'][0]
    elif task=='T071': s['codewords']=[0,1]
    elif task=='T070': s['squares'].append(s['squares'][0])
    elif task=='T069': s['tour'][1]=s['tour'][0]
    elif task=='T068': s['codewords']=[]
    elif task=='T067': s['codewords']=['00000000000011111','00000000000101111']
    elif task=='T066': s['points'][1]=s['points'][0]
    elif task=='T079': s['lines'][1]=s['lines'][0]
    elif task=='T078': s['gram'][0][0]=0
    elif task in ('T077','T080'): s['set'][1]=s['set'][0]
    elif task=='T075': s['edges']=[[0,1,2],[0,1,3],[0,2,3]]
    elif task=='T076': s['elements']=[1,2,3]+[2**i for i in range(3,15)]
    elif task in ('T073','T074','T081','T065'): s['points'][1]=s['points'][0]
    elif task=='T064': s['edges'].pop()
    elif task=='T062': s['elements']=[1,2]
    elif task=='T063': s['coefficients_ascending']=[0]*101
    elif task=='T061': s['edges']=[[i,(i+1)%6] for i in range(6)]
    elif task=='T060': s['expression']+=' + 1'
    elif task=='T058': s['rounds'].append(s['rounds'][0])
    elif task=='T059': s['vertices'].append(s['vertices'][0])
    elif task=='T057': s['routes'].append(s['routes'][0][:])
    elif task=='T055': s['assignment']=[False]*1630
    elif task=='T056': s['machine_orders'][0][1]=s['machine_orders'][0][0]
    elif task=='T054': s['sequence'][0]=0
    elif task=='T053': s['factors'][0]*=2
    elif task=='T051': s['sequence']=[1]*4
    elif task=='T052': s['codewords']=[list(range(12)),list(range(12))]
    elif task=='T050': s['vertices']=[0,1,3,2]
    elif task=='T049': s['points'][1]=s['points'][0]
    elif task=='T048': s['comparators']=[]
    elif task=='T047': s['basis']=[0,6166]
    elif task=='T046': s['coefficients']=[0]
    elif task=='T045': s['ordering'][1]=s['ordering'][0]
    elif task=='T044': s['edges'].append([0,0])
    elif task=='T043': s['codewords']=[ [1,2,4], [1,2,8] ]
    elif task=='T042': s['elements']=[1,2,3]
    elif task=='T041': s['squares'][1]=s['squares'][0]
    elif task=='T040':
        key='points' if 'points' in s else 'stereographic'
        s[key][1]=s[key][0]
    elif task=='T039': s['rows'][0][1]=s['rows'][0][0]
    elif task=='T032':
        for i in range(3):
            for j in range(3): s['matrix'][i][j]=1
    elif task=='T017': s['heights'][0]='2'
    elif task=='T001': s['centers'][1]=s['centers'][0]
    elif task=='T003': s['circles'][1]=s['circles'][0]
    elif task=='T002': s['squares'][1]=s['squares'][0]
    elif task in ('T004','T021','T005','T025'): s['points'][1]=s['points'][0]
    elif task in ('T024','T022'): s['adjacency']=[[1]]
    elif task=='T023': s['array']=[]
    elif task=='T006': s['edges'].pop()
    elif task=='T008': s['blocks']=[]
    elif task=='T009': s['generator_matrix'][1]=s['generator_matrix'][0]
    elif task=='T010': s['codewords'].append(s['codewords'][0])
    elif task=='T018': s['matrix'][0][0]=0
    elif task=='T013': s['sequence'][0]=0
    else:
        key={'T007':'marks','T012':'set','T011':'words','T019':'tuple','T020':'chain'}[task]
        s[key][1]=s[key][0]
    return s
