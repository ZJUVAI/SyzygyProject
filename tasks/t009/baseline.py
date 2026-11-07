from mathbench.search import search_deadline, search_steps
"""Bounded simulated annealing on systematic binary generator matrices."""
import math
import os
import random
import time

N, K = 68, 15


def _make_systematic(seed, n=N, k=K):
    rng = random.Random(seed)
    rows=[]
    for i in range(k):
        row=1 << i
        for j in range(k, n):
            if rng.getrandbits(1):
                row |= 1 << j
        rows.append(row)
    return rows


def _distance(rows, n=N, k=None):
    """Exact minimum weight over all nonzero linear combinations."""
    k = len(rows) if k is None else k
    words=[0] * (1 << k)
    best=n+1
    for mask in range(1, 1 << k):
        bit=mask & -mask
        index=bit.bit_length()-1
        words[mask]=words[mask ^ bit] ^ rows[index]
        weight=bin(words[mask]).count('1')
        if weight < best:
            best=weight
    return best


def _mutate_parity(rows, rng, max_flips=4, n=N, k=K):
    """Flip 1..max_flips entries in P of [I|P], preserving rank."""
    candidate=rows[:]
    count=rng.randint(1, max_flips)
    for _ in range(count):
        row=rng.randrange(k)
        col=rng.randrange(k, n)
        candidate[row] ^= 1 << col
    return candidate


def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T009-C01')
    if config_id == 'T009-C02': n,k=80,20
    elif config_id == 'T009-C03': n,k=100,20
    elif config_id == 'T009-C01': n,k=N,K
    else: raise ValueError('unsupported configuration')
    seed=int(os.environ.get('MATHBENCH_SEED','0'))
    rng=random.Random(seed)
    current=_make_systematic(seed,n,k)
    current_d=_distance(current,n,k)
    best=current[:]
    best_d=current_d
    budget=max(0.0, min(float(os.environ.get('MATHBENCH_SEARCH_SECONDS','2')), 30.0))
    deadline = search_deadline()
    steps=0
    attempts = 5 if config_id != 'T009-C01' else 60
    steps=0
    for _attempt in search_steps(attempts):
        candidate=_mutate_parity(current, rng, n=n, k=k)
        candidate_d=_distance(candidate,n,k)
        steps += 1
        steps += 1
        if candidate_d > best_d:
            best,best_d=candidate[:],candidate_d
        # A cooling schedule permits occasional downhill moves to escape plateaus.
        temperature=max(0.15, 2.0 * (1.0 - min(steps, 200) / 200.0))
        delta=candidate_d-current_d
        if delta >= 0 or rng.random() < math.exp(delta/temperature):
            current,current_d=candidate,candidate_d
    matrix=[[((row >> j) & 1) for j in range(n)] for row in best]
    return {'generator_matrix':matrix, 'search_metadata': {
        'algorithm':'simulated annealing over systematic parity matrices',
        'iterations':steps, 'seed':seed}}
