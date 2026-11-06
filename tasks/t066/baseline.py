from mathbench.search import search_deadline, search_steps
"""Bounded simulated annealing on systematic binary generator matrices."""
import math
import os
import random
import time

N, K = 68, 15


def _make_systematic(seed):
    rng = random.Random(seed)
    rows=[]
    for i in range(K):
        row=1 << i
        for j in range(K, N):
            if rng.getrandbits(1):
                row |= 1 << j
        rows.append(row)
    return rows


def _distance(rows):
    """Exact minimum weight over all nonzero linear combinations."""
    words=[0] * (1 << K)
    best=N+1
    for mask in range(1, 1 << K):
        bit=mask & -mask
        index=bit.bit_length()-1
        words[mask]=words[mask ^ bit] ^ rows[index]
        weight=bin(words[mask]).count('1')
        if weight < best:
            best=weight
    return best


def _mutate_parity(rows, rng, max_flips=4):
    """Flip 1..max_flips entries in P of [I|P], preserving rank."""
    candidate=rows[:]
    count=rng.randint(1, max_flips)
    for _ in range(count):
        row=rng.randrange(K)
        col=rng.randrange(K, N)
        candidate[row] ^= 1 << col
    return candidate


def run_code():
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T066-C01')
    if config_id != 'T066-C01':
        raise ValueError('unsupported configuration')
    seed=int(os.environ.get('MATHBENCH_SEED','0'))
    rng=random.Random(seed)
    current=_make_systematic(seed)
    current_d=_distance(current)
    best=current[:]
    best_d=current_d
    budget=max(0.0, min(float(os.environ.get('MATHBENCH_SEARCH_SECONDS','2')), 30.0))
    deadline = search_deadline()
    steps=0
    for _attempt in search_steps(60):
        candidate=_mutate_parity(current, rng)
        candidate_d=_distance(candidate)
        steps += 1
        if candidate_d > best_d:
            best,best_d=candidate[:],candidate_d
        # A cooling schedule permits occasional downhill moves to escape plateaus.
        temperature=max(0.15, 2.0 * (1.0 - min(steps, 200) / 200.0))
        delta=candidate_d-current_d
        if delta >= 0 or rng.random() < math.exp(delta/temperature):
            current,current_d=candidate,candidate_d
    matrix=[[((row >> j) & 1) for j in range(N)] for row in best]
    return {'generator_matrix':matrix}
