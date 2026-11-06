from mathbench.search import search_deadline, search_steps
"""Seeded local edits; this search does not read the human witness."""
import os, random, time
from tasks.t079.init_program import run_code as initial
from fractions import Fraction

def _score(a):
    mass=sum(a); return Fraction(416)*max(sum((a[i]*a[k-i] for i in range(max(0,k-207),min(207,k)+1)),Fraction(0)) for k in range(415))/(mass*mass)

def run_code():
    rng=random.Random(int(os.environ.get("MATHBENCH_SEED","0")))
    best=[Fraction(x) for x in initial()["coefficients"]]; score=_score(best)
    deadline = search_deadline()
    for _attempt in search_steps(20):
        cand=best[:]; i=rng.randrange(208); cand[i]=max(Fraction(0),cand[i]+rng.randint(-100,100))
        if not any(cand): continue
        value=_score(cand)
        if value<score: best,score=cand,value
    return {"coefficients":[str(x) for x in best]}
