"""Exact Q(sqrt(2)) checker for rational-angle parameterized unit squares."""
from fractions import Fraction
import math

class Q:
    __slots__=('a','b')
    def __init__(self,a=0,b=0): self.a,self.b=Fraction(a),Fraction(b)
    @staticmethod
    def parse(v):
        if isinstance(v,Q): return v
        if type(v) is int: return Q(v)
        if isinstance(v,float):
            if not math.isfinite(v): raise ValueError('non-finite number')
            return Q(Fraction.from_float(v))
        if not isinstance(v,str): raise ValueError('coordinates must be finite numbers or exact strings')
        s=v.replace(' ','')
        if 'sqrt2' not in s:
            try: return Q(Fraction(s))
            except Exception as e: raise ValueError('invalid exact number') from e
        # Accepted form: rational + rational*sqrt2 (for example 3/2+1/2*sqrt2).
        s=s.replace('-sqrt2','-1*sqrt2').replace('+sqrt2','+1*sqrt2')
        if s.startswith('sqrt2'): s='1*'+s
        if s.startswith('-sqrt2'): s='-1*sqrt2'
        parts=[]; start=0
        for i in range(1,len(s)):
            if s[i] in '+-' and s[i-1] not in 'eE': parts.append(s[start:i]); start=i
        parts.append(s[start:]); a=Fraction(0); b=Fraction(0)
        for term in parts:
            if not term: continue
            if term.endswith('*sqrt2') and term.count('sqrt2')==1:
                coef=term.split('*sqrt2')[0]; b+=Fraction(coef or '1')
            elif term=='sqrt2': b+=1
            elif term=='-sqrt2': b-=1
            elif 'sqrt2' in term: raise ValueError('invalid quadratic number')
            else: a+=Fraction(term)
        return Q(a,b)
    def __add__(x,y): y=Q.parse(y); return Q(x.a+y.a,x.b+y.b)
    __radd__=__add__
    def __neg__(x): return Q(-x.a,-x.b)
    def __sub__(x,y): return x+-Q.parse(y)
    def __rsub__(x,y): return Q.parse(y)+-x
    def __mul__(x,y): y=Q.parse(y); return Q(x.a*y.a+2*x.b*y.b,x.a*y.b+x.b*y.a)
    __rmul__=__mul__
    def __truediv__(x,y):
        y=Q.parse(y); d=y.a*y.a-2*y.b*y.b
        if not d: raise ZeroDivisionError
        return Q((x.a*y.a-2*x.b*y.b)/d,(x.b*y.a-x.a*y.b)/d)
    def __rtruediv__(x,y): return Q.parse(y)/x
    def sign(x):
        if x.a==0: return (x.b>0)-(x.b<0)
        if x.b==0: return (x.a>0)-(x.a<0)
        if x.a>0 and x.b>0: return 1
        if x.a<0 and x.b<0: return -1
        z=x.a*x.a-2*x.b*x.b
        if x.a>0: return (z>0)-(z<0)
        return -((z>0)-(z<0))
    def __le__(x,y): return (x-Q.parse(y)).sign()<=0
    def __lt__(x,y): return (x-Q.parse(y)).sign()<0
    def __eq__(x,y):
        try: y=Q.parse(y)
        except ValueError: return False
        return x.a==y.a and x.b==y.b
    def __str__(x):
        def f(z): return str(z.numerator) if z.denominator==1 else f'{z.numerator}/{z.denominator}'
        if x.b==0: return f(x.a)
        return f'{f(x.a)}{("+" if x.b>0 else "")}{f(x.b)}*sqrt2'

def corners(sq):
    if not isinstance(sq,dict) or not {'x','y','t'}<=set(sq): raise ValueError('each square needs x, y, t')
    x,y,t=(Q.parse(sq[k]) for k in ('x','y','t'))
    den=1+t*t; c=(1-t*t)/den; s=2*t/den
    u=(c/2,s/2); v=(-s/2,c/2)
    return [(x+a*u[0]+b*v[0],y+a*u[1]+b*v[1]) for a,b in ((-1,-1),(1,-1),(1,1),(-1,1))]

def separated(a,b):
    for poly in (a,b):
        for i,p in enumerate(poly):
            q=poly[(i+1)%4]; axis=(q[1]-p[1],p[0]-q[0])
            pa=[x*axis[0]+y*axis[1] for x,y in a]; pb=[x*axis[0]+y*axis[1] for x,y in b]
            if max(pa)<=min(pb) or max(pb)<=min(pa): return True
    return False

def _min(values):
    out=values[0]
    for v in values[1:]:
        if v<out: out=v
    return out

def _max(values):
    out=values[0]
    for v in values[1:]:
        if out<v: out=v
    return out

def validate(solution,config,strict=False):
    n=config.get('parameters',{}).get('n')
    if type(n) is not int or n not in (26,29,38) or config.get('parameters')!={'n':n}: raise ValueError('unsupported configuration')
    if not isinstance(solution,dict) or not isinstance(solution.get('squares'),(list,tuple)): raise ValueError('solution must contain squares')
    raw=solution['squares']
    if len(raw)!=n: raise ValueError(f'expected exactly {n} squares')
    polys=[corners(s) for s in raw]
    for i in range(n):
        for j in range(i):
            if not separated(polys[i],polys[j]): raise ValueError('square interiors overlap')
    points=[p for poly in polys for p in poly]
    xmin=_min([p[0] for p in points]); xmax=_max([p[0] for p in points])
    ymin=_min([p[1] for p in points]); ymax=_max([p[1] for p in points])
    side=_max([xmax-xmin,ymax-ymin])
    # Bound sqrt(2) by adjacent rationals using integer square root.
    scale=10**60; root=math.isqrt(2*scale*scale)
    low,high=Fraction(root,scale),Fraction(root+1,scale)
    lower=side.a+side.b*(low if side.b>=0 else high)
    upper=side.a+side.b*(high if side.b>=0 else low)
    return {'objective':str(side),'objective_value':str(upper),'verification_status':'certified' if strict else 'exact','details':{'objective_interval':[str(lower),str(upper)],'n':n,'bounding_width':str(xmax-xmin),'bounding_height':str(ymax-ymin),'pair_checks':n*(n-1)//2}}
