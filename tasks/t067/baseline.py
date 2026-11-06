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
    if os.environ.get('MATHBENCH_CONFIG_ID','T067-C01') != 'T067-C01': raise ValueError('unsupported configuration')
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
