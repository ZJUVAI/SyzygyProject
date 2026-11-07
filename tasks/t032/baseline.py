"""Seeded kicked-greedy search, independent of witness files."""
import os
import random
from itertools import combinations
from mathbench.search import search_steps

ROWS, COLS = 14, 19
ROW_TRIPLES = tuple(combinations(range(ROWS), 3))


def _valid(masks):
    return all((masks[a] & masks[b] & masks[c]).bit_count() < 3
               for a, b, c in ROW_TRIPLES)


def _score(matrix):
    return sum(sum(row) for row in matrix)


def run_code():
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    rng = random.Random(seed)
    matrix = [[0] * COLS for _ in range(ROWS)]
    masks = [0] * ROWS
    incumbent = [row[:] for row in matrix]
    incumbent_score = 0
    accepted_additions = 0
    steps = 0
    kicks = 0

    for step in search_steps(10000):
        steps += 1
        # Kick only by deleting existing ones, so feasibility is preserved.
        if step and step % 997 == 0:
            present = [(i, j) for i in range(ROWS) for j in range(COLS) if matrix[i][j]]
            for i, j in rng.sample(present, min(4, len(present))):
                matrix[i][j] = 0
                masks[i] &= ~(1 << j)
            kicks += 1

        # Greedy one-bit addition. Rejected additions leave the matrix untouched.
        i, j = rng.randrange(ROWS), rng.randrange(COLS)
        if not matrix[i][j]:
            matrix[i][j] = 1
            masks[i] |= 1 << j
            if _valid(masks):
                accepted_additions += 1
                score = _score(matrix)
                if score > incumbent_score:
                    incumbent_score = score
                    incumbent = [row[:] for row in matrix]
            else:
                matrix[i][j] = 0
                masks[i] &= ~(1 << j)

    final_score = _score(matrix)
    return {
        "matrix": incumbent,
        "search_metadata": {
            "algorithm": "seeded greedy one-bit addition with four-one deletion kicks",
            "seed": seed,
            "iteration_budget": 10000,
            "actual_steps": steps,
            "kicks": kicks,
            "accepted_additions": accepted_additions,
            "incumbent_score": incumbent_score,
            "final_search_state_score": final_score,
            "returned_score": incumbent_score,
            "time_budget_seconds": float(os.environ["MATHBENCH_SEARCH_SECONDS"])
                if "MATHBENCH_SEARCH_SECONDS" in os.environ else None,
        },
    }
