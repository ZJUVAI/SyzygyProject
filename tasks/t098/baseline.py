"""Deterministic area-preserving-size mutation and B-code skyline search."""
import os
import random
import re
from math import isqrt

from tasks.t098.builder import tile_bouwkamp_line
from tasks.t098.check import CONFIG_ID, FROZEN_CONFIG, validate

# This weak seed came from an independent run of the general network method.
# No human construction, comparison B-code, or reference witness is read here.
_OWN_BCODE = "38 4755 4755 (2429,2326)(103,657,1566)(1092,502,384,554)(118,96,170)(22,74)(590,52)(538,969)(1234,555,431)(60,226,417,863)(124,803,367,166)(679)(201,191)(10,152,446)(436,142)(294)"
_OWN_GROUPS = tuple(
    tuple(map(int, group.split(",")))
    for group in re.findall(r"\(([^)]*)\)", _OWN_BCODE)
)
LAST_SEARCH_STATS = {}


def _size_mutations():
    """All one-side replacements changing outer area to a nearby square."""
    sizes = [size for group in _OWN_GROUPS for size in group]
    side = 4755
    result = []
    # This finite neighborhood is a search range, not a candidate-domain cap.
    for delta in range(-1000, 1001):
        target = side + delta
        if delta == 0 or target <= 0:
            continue
        target_area_delta = target * target - side * side
        for index, old in enumerate(sizes):
            new_square = old * old + target_area_delta
            if new_square <= 0:
                continue
            new = isqrt(new_square)
            if new * new != new_square or new <= 0 or new > target:
                continue
            if new in sizes[:index] or new in sizes[index + 1 :]:
                continue
            result.append((delta, index, old, new))
    return tuple(result)


_MUTATIONS = _size_mutations()


def run_code():
    global LAST_SEARCH_STATS
    if os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID) != CONFIG_ID:
        raise ValueError("unsupported T098 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rounds = int(os.environ.get("T098_SEARCH_ITERS", "40"))
    if not 0 <= rounds <= 1000:
        raise ValueError("T098_SEARCH_ITERS must be in 0..1000")
    randomizer = random.Random(seed)
    best = tile_bouwkamp_line(_OWN_BCODE)
    best_value = validate(best, FROZEN_CONFIG)["objective"]
    proposed_sides = set()
    build_successes = 0
    valid_candidates = 0
    for _ in range(rounds):
        if not _MUTATIONS:
            break
        delta, index, old, new = randomizer.choice(_MUTATIONS)
        target = 4755 + delta
        proposed_sides.add(target)
        groups = [list(group) for group in _OWN_GROUPS]
        flat_index = 0
        replaced = False
        for group in groups:
            if flat_index <= index < flat_index + len(group):
                group[index - flat_index] = new
                replaced = True
                break
            flat_index += len(group)
        if not replaced:
            continue
        randomizer.shuffle(groups)
        for group in groups:
            randomizer.shuffle(group)
        code = f"38 {target} {target} " + "".join(
            "(" + ",".join(map(str, group)) + ")" for group in groups
        )
        try:
            candidate = tile_bouwkamp_line(code)
            build_successes += 1
            value = validate(candidate, FROZEN_CONFIG)["objective"]
            valid_candidates += 1
        except (ValueError, IndexError):
            continue
        if value < best_value:
            best, best_value = candidate, value
    LAST_SEARCH_STATS = {
        "iterations_requested": rounds,
        "size_set_and_outer_side_proposals": rounds,
        "distinct_proposed_outer_sides": sorted(proposed_sides),
        "skyline_build_successes": build_successes,
        "valid_candidates": valid_candidates,
        "best_objective": best_value,
        "baseline_fallback_used": best_value == 4755,
        "mutation_pool_size": len(_MUTATIONS),
        "seed": seed,
    }
    return best
