"""Focused integer swap search for C(24, 14, 4).

Only the runner-supplied owned incumbent is read. The compiled search changes
fixed-size covers; a complete exact four-subset check certifies each output.
"""

import json
import os
import random
import time
from itertools import combinations

from tasks.t008.init_program import run_code as seed_cover


V, K, T = 24, 14, 4
QUADS = tuple(combinations(range(V), T))
UNIVERSE_SIZE = len(QUADS)
UNIVERSE = (1 << UNIVERSE_SIZE) - 1


def _budget_seconds():
    try:
        requested = float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))
    except (TypeError, ValueError):
        requested = 45.0
    return max(0.01, min(300.0, requested))


def _normalize(raw_blocks):
    blocks = []
    for raw in raw_blocks:
        block = tuple(sorted(raw))
        if len(block) != K or len(set(block)) != K or any(type(x) is not int or x < 0 or x >= V for x in block):
            raise ValueError("warm start contains an invalid block")
        blocks.append(block)
    if len(set(blocks)) != len(blocks):
        raise ValueError("warm start contains duplicate blocks")
    return blocks


def _cover_mask(block, quad_index):
    mask = 0
    for quad in combinations(block, T):
        mask |= 1 << quad_index[quad]
    return mask


def _read_warm_start():
    path = os.environ.get("MATHBENCH_WARM_START")
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            blocks = _normalize(json.load(handle)["blocks"])
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        return None
    index = {quad: i for i, quad in enumerate(QUADS)}
    covered = 0
    for block in blocks:
        covered |= _cover_mask(block, index)
    return blocks if covered == UNIVERSE else None


def _mutate(block, rng):
    values = set(block)
    outgoing = rng.sample(tuple(values), rng.choice((1, 1, 2, 3)))
    incoming = rng.sample(tuple(set(range(V)) - values), len(outgoing))
    values.difference_update(outgoing)
    values.update(incoming)
    return tuple(sorted(values))


def _repair(selected, pool, masks, deadline, rng):
    """Greedily restore exact coverage from a bitset deficit."""
    chosen = set(selected)
    covered = 0
    for i in chosen:
        covered |= masks[i]
    while covered != UNIVERSE and time.monotonic() < deadline:
        deficit = UNIVERSE & ~covered
        top = []
        for i, mask in enumerate(masks):
            if i in chosen:
                continue
            gain = (mask & deficit).bit_count()
            if gain:
                top.append((gain, rng.random(), i))
        if not top:
            return None
        top.sort(reverse=True)
        # Randomize among near-best candidates to keep several repair paths.
        width = min(8, len(top))
        best_gain = top[0][0]
        near = [item for item in top[:width] if item[0] >= best_gain * 0.97]
        choice = rng.choice(near)
        chosen.add(choice[2])
        covered |= masks[choice[2]]
    return sorted(chosen) if covered == UNIVERSE else None


def _milp_repair(selected, masks, limit, deadline):
    """Solve a bounded exact set-cover subproblem on the uncovered quads."""
    import numpy as np
    from scipy.optimize import milp, Bounds, LinearConstraint
    from scipy.sparse import csc_matrix
    covered = 0
    for i in selected:
        covered |= masks[i]
    deficit = UNIVERSE & ~covered
    if not deficit:
        return sorted(selected)
    # A single exact column can close this deficit without solver startup.
    if limit >= 1:
        for i, mask in enumerate(masks):
            if deficit & ~mask == 0:
                return sorted(set(selected) | {i})
    rows = {}
    bits = deficit
    while bits:
        bit = bits & -bits
        rows[bit.bit_length()-1] = len(rows)
        bits ^= bit
    columns, rr, cc = [], [], []
    for i, mask in enumerate(masks):
        overlap = mask & deficit
        if not overlap:
            continue
        column = len(columns)
        columns.append(i)
        while overlap:
            bit = overlap & -overlap
            rr.append(rows[bit.bit_length()-1]); cc.append(column)
            overlap ^= bit
    if time.monotonic() >= deadline or not columns:
        return None
    matrix = csc_matrix((np.ones(len(rr)), (rr, cc)), shape=(len(rows), len(columns)))
    from scipy.sparse import vstack
    matrix = vstack([matrix, np.ones((1, len(columns)))], format="csc")
    lower = np.r_[np.ones(len(rows)), 0]
    upper = np.r_[np.full(len(rows), np.inf), limit]
    result = milp(np.ones(len(columns)), integrality=np.ones(len(columns)),
                  bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, lower, upper),
                  options={"time_limit": min(2.0, max(.01, deadline-time.monotonic())), "threads": 1})
    if result.x is None:
        return None
    candidate = sorted(set(selected) | {columns[j] for j,x in enumerate(result.x) if x > .5})
    check = 0
    for i in candidate:
        check |= masks[i]
    return candidate if check == UNIVERSE and len(candidate) <= len(selected)+limit else None


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T008-C01")
    if config_id == "T008-C02":
        # The C01 compiled swap kernel is parameter-specific. Keep new drafts
        # valid and deterministic until a separately tuned kernel is reviewed.
        return seed_cover()
    if config_id != "T008-C01":
        raise ValueError("unsupported configuration")

    started = time.monotonic()
    deadline = started + _budget_seconds()
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    index = {quad: i for i, quad in enumerate(QUADS)}
    fallback = _normalize(seed_cover()["blocks"])
    best = _read_warm_start() or fallback
    import subprocess
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory(prefix='t008_cover_') as temporary:
        executable = Path(temporary) / 'cover_search'
        subprocess.run(['g++', '-O3', '-std=c++17', str(Path(__file__).with_name('cover_search.cpp')),
                        '-o', str(executable)], check=True,capture_output=True,timeout=35)
        remaining=max(0.0,deadline-time.monotonic())
        payload=f'{seed % 2**32} {remaining:.6f} {len(best)}\n'
        payload+='\n'.join(' '.join(map(str,block)) for block in best)+'\n'
        result=subprocess.run([str(executable)],input=payload,text=True,capture_output=True,
                              check=True,timeout=remaining+10)
    lines=result.stdout.strip().splitlines()
    size,moves,restarts,lowest=map(int,lines[0].split())
    blocks=_normalize([list(map(int,line.split())) for line in lines[1:]])
    covered=0
    for block in blocks:
        covered|=_cover_mask(block,index)
    if len(blocks)!=size or covered!=UNIVERSE:
        raise RuntimeError('compiled cover search returned invalid cover')
    return {'blocks':[list(block) for block in blocks], '_evolution':{
        'method':'compiled fixed-size focused swaps with adaptive uncovered-quad weights',
        'moves':moves,'restarts':restarts,'minimum_deficit':lowest,
        'kernel_log':result.stderr.strip(),'elapsed_seconds':time.monotonic()-started}}
