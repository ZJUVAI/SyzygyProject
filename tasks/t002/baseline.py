"""Bounded classical local search with exact-feasible grid fallback."""
import os, random
from fractions import Fraction
from tasks.t002.check import validate, Q
from tasks.t002.init_program import run_code as initial

def run_code():
    cid=os.environ.get('MATHBENCH_CONFIG_ID','T002-C01')
    n={'T002-C01':26,'T002-C03':29,'T002-C04':38}.get(cid)
    if n is None: raise ValueError('unknown T002 configuration')
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
