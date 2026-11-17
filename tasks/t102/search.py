"""Shared seeded rational mutation search for T102."""
from fractions import Fraction
import os
import random
try:
    from .check import validate
except ImportError:
    from check import validate

GRID=[Fraction(i,12) for i in range(13)]

def search(iterations):
    seed=int(os.environ.get("MATHBENCH_SEED","0"))
    rng=random.Random(seed)
    pairs=[[Fraction(1,4),Fraction(1,4)] for _ in range(15)]
    cfg={"id":"T102-C01","parameters":{"m":15},"direction":"maximize"}
    def score(candidate):
        witness={"pairs":[[str(u),str(v)] for u,v in candidate]}
        return Fraction(validate(witness,cfg)["objective"])
    best_score=score(pairs)
    accepted=0
    for _ in range(iterations):
        i=rng.randrange(15); u=rng.choice(GRID); v=rng.choice(GRID)
        if u+v>1: continue
        trial=[pair[:] for pair in pairs]; trial[i]=[u,v]
        trial_score=score(trial)
        if trial_score>best_score:
            pairs,best_score=trial,trial_score
            accepted+=1
    return {"pairs":[[str(u),str(v)] for u,v in pairs],"claimed_objective":str(best_score),"search_metadata":{"algorithm":"seeded heterogeneous rational coordinate mutation with exact checker feedback","seed":seed,"iterations":iterations,"accepted_moves":accepted,"reference_data_read":False}}
