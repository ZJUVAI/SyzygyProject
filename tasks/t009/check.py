"""Exact verifier for configured binary linear codes."""


SUPPORTED = {
    "T009-C01": {"n": 68, "k": 15, "q": 2},
    "T009-C02": {"n": 80, "k": 20, "q": 2},
    "T009-C03": {"n": 100, "k": 20, "q": 2},
}


def _rank(rows, n, k):
    packed = [sum(bit << j for j, bit in enumerate(row)) for row in rows]
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, k) if (packed[i] >> col) & 1), None)
        if pivot is None:
            continue
        packed[rank], packed[pivot] = packed[pivot], packed[rank]
        for i in range(k):
            if i != rank and ((packed[i] >> col) & 1):
                packed[i] ^= packed[rank]
        rank += 1
        if rank == k:
            break
    return rank


def _matrix(solution, n, k):
    if not isinstance(solution, dict) or "generator_matrix" not in solution:
        raise ValueError("solution must contain generator_matrix")
    matrix = solution["generator_matrix"]
    if not isinstance(matrix, (list, tuple)) or len(matrix) != k:
        raise ValueError(f"generator_matrix must have {k} rows")
    rows = []
    for row in matrix:
        if not isinstance(row, (list, tuple)) or len(row) != n:
            raise ValueError(f"each generator row must have {n} entries")
        if any(type(bit) is not int or bit not in (0, 1) for bit in row):
            raise ValueError("matrix entries must be integer 0 or 1 (bool is rejected)")
        rows.append(list(row))
    if _rank(rows, n, k) != k:
        raise ValueError(f"generator matrix must have rank {k} over GF(2)")
    return rows


def _min_distance(rows):
    k = len(rows)
    n = len(rows[0])
    packed = [sum(bit << j for j, bit in enumerate(row)) for row in rows]
    word = 0
    previous_gray = 0
    best = n + 1
    for i in range(1, 1 << k):
        gray = i ^ (i >> 1)
        changed = gray ^ previous_gray
        word ^= packed[changed.bit_length() - 1]
        best = min(best, word.bit_count())
        previous_gray = gray
    return best


def validate(solution, config, strict=False):
    if not isinstance(config, dict):
        raise ValueError("unsupported configuration")
    config_id = config.get("id")
    params = config.get("parameters")
    if config_id not in SUPPORTED or params != SUPPORTED[config_id]:
        raise ValueError("unsupported configuration")
    n, k = params["n"], params["k"]
    rows = _matrix(solution, n, k)
    distance = _min_distance(rows)
    return {
        "objective": distance,
        "verification_status": "exact",
        "details": {
            "parameters": {"n": n, "k": k, "q": 2},
            "rank": k,
            "codewords_checked": (1 << k) - 1,
            "claimed_objective_ignored": True,
        },
    }
