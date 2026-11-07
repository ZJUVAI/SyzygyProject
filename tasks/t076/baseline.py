"""Seeded cap-sweep greedy search for 15 sum-distinct integers."""

import os
import random


CAP_START = 8_000
CAP_STOP = 10_000
CAP_STEP = 25
ELEMENT_COUNT = 15
_CONFIGS = {"T076-C01":15,"T076-C02":16,"T076-C03":17}


def _greedy_descending(cap, element_count):
    subset_sums = 1
    selected = []
    for value in range(cap, 0, -1):
        shifted = subset_sums << value
        if subset_sums & shifted:
            continue
        selected.append(value)
        subset_sums |= shifted
        if len(selected) == element_count:
            return sorted(selected)
    return None


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T076-C01")
    try: element_count = _CONFIGS[chosen]
    except KeyError: raise ValueError(f"unsupported configuration: {chosen}") from None
    try:
        seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    except ValueError as exc:
        raise ValueError("MATHBENCH_SEED must be an integer") from exc
    if element_count == 15:
        caps = list(range(CAP_START, CAP_STOP + 1, CAP_STEP))
    else:
        start, stop = {16:(16000,19000),17:(32000,37000)}[element_count]
        caps = list(range(start, stop + 1, max(1, (stop-start)//9)))
    random.Random(seed).shuffle(caps)
    best = None
    completed = 0
    for cap in caps:
        candidate = _greedy_descending(cap, element_count)
        completed += 1
        if candidate is not None and (best is None or max(candidate) < max(best)):
            best = candidate
    if best is None:
        best = [1 << bit for bit in range(element_count)]
    return {
        "elements": best,
        "search_metadata": {
            "algorithm": "greedy descending scan with exact subset-sum bitset, over a seeded fixed cap grid",
            "seed": seed,
            "cap_start": min(caps) if caps else None,
            "cap_stop": max(caps) if caps else None,
            "cap_step": (caps[1]-caps[0]) if len(caps)>1 else 0,
            "cap_trials_completed": completed,
            "reference_data_read": False,
        },
    }
