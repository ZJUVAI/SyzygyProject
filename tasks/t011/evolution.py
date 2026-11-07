"""Integer tabu and bounded clique search for independent sets in C7^5.

Only an optional owned incumbent supplied by the runner is read. A compiled
single-thread kernel searches exact neighborhoods and saves feasible sets.
"""

import itertools
import json
import os
import random
import time

N = 7 ** 5
_POWERS = (7 ** 4, 7 ** 3, 7 ** 2, 7, 1)
_NEIGHBORHOODS = None


def _build_neighborhoods():
    """Build closed-neighborhood bitsets for all 7^5 words."""
    out = [0] * N
    for v in range(N):
        x = v
        digits = [0] * 5
        for i in range(4, -1, -1):
            digits[i] = x % 7
            x //= 7
        choices = [((d - 1) % 7, d, (d + 1) % 7) for d in digits]
        mask = 0
        for word in itertools.product(*choices):
            u = 0
            for d in word:
                u = 7 * u + d
            mask |= 1 << u
        out[v] = mask
    return out


def _decode(v):
    word = [0] * 5
    for i in range(4, -1, -1):
        word[i] = v % 7
        v //= 7
    return word


def _encode(word):
    value = 0
    for digit in word:
        value = 7 * value + digit
    return value


def _warm_start():
    path = os.environ.get("MATHBENCH_WARM_START")
    if not path:
        return None
    try:
        with open(path, encoding="utf-8") as stream:
            solution = json.load(stream)
        words = solution["words"]
        if not isinstance(words, list):
            return None
        encoded = [_encode(word) for word in words]
        if len(set(encoded)) != len(encoded):
            return None
        return encoded
    except (OSError, ValueError, TypeError, KeyError):
        return None


def _affine_variant(source, rng):
    """Apply a coordinate permutation and independent dihedral maps of C7."""
    permutation = list(range(5))
    rng.shuffle(permutation)
    offsets = [rng.randrange(7) for _ in range(5)]
    signs = [rng.choice((-1, 1)) for _ in range(5)]
    result = []
    for value in source:
        digits = _decode(value)
        mapped = [(signs[i] * digits[permutation[i]] + offsets[i]) % 7
                  for i in range(5)]
        result.append(_encode(mapped))
    return result


def _local_exchange(chosen, neighborhoods, rng, deadline):
    """Remove a small set and greedily refill its neighborhood.

    A move is committed only if its cardinality grows, so every incumbent
    remains a valid independent set and the search cannot lose its best.
    """
    if len(chosen) < 2 or time.monotonic() >= deadline:
        return chosen
    remove_count = rng.choices((2, 3, 4, 5, 7, 9),
                               weights=(24, 23, 20, 16, 11, 6))[0]
    remove_count = min(remove_count, len(chosen))
    if rng.random() < 0.75:
        # Center destruction on an unselected vertex. Its actual blockers
        # form a coherent cavity; independent random removals rarely do.
        anchor = rng.randrange(N)
        positions = {i for i, v in enumerate(chosen)
                     if neighborhoods[anchor] & (1 << v)}
        if not positions or len(positions) > 14:
            positions = set(rng.sample(range(len(chosen)), remove_count))
    else:
        positions = set(rng.sample(range(len(chosen)), remove_count))
    removed = [chosen[i] for i in positions]
    retained = [v for i, v in enumerate(chosen) if i not in positions]
    blocked = 0
    for v in retained:
        blocked |= neighborhoods[v]

    pool_mask = 0
    for v in removed:
        pool_mask |= neighborhoods[v]
    available_mask = pool_mask & ~blocked
    cavity_mask = available_mask
    candidates = []
    while available_mask:
        bit = available_mask & -available_mask
        candidates.append(bit.bit_length() - 1)
        available_mask ^= bit

    # Low-conflict vertices tend to leave more room for later additions.
    # Random jitter preserves diversity across repeated exchanges.
    rng.shuffle(candidates)
    candidates.sort(key=lambda v: (neighborhoods[v] & cavity_mask).bit_count()
                    + rng.random() * 0.15)
    trial = retained[:]
    for v in candidates:
        if time.monotonic() >= deadline:
            break
        bit = 1 << v
        if not blocked & bit:
            trial.append(v)
            blocked |= neighborhoods[v]
    return trial if len(trial) >= len(chosen) else chosen


def _random_greedy(neighborhoods, rng, deadline):
    order = list(range(N))
    rng.shuffle(order)
    chosen = []
    blocked = 0
    for v in order:
        if time.monotonic() >= deadline:
            break
        bit = 1 << v
        if not blocked & bit:
            chosen.append(v)
            blocked |= neighborhoods[v]
    return chosen


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T011-C01")
    if config_id != "T011-C01":
        # The compiled cavity kernel below is specialized to the accepted C7^5
        # search. New powers use the dimension-aware classical greedy baseline.
        from baseline import run_code as run_baseline
        candidate = run_baseline()
        candidate["_evolution"] = {"method": "dimension-aware seeded randomized greedy"}
        return candidate
    global _NEIGHBORHOODS
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    try:
        budget = min(240.0, max(0.0, float(
            os.environ.get("MATHBENCH_EVOLUTION_SECONDS", "45"))))
    except ValueError:
        budget = 45.0
    rng = random.Random(seed)
    # Valid cold-start construction: {0,2,4}^5.
    best = [sum(d * p for d, p in zip(word, _POWERS))
            for word in itertools.product((0, 2, 4), repeat=5)]
    started = time.monotonic()
    warm = _warm_start()
    if warm is not None:
        from check import validate
        validate({"words": [_decode(v) for v in warm]},
                 {"id": "T011-C01", "parameters": {"q": 7, "power": 5}})
    if warm is not None and len(warm) > len(best):
        best = warm
    if budget <= 0:
        return {"words": [_decode(v) for v in best]}

    import subprocess
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory(prefix='t011_kernel_') as temporary:
        executable = Path(temporary) / 'search_kernel'
        subprocess.run(['g++', '-O3', '-std=c++17', str(Path(__file__).with_name('search_kernel.cpp')),
                        '-o', str(executable)], check=True, capture_output=True, timeout=35)
        remaining = max(0.0, budget-(time.monotonic()-started))
        payload = f'{seed % 2**32} {remaining:.6f} {len(best)}\n' + ' '.join(map(str,best)) + '\n'
        result = subprocess.run([str(executable)],input=payload,text=True,capture_output=True,
                                check=True,timeout=remaining+10)
    header, raw = result.stdout.strip().split('\n')
    size,moves,cavities,improvements=map(int,header.split())
    candidate = list(map(int,raw.split()))
    from check import validate
    output = {'words': [_decode(v) for v in candidate]}
    validate(output, {'id':'T011-C01','parameters':{'q':7,'power':5}},strict=True)
    if len(candidate)!=size:
        raise RuntimeError('kernel size mismatch')
    output['_evolution'] = {'method':'compiled fixed-size tabu and exact bounded clique cavity',
        'moves':moves,'cavities':cavities,'improvements':improvements,'kernel_log':result.stderr.strip()}
    return output
