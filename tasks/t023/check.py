"""Exact bit-mask verifier for uniform covering arrays."""
from itertools import combinations
from math import comb


def validate(solution, config, strict=False):
    p = config["parameters"]
    t, k, v = p["strength"], p["columns"], p["alphabet_size"]
    if not isinstance(solution, dict) or "array" not in solution:
        raise ValueError("solution must contain array")
    array = solution["array"]
    if not isinstance(array, list) or not 1 <= len(array) <= p["rows_upper_bound"]:
        raise ValueError("array row count is outside the allowed range")
    if any(not isinstance(row, list) or len(row) != k for row in array):
        raise ValueError("each row must have the configured number of columns")
    if any(type(x) is not int or not 0 <= x < v for row in array for x in row):
        raise ValueError("entries must be integers in the configured alphabet")
    if len({tuple(row) for row in array}) != len(array):
        raise ValueError("duplicate rows are not allowed")
    symbol_rows = [[0 for _ in range(v)] for _ in range(k)]
    for ri, row in enumerate(array):
        row_bit = 1 << ri
        for j, value in enumerate(row):
            symbol_rows[j][value] |= row_bit
    uncovered = 0
    projection_count = 0
    for cols in combinations(range(k), t):
        projection_count += 1
        for pattern in __import__("itertools").product(range(v), repeat=t):
            covered = (1 << len(array)) - 1
            for j, value in zip(cols, pattern):
                covered &= symbol_rows[j][value]
                if not covered:
                    break
            if not covered:
                uncovered += 1
    if uncovered:
        raise ValueError(f"array misses {uncovered} projections")
    return {"objective": len(array), "verification_status": "exact",
            "details": {"rows": len(array), "columns": k, "strength": t,
                        "alphabet_size": v, "projection_count": projection_count,
                        "uncovered_tuples": 0, "claimed_objective_ignored": True}}
