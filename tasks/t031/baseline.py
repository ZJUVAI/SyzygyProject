"""Seeded randomized maximum-overlap search over all 7! permutations."""

from itertools import permutations
import os
import random

from mathbench.search import search_steps


ITERATION_LIMIT = 8


def _best_successors(current, remaining):
    """Return unused next permutations with the greatest available overlap."""
    alphabet = "1234567"
    for overlap in range(6, -1, -1):
        prefix = current[-overlap:] if overlap else ""
        missing = tuple(symbol for symbol in alphabet if symbol not in prefix)
        choices = [
            prefix + "".join(tail)
            for tail in permutations(missing)
            if prefix + "".join(tail) in remaining
        ]
        if choices:
            return overlap, choices
    return -1, []


def _greedy_word(all_permutations, rng):
    remaining = set(all_permutations)
    current = rng.choice(all_permutations)
    remaining.remove(current)
    word = current
    while remaining:
        chosen_overlap, choices = _best_successors(current, remaining)
        if not choices:
            raise RuntimeError("no unused permutation successor")
        current = rng.choice(choices)
        remaining.remove(current)
        word += current[chosen_overlap:]
    return word


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T031-C01")
    if config_id != "T031-C01":
        raise ValueError("unsupported configuration id")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    all_permutations = ["".join(p) for p in permutations("1234567")]
    best_word = None
    best_length = None
    iterations = 0
    steps = iter(search_steps(ITERATION_LIMIT))
    for _ in range(ITERATION_LIMIT):
        if next(steps, None) is None:
            break
        candidate = _greedy_word(all_permutations, rng)
        iterations += 1
        if best_length is None or len(candidate) < best_length:
            best_word, best_length = candidate, len(candidate)
    if best_word is None:
        # A zero-second exploration budget still returns a valid construction.
        best_word = "".join(all_permutations)
        best_length = len(best_word)
    return {
        "word": best_word,
        "claimed_objective": best_length,
        "search_metadata": {
            "algorithm": "seeded randomized maximum-overlap greedy path through all permutations",
            "configuration_id": config_id,
            "seed": seed,
            "iterations": iterations,
            "iteration_limit": ITERATION_LIMIT,
            "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            "reference_data_read": False,
            "budget": {
                "iteration_limit": ITERATION_LIMIT,
                "wall_clock_cutoff_seconds": os.environ.get("MATHBENCH_SEARCH_SECONDS"),
            },
        },
    }
