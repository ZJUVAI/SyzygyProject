"""Independent closed-form Rayleigh and Parseval audit for saved oval witnesses."""
from fractions import Fraction as F
from math import isqrt


def sqrt_interval(v):
    assert v>0;S=10**65;k=isqrt(v.numerator*S*S//v.denominator);lo=F(k,S)
    return lo,lo if lo*lo==v else F(k+1,S)


def coefficients(spec):
    c=F(spec['constant']);a=list(map(F,spec['cos']));b=list(map(F,spec['sin']));assert len(a)==len(b)
    return c,{i+1:(u,v) for i,(u,v) in enumerate(zip(a,b)) if u or v}


def audit(s):
    mean,rho=coefficients(s['rho']);c,f=coefficients(s['trial']);delta=F(s['rho_lower_bound'])
    assert mean==1 and 1 not in rho and delta>0
    if not rho:
        assert delta<=1
        den=c*c+sum(((a*a+b*b)/2 for a,b in f.values()),F(0));assert den>0
        num=c*c+sum(((n*n+1)*(a*a+b*b)/2 for n,(a,b) in f.items()),F(0))
        value=num/den
        return {'ratio_interval':[str(value),str(value)],'method':'Exact circle Parseval sum of Fourier energy weights n^2+1; no reciprocal series or angular sampling.'}
    assert set(rho)<={2} and set(f)<={1},'Independent saved-witness formula covers second-harmonic rho and first-harmonic trial functions.'
    a,b=rho.get(2,(F(0),F(0)));u,v=f.get(1,(F(0),F(0)));r=a*a+b*b
    assert r<1 and delta<=1 and (1-delta)**2>=r
    den=c*c+(u*u+v*v)/2+a*(u*u-v*v)/4+b*u*v/2;assert den>0
    numerator=c*c+u*u+v*v;rootlo,roothi=sqrt_interval(1-r)
    lo=numerator/(den*roothi);hi=numerator/(den*rootlo)
    return {'ratio_interval':[str(lo),str(hi)],'denominator':str(den),'reciprocal_radius_mean_squared':str(1/(1-r)),'method':'Closed integral avg(1/(1+a*cos2theta+b*sin2theta))=1/sqrt(1-a^2-b^2), odd-harmonic cancellation and exact trial denominator; no geometric reciprocal expansion.'}
