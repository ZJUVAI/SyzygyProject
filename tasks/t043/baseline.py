"""Seeded randomized greedy packing of 3-spaces by their 2-subspaces."""

import os
import random
import time
from functools import lru_cache


@lru_cache(maxsize=1)
def _spaces():
    spaces = set()
    vectors = range(1, 128)
    for a in vectors:
        for b in range(a + 1, 128):
            ab = {0, a, b, a ^ b}
            for c in range(b + 1, 128):
                if c in ab:
                    continue
                space = tuple(sorted(ab | {x ^ c for x in ab}))
                spaces.add(space)
    ordered = sorted(spaces)
    line_ids = {}
    supports = []
    for space in ordered:
        nonzero = [x for x in space if x]
        lines = set()
        for i, x in enumerate(nonzero):
            for y in nonzero[i + 1:]:
                lines.add(tuple(sorted((x, y, x ^ y))))
        assert len(lines) == 7
        ids = []
        for line in sorted(lines):
            ids.append(line_ids.setdefault(line, len(line_ids)))
        supports.append(tuple(ids))
    assert len(ordered) == 11811 and len(line_ids) == 2667
    return ordered, supports


def _basis(space):
    chosen, span = [], {0}
    for vector in space:
        if vector and vector not in span:
            chosen.append(vector)
            span |= {x ^ vector for x in span}
            if len(chosen) == 3:
                return chosen
    raise ValueError("space has no three-vector basis")


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T043-C01") != "T043-C01":
        raise ValueError("unsupported configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    passes = max(1, min(100, int(os.environ.get("MATHBENCH_SEARCH_ITERATIONS", "12"))))
    from mathbench.search import search_steps

    start = time.monotonic()
    spaces, supports = _spaces()
    rng = random.Random(seed)
    best, best_pass = [], 0
    passes_run = 0
    for pass_index in search_steps(passes):
        order = list(range(len(spaces)))
        rng.shuffle(order)
        used_lines = 0
        chosen = []
        for index in order:
            line_mask = sum(1 << line_id for line_id in supports[index])
            if not (used_lines & line_mask):
                chosen.append(index)
                used_lines |= line_mask
        passes_run += 1
        if len(chosen) > len(best):
            best = chosen
            best_pass = pass_index
    return {
        "codewords": [_basis(spaces[index]) for index in best],
        "search_metadata": {
            "algorithm": "seeded randomized greedy packing of enumerated 3-spaces by 2-space supports",
            "seed": seed,
            "iterations_requested": passes,
            "iterations_run": passes_run,
            "best_pass": best_pass,
            "candidate_subspaces_enumerated": len(spaces),
            "line_supports": 2667,
            "generation_seconds": time.monotonic() - start,
            "budget": {"mode": "fixed_iterations unless MATHBENCH_SEARCH_SECONDS is set",
                       "runner_generation_limit_seconds": 300},
        },
    }


if __name__ == "__main__":
    print(run_code())
