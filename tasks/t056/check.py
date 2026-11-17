"""Exact verifier for mutually orthogonal Latin squares of order 12."""

ORDER = 12
SYMBOLS = set(range(ORDER))


def _squares(solution):
    if isinstance(solution, dict):
        if "squares" not in solution:
            raise ValueError("solution must contain squares")
        squares = solution["squares"]
    else:
        squares = solution
    if not isinstance(squares, (list, tuple)):
        raise ValueError("squares must be a list")
    if len(squares) > ORDER - 1:
        raise ValueError("a family cannot have more than n-1 squares")
    checked = []
    for square_index, square in enumerate(squares):
        if not isinstance(square, (list, tuple)) or len(square) != ORDER:
            raise ValueError(f"square {square_index} must have 12 rows")
        rows = []
        for row_index, row in enumerate(square):
            if not isinstance(row, (list, tuple)) or len(row) != ORDER:
                raise ValueError(f"square {square_index}, row {row_index} must have 12 entries")
            values = []
            for value in row:
                if type(value) is not int or value not in SYMBOLS:
                    raise ValueError("entries must be integers 0..11; bool and non-integers are rejected")
                values.append(value)
            if set(values) != SYMBOLS:
                raise ValueError(f"row {row_index} of square {square_index} is not a permutation")
            rows.append(values)
        for column in range(ORDER):
            if {rows[row][column] for row in range(ORDER)} != SYMBOLS:
                raise ValueError(f"column {column} of square {square_index} is not a permutation")
        checked.append(rows)
    return checked


def validate(solution, config, strict=False):
    if config.get("parameters") != {"order": ORDER}:
        raise ValueError("unsupported configuration")
    squares = _squares(solution)
    pair_checks = 0
    for left in range(len(squares)):
        for right in range(left + 1, len(squares)):
            pairs = {
                (squares[left][row][column], squares[right][row][column])
                for row in range(ORDER)
                for column in range(ORDER)
            }
            if len(pairs) != ORDER * ORDER:
                raise ValueError(f"squares {left} and {right} are not orthogonal")
            pair_checks += 1
    return {
        "objective": len(squares),
        "verification_status": "exact",
        "details": {
            "order": ORDER,
            "squares_checked": len(squares),
            "orthogonal_pairs_checked": pair_checks,
            "ordered_pairs_per_square_pair": ORDER * ORDER,
            "claimed_objective_ignored": True,
        },
    }
