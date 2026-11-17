"""Bounded classical local search with exact-feasible grid fallback."""
import os, random
from fractions import Fraction
from tasks.t003.check import validate, Q
from tasks.t003.init_program import run_code as initial

def run_code():
    cid=os.environ.get('MATHBENCH_CONFIG_ID','T003-C01')
    if cid != 'T003-C01': raise ValueError('unknown T003 configuration')
    n=26
    best=initial(); config={'parameters':{'n':n}}
    rng=random.Random(int(os.environ.get('MATHBENCH_SEED','0')))
    for _ in range(40):
        candidate={'squares':[dict(s) for s in best['squares']]}
        i=rng.randrange(n); sq=candidate['squares'][i]
        sq['x']=str(Fraction(sq['x'])+Fraction(rng.randrange(-2,3),1000))
        sq['y']=str(Fraction(sq['y'])+Fraction(rng.randrange(-2,3),1000))
        try:
            if Q.parse(validate(candidate,config)['objective']) < Q.parse(validate(best,config)['objective']): best=candidate
        except ValueError: pass
    return best
