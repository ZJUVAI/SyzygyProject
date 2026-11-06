"""Local-search evolution for binary A(17, 6), seeded by the BCH baseline."""

import os
import random
import time

from baseline import _start


N = 17
_LIMIT = 45.0


def _seconds():
    try:
        value = float(os.environ.get("MATHBENCH_EVOLUTION_SECONDS", _LIMIT))
    except (TypeError, ValueError):
        value = _LIMIT
    return max(0.0, min(_LIMIT, value))


def _distance_masks():
    masks = []
    for a in range(1 << N):
        if a.bit_count() <= 5:
            masks.append(a)
    return masks


def _valid(words):
    # The BCH seed and every update are checked with exact integer bit counts.
    for i, a in enumerate(words):
        for b in words[i + 1 :]:
            if (a ^ b).bit_count() < 6:
                return False
    return len(words) == len(set(words))


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T067-C01") != "T067-C01":
        raise ValueError("unsupported configuration")

    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    best = list(_start())
    if not _valid(best):
        raise RuntimeError("BCH starting construction failed exact validation")

    deadline = time.monotonic() + _seconds()
    masks = _distance_masks()
    # Candidate availability is maintained as a byte array. The zero mask is
    # included because selected words must also be excluded from reinsertion.
    universe = 1 << N
    while time.monotonic() < deadline:
        incumbent = best[:]
        # A kick removes a small random subset, then greedy reinsertion repairs
        # the code. Larger kicks occasionally escape a stable local maximum.
        kick = min(len(incumbent) - 1, rng.choices((1, 2, 3, 5, 8), (42, 28, 16, 10, 4))[0])
        removed = set(rng.sample(range(len(incumbent)), kick))
        chosen = [w for i, w in enumerate(incumbent) if i not in removed]
        forbidden = bytearray(universe)
        for word in chosen:
            for mask in masks:
                forbidden[word ^ mask] = 1

        order = list(range(universe))
        rng.shuffle(order)
        for word in order:
            if not forbidden[word]:
                chosen.append(word)
                for mask in masks:
                    forbidden[word ^ mask] = 1
        if len(chosen) > len(best) and _valid(chosen):
            best = chosen

    return {"codewords": best}
