"""Exact checker for a 14 by 19 binary matrix with no all-ones 3x3 submatrix."""
from itertools import combinations


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    p = config.get("parameters", config)
    if not isinstance(p, dict) or p.get("rows") != 14 or p.get("columns") != 19 or p.get("forbidden_submatrix") != [3, 3]:
        raise ValueError("configuration must be T032-C01 (14 by 19, forbid all-ones 3x3)")
    matrix = solution.get("matrix")
    if not isinstance(matrix, list) or len(matrix) != 14:
        raise ValueError("matrix must have exactly 14 rows")
    for row in matrix:
        if not isinstance(row, list) or len(row) != 19:
            raise ValueError("each matrix row must have exactly 19 entries")
        if any(type(x) is not int or x not in (0, 1) for x in row):
            raise ValueError("matrix entries must be integer 0 or 1")
    ones = sum(sum(row) for row in matrix)
    # A forbidden submatrix exists iff some row triple has at least three common 1-columns.
    max_common = 0
    row_masks = [sum(bit << j for j, bit in enumerate(row)) for row in matrix]
    for triple in combinations(row_masks, 3):
        common = (triple[0] & triple[1] & triple[2]).bit_count()
        max_common = max(max_common, common)
        if common >= 3:
            raise ValueError("matrix contains an all-ones 3x3 submatrix")
    return {"objective": ones, "verification_status": "exact",
            "details": {"rows": 14, "columns": 19, "ones": ones,
                        "row_triples_checked": 364, "maximum_common_columns": max_common,
                        "claimed_objective_ignored": True}}
