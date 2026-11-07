"""Fixed-seed random-order greedy independent-set search for T071."""

import math
import os
import random
import time

from tasks.t071.check import ALPHABET_SIZE, CONFIG_ID, deletion_outputs


TRIAL_LIMIT = 2


def _greedy(order, deadline=None):
    selected = []
    used_outputs = set()
    attempted = 0
    for word in order:
        if attempted % 1024 == 0 and deadline is not None and time.monotonic() >= deadline:
            break
        attempted += 1
        outputs = deletion_outputs(word)
        if not outputs.isdisjoint(used_outputs):
            continue
        selected.append(word)
        used_outputs.update(outputs)
    return selected, attempted


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    try:
        seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    except ValueError as exc:
        raise ValueError("MATHBENCH_SEED must be an integer") from exc
    seconds_text = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    deadline = None
    if seconds_text is not None:
        try:
            seconds = float(seconds_text)
        except ValueError as exc:
            raise ValueError("search seconds must be numeric") from exc
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + seconds
    rng = random.Random(seed)
    order = list(range(ALPHABET_SIZE))
    best = []
    completed = attempted = 0
    for _ in range(TRIAL_LIMIT):
        if deadline is not None and time.monotonic() >= deadline:
            break
        rng.shuffle(order)
        candidate, count = _greedy(order, deadline)
        attempted += count
        completed += 1
        if len(candidate) > len(best):
            best = candidate
        if deadline is not None and time.monotonic() >= deadline:
            break
    return {
        "codewords": best,
        "search_metadata": {
            "algorithm": "random-order greedy selection of an independent set in the deletion-conflict graph",
            "seed": seed,
            "trial_limit": TRIAL_LIMIT,
            "trials_completed": completed,
            "candidate_visits": attempted,
            "reference_data_read": False,
            "search_seconds_cutoff": seconds_text,
        },
    }
