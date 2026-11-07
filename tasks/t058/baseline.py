"""Fixed-work randomized greedy search for pair-disjoint parallel rounds."""

import math
import os
import random
import time

from tasks.t058.check import CONFIG_ID


def _try_add_random_round(used_pairs, rng):
    players = list(range(35))
    rng.shuffle(players)
    groups = [players[i:i + 5] for i in range(0, 35, 5)]
    new_pairs = set()
    for group in groups:
        for offset, left in enumerate(group):
            for right in group[offset + 1:]:
                pair = (left, right) if left < right else (right, left)
                if pair in used_pairs:
                    return None
                new_pairs.add(pair)
    return groups, new_pairs


def _grow_once(rng, attempts_per_round, deadline):
    rounds = []
    used_pairs = set()
    attempts = 0
    for _ in range(8):
        added = None
        for _ in range(attempts_per_round):
            if deadline is not None and time.monotonic() >= deadline:
                return rounds, attempts, True
            attempts += 1
            added = _try_add_random_round(used_pairs, rng)
            if added is not None:
                break
        if added is None:
            break
        groups, new_pairs = added
        rounds.append(groups)
        used_pairs.update(new_pairs)
    return rounds, attempts, False


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    restarts = int(os.environ.get("T058_SEARCH_RESTARTS", "8"))
    attempts_per_round = int(os.environ.get("T058_ATTEMPTS_PER_ROUND", "5000"))
    if restarts < 0 or attempts_per_round < 1:
        raise ValueError("restarts must be nonnegative and attempts per round positive")
    seconds_text = os.environ.get("MATHBENCH_SEARCH_SECONDS")
    if seconds_text is None:
        deadline = None
    else:
        seconds = float(seconds_text)
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("search seconds must be finite and positive")
        deadline = time.monotonic() + seconds

    rng = random.Random(seed)
    best = [[[5 * group + offset for offset in range(5)] for group in range(7)]]
    completed_restarts = 0
    total_attempts = 0
    timed_out = False
    for _ in range(restarts):
        candidate, attempts, timed_out = _grow_once(rng, attempts_per_round, deadline)
        total_attempts += attempts
        completed_restarts += 1
        if len(candidate) > len(best):
            best = candidate
        if timed_out:
            break
    return {
        "rounds": best,
        "search": {
            "algorithm": "randomized greedy construction of pair-disjoint rounds",
            "seed": seed,
            "restart_limit": restarts,
            "restarts_completed": completed_restarts,
            "attempts_per_round": attempts_per_round,
            "partition_attempts": total_attempts,
            "time_cutoff_reached": timed_out,
            "reference_data_read": False,
        },
    }
