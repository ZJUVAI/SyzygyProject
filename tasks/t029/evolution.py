"""Bounded exact subset search from the public schoolbook seed."""
import os
import random

from tasks.t029.init_program import run_code as schoolbook
from tasks.t029.check import validate


TRIALS = 4


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    config = {"parameters": {
        "matrix_order": 3,
        "field": "Q",
        "coefficient_domain": "arbitrary rational strings or exact Fraction values",
        "max_terms": 27,
        "term_count_is_scalar_multiplication_count": True,
    }}
    best = schoolbook()
    attempts = 0
    # Search for a shorter subset of the 27 elementary products. A deletion
    # is kept only when exact verification succeeds; this conservative search
    # does not make any claim about completeness over all rational factors.
    for _ in range(TRIALS):
        order = list(range(len(best["terms"])))
        rng.shuffle(order)
        candidate = {"terms": list(best["terms"])}
        for index in order:
            proposal = {"terms": [term for j, term in enumerate(candidate["terms"]) if j != index]}
            attempts += 1
            try:
                validate(proposal, config)
            except ValueError:
                continue
            candidate = proposal
        if len(candidate["terms"]) < len(best["terms"]):
            best = candidate
    best["search_metadata"] = {
        "algorithm": "seeded randomized greedy deletion with exact tensor checks",
        "seed": seed,
        "iterations": attempts,
        "trial_limit": TRIALS,
        "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
        "reference_data_read": False,
        "search_scope": "subsets of the 27 schoolbook terms only; coefficients are not evolved",
    }
    return best
