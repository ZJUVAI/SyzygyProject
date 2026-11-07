"""Main review of short vectors after an independent integral basis change."""
from fractions import Fraction as F
from math import isqrt


def audit(solution):
    gram=[[F(v) for v in row] for row in solution['gram']]
    assert len(gram)==10 and all(len(row)==10 for row in gram)
    assert all(gram[i][j]==gram[j][i] for i in range(10) for j in range(10))
    # Change the integral lattice basis; this is not the formal checker's basis.
    u=[[int(i==j)-int(j==i+1) for j in range(10)] for i in range(10)]
    g=[[sum(u[a][i]*gram[a][b]*u[b][j] for a in range(10) for b in range(10)) for j in range(10)] for i in range(10)]
    # Independent Gaussian elimination determinant (not product from LDL).
    work=[row[:] for row in g];det=F(1)
    for i in range(10):
        pivot=work[i][i];assert pivot>0;det*=pivot
        for j in range(i+1,10):
            scale=work[j][i]/pivot
            for k in range(i+1,10):work[j][k]-=scale*work[i][k]
    lower=[[F(i==j) for j in range(10)] for i in range(10)];diagonal=[]
    for i in range(10):
        diagonal.append(g[i][i]-sum(lower[i][k]**2*diagonal[k] for k in range(i)))
        assert diagonal[-1]>0
        for j in range(i+1,10):lower[j][i]=(g[j][i]-sum(lower[j][k]*lower[i][k]*diagonal[k] for k in range(i)))/diagonal[i]
    z=[0]*10;count=0;nodes=0
    def enumerate_remaining(i,left):
        nonlocal count,nodes
        nodes+=1
        if i<0:
            if any(z):
                assert sum(z[a]*g[a][b]*z[b] for a in range(10) for b in range(10))==4
                count+=1
            return
        center=-sum(lower[j][i]*z[j] for j in range(i+1,10))
        bound=left/diagonal[i];radius=isqrt(bound.numerator//bound.denominator)+1
        base=center.numerator//center.denominator
        for v in range(base-radius,base+radius+2):
            remainder=left-diagonal[i]*(v-center)**2
            if remainder>=0:
                z[i]=v;enumerate_remaining(i-1,remainder)
    enumerate_remaining(9,F(4))
    return {'determinant':str(det),'vectors_with_squared_norm_at_most4':count,'nodes':nodes,'method':'independent unitriangular integer basis change, Gaussian determinant, complete exact ellipsoid enumeration'}
