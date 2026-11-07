"""Exact checker for binary strength-4 orthogonal arrays."""
from itertools import combinations
import math

PARAMETERS = {"columns": 63, "levels": 2, "strength": 4, "row_repetition": "allowed"}
COLUMN_COUNT = 63
ROW_MASK_LIMIT = 1 << COLUMN_COUNT
MINIMUM_ROW_BOUND = 2032


def _column_bitsets(rows):
    columns = [0] * COLUMN_COUNT
    for row_index, row in enumerate(rows):
        bit = 1 << row_index
        for column in range(COLUMN_COUNT):
            if (row >> column) & 1:
                columns[column] |= bit
    return columns


def _balanced_parity_characters(columns, row_count):
    target = row_count // 2
    for size in range(1, 5):
        for indices in combinations(range(COLUMN_COUNT), size):
            parity_rows = 0
            for index in indices:
                parity_rows ^= columns[index]
            if parity_rows.bit_count() != target:
                return False, size, indices, parity_rows.bit_count(), target
    return True, 0, (), target, target


def validate(solution, config, strict=False):
    if (not isinstance(config, dict) or config.get("id") != "T091-C01"
            or not isinstance(config.get("parameters"), dict)
            or config["parameters"] != PARAMETERS
            or any(type(config["parameters"].get(k)) is not type(v) for k, v in PARAMETERS.items())):
        raise ValueError("unsupported configuration or parameters")
    if not isinstance(solution, dict) or not isinstance(solution.get("rows"), list):
        raise ValueError("solution must contain a row list")
    rows = solution["rows"]
    row_count = len(rows)
    if row_count < MINIMUM_ROW_BOUND:
        raise ValueError("row count violates the proven Rao lower bound and divisibility")
    if row_count % 16:
        raise ValueError("row count must be divisible by 16 for strength 4")
    for i, row in enumerate(rows):
        if type(row) is not int or not 0 <= row < ROW_MASK_LIMIT:
            raise ValueError(f"row {i} must be a 63-bit nonnegative integer mask")
    columns = _column_bitsets(rows)
    valid, size, indices, count, target = _balanced_parity_characters(columns, row_count)
    if not valid:
        raise ValueError(f"unbalanced parity on {size} columns {indices}: {count}, expected {target}")
    return {
        "objective": row_count,
        "objective_value": row_count,
        "verification_status": "exact",
        "details": {
            "rows": row_count,
            "columns": COLUMN_COUNT,
            "strength": 4,
            "repeated_rows_allowed": True,
            "balanced_parity_checks": sum(math.comb(COLUMN_COUNT, k) for k in range(1, 5)),
            "pattern_equivalence": "For each selected set of four columns, all nontrivial parity characters are balanced; binary Fourier inversion gives every 4-bit pattern exactly N/16 times.",
            "rao_lower_bound": MINIMUM_ROW_BOUND,
            "claimed_score_ignored": True
        }
    }
