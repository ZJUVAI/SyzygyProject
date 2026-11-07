"""Fixed-step local search for shorter integer B3 sets."""

import os
import random

from tasks.t084.baseline import build_greedy
from tasks.t084.check import validate


def run_code():
    rng = random.Random(int(os.environ.get("MATHBENCH_SEED", "0")))
    current, candidate_checks = build_greedy()
    best = current[:]
    iterations = 0
    accepted = 0
    # Each proposal changes one nonzero element. The exact checker enforces B3.
    for iterations in range(1, 1501):
        index = rng.randrange(1, len(current))
        proposal = current[:]
        radius = max(20, current[-1] // (8 + iterations // 250))
        proposal[index] = max(1, proposal[index] + rng.randint(-radius, radius))
        if len(set(proposal)) != len(proposal):
            continue
        proposal.sort()
        try:
            outcome = validate({"elements": proposal}, {
                "id": "T084-C01",
                "parameters": {"cardinality": 31, "order": 3, "integer_domain": True},
            })
        except ValueError:
            continue
        accepted += 1
        if outcome["objective"] < max(best) - min(best):
            best = proposal
        if outcome["objective"] <= max(current) - min(current) or rng.random() < 0.002:
            current = proposal
        if iterations % 100 == 0:
            current = best[:]
    return {
        "elements": best,
        "search_method": "greedy construction followed by exact-check single-element mutation",
        "candidate_checks": candidate_checks,
        "search_iterations": iterations,
        "accepted_valid_proposals": accepted,
        "random_seed": int(os.environ.get("MATHBENCH_SEED", "0")),
    }
