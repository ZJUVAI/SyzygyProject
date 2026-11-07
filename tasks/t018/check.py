"""Exact validation for 29 by 29 sign matrices."""


def determinant_bareiss(matrix):
    a = [list(row) for row in matrix]
    n = len(a)
    sign, previous = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * p - a[i][k] * a[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = p
    return sign * a[n - 1][n - 1]


def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    n = params.get("n") if isinstance(params, dict) else None
    if type(n) is not int or n not in (27, 29, 31):
        raise ValueError("configuration must specify n=27, 29, or 31")
    matrix = solution.get("matrix")
    if not isinstance(matrix, list) or len(matrix) != n:
        raise ValueError(f"matrix must have {n} rows")
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            raise ValueError(f"each row must have {n} entries")
        for value in row:
            if type(value) is not int or value not in (-1, 1):
                raise ValueError("entries must be integer -1 or 1; bool is not accepted")
    det = determinant_bareiss(matrix)
    return {"objective": abs(det), "verification_status": "exact", "details": {"signed_determinant": det, "n": n}}
