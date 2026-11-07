"""Fixed-seed greedy set-cover baseline for the 10-dimensional cube."""

import math
import os
import random
import time

from tasks.t068.check import CONFIG_ID, LENGTH, UNIVERSE_MASK, UNIVERSE_SIZE


TRIAL_LIMIT = 8
_BALLS = tuple(
    (1 << center) | sum(1 << (center ^ (1 << bit)) for bit in range(LENGTH))
    for center in range(UNIVERSE_SIZE)
)


def _greedy(order):
    uncovered = UNIVERSE_MASK
    selected = []
    remaining = set(range(UNIVERSE_SIZE))
    while uncovered:
        best = None
        best_gain = -1
        for center in order:
            if center not in remaining:
                continue
            gain = (_BALLS[center] & uncovered).bit_count()
            if gain > best_gain:
                best, best_gain = center, gain
        if best is None or best_gain <= 0:
            raise RuntimeError("greedy set cover failed to cover the cube")
        selected.append(best)
        remaining.remove(best)
        uncovered &= ~_BALLS[best]

    # Remove redundant sets in reverse selection order.
    for center in tuple(reversed(selected)):
        others = [item for item in selected if item != center]
        union = 0
        for item in others:
            union |= _BALLS[item]
        if union == UNIVERSE_MASK:
            selected.remove(center)
    return sorted(selected)


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    seconds_text = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds_text is not None:
        seconds = float(seconds_text)
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + seconds

    rng = random.Random(seed)
    order = list(range(UNIVERSE_SIZE))
    best = _greedy(order)
    completed = 0
    for _ in range(TRIAL_LIMIT):
        if deadline is not None and time.monotonic() >= deadline:
            break
        rng.shuffle(order)
        candidate = _greedy(order)
        completed += 1
        if len(candidate) < len(best):
            best = candidate
    return {
        "codewords": best,
        "search_metadata": {
            "algorithm": "greedy maximum-new-coverage set cover followed by redundant-center deletion",
            "seed": seed,
            "trial_limit": TRIAL_LIMIT,
            "trials_completed": completed,
            "reference_data_read": False,
            "search_seconds_cutoff": seconds_text,
        },
    }
