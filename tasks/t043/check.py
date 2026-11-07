"""Exact verifier for binary (7,4;3) constant-dimension subspace codes."""

PARAMETERS = {
    "field_size": 2,
    "ambient_dimension": 7,
    "subspace_dimension": 3,
    "minimum_subspace_distance": 4,
}
N = 7
K = 3


def _rank(rows):
    rows = list(rows)
    rank = 0
    for col in range(N):
        pivot = next((i for i in range(rank, len(rows)) if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for i in range(len(rows)):
            if i != rank and ((rows[i] >> col) & 1):
                rows[i] ^= rows[rank]
        rank += 1
        if rank == len(rows):
            break
    return rank


def _span(rows):
    return frozenset((a * rows[0]) ^ (b * rows[1]) ^ (c * rows[2])
                     for a in (0, 1) for b in (0, 1) for c in (0, 1))


def _parse_basis(value):
    if not isinstance(value, (list, tuple)) or len(value) != K:
        raise ValueError("each codeword must contain exactly three basis rows")
    if all(type(x) is int for x in value):
        rows = []
        for x in value:
            if x < 0 or x >= (1 << N):
                raise ValueError("row masks must be integers from 0 through 127")
            rows.append(x)
    else:
        rows = []
        for row in value:
            if not isinstance(row, (list, tuple)) or len(row) != N:
                raise ValueError("basis matrices must have shape 3 by 7")
            if any(type(x) is not int or x not in (0, 1) for x in row):
                raise ValueError("matrix entries must be integer 0 or 1; bool is rejected")
            rows.append(sum(x << j for j, x in enumerate(row)))
    if _rank(rows) != K:
        raise ValueError("each codeword basis must have rank 3 over GF(2)")
    return _span(rows)


def validate(solution, config, strict=False):
    if config.get("parameters") != PARAMETERS:
        raise ValueError("unsupported configuration")
    if not isinstance(solution, dict) or "codewords" not in solution:
        raise ValueError("solution must contain codewords")
    codewords = solution["codewords"]
    if not isinstance(codewords, (list, tuple)):
        raise ValueError("codewords must be a list")
    spaces = [_parse_basis(word) for word in codewords]
    canonical = set()
    for space in spaces:
        if space in canonical:
            raise ValueError("duplicate codeword subspace")
        canonical.add(space)
    pair_count = 0
    for i, left in enumerate(spaces):
        for right in spaces[i + 1:]:
            pair_count += 1
            if len(left.intersection(right)) > 2:
                raise ValueError("codewords intersect in dimension at least 2")
    return {
        "objective": len(spaces),
        "verification_status": "exact",
        "details": {
            "codewords_checked": len(spaces),
            "pairs_checked": pair_count,
            "minimum_subspace_distance": 4,
            "claimed_objective_ignored": True,
        },
    }
