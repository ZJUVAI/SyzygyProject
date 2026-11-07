"""Find a 24-point D4 orbit by exact integer moment-pattern enumeration."""

from itertools import combinations_with_replacement
import os
import random

from tasks.t073.construction import radical_field_solution, signed_permutation_orbit


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T073-C01")
    if chosen != "T073-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    try:
        seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    except ValueError as exc:
        raise ValueError("MATHBENCH_SEED must be an integer") from exc
    examined = 0
    patterns = list(combinations_with_replacement(range(4), 4))
    random.Random(seed).shuffle(patterns)
    for pattern in patterns:
        examined += 1
        squared_norm = sum(value * value for value in pattern)
        fourth_sum = sum(value ** 4 for value in pattern)
        if squared_norm == 0 or 2 * fourth_sum != squared_norm * squared_norm:
            continue
        orbit = signed_permutation_orbit(pattern)
        if len(orbit) != 24:
            continue
        solution = radical_field_solution(orbit, squared_norm)
        solution["search_metadata"] = {
            "algorithm": "enumerate integer coordinate multisets and select a signed-permutation orbit satisfying the exact fourth-moment identity",
            "seed": seed,
            "integer_patterns_examined": examined,
            "point_count": len(orbit),
            "human_or_reference_data_read": False,
        }
        return solution
    raise RuntimeError("no 24-point integer orbit found within the fixed pattern set")
