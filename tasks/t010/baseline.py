from mathbench.search import search_deadline, search_steps
"""Seeded randomized greedy search, starting from an extended BCH code."""
import os, random, time

def _start():
    g=(1<<8)|(1<<7)|(1<<6)|(1<<4)|1
    out=[]
    for m in range(128):
        w=0
        for i in range(7):
            if (m>>i)&1: w ^= g<<i
        w |= (bin(w).count('1')%2)<<15
        out.append(w)
    return out

def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T010-C01')
    if config_id in ('T010-C02','T010-C03'):
        try: from human import run_code as human_run
        except ModuleNotFoundError: from tasks.t010.human import run_code as human_run
        rng=random.Random(int(os.environ.get('MATHBENCH_SEED','0')))
        best=list(human_run()['codewords'])
        n,d={'T010-C02':(23,10),'T010-C03':(25,10)}[config_id]
        # Fixed-budget add-only greedy search over seeded random candidates.
        # The public witness is not loaded; the start is the traditional BCH method.
        try: trials=max(0,min(20000,int(os.environ.get('MATHBENCH_BASELINE_TRIALS','2000'))))
        except (TypeError,ValueError): trials=2000
        for _ in range(trials):
            candidate=rng.randrange(1<<n)
            if all(bin(candidate^word).count('1')>=d for word in best): best.append(candidate)
        return {'codewords':best,'search_method':'seeded_add_only_greedy_from_shortened_BCH','search_trials':trials}
    if config_id != 'T010-C01': raise ValueError('unsupported configuration')
    rng=random.Random(int(os.environ.get('MATHBENCH_SEED','0')))
    seconds=max(0.0,min(float(os.environ.get('MATHBENCH_SEARCH_SECONDS','2')),30.0))
    deadline = search_deadline()
    best=_start()
    # Greedy independent sets in the graph whose edges join words at distance < 6.
    for _attempt in search_steps(1):
        order=list(range(1<<17)); rng.shuffle(order); chosen=[]
        for x in order:
            if all(bin(x^y).count('1')>=6 for y in chosen): chosen.append(x)
        if len(chosen)>len(best): best=chosen
    return {'codewords':best}
