"""Rebuild the two public degree-three binary quasi-cyclic codes."""

PARAMETERS = {
    "T009-C02": {
        "n": 80,
        "k": 20,
        "block_length": 27,
        "operation": "puncture",
        "polynomials": (
            (11, 8, 6, 5, 3, 0),
            (14, 9, 8, 7, 4, 2, 1, 0),
            (22, 21, 20, 18, 17, 16, 13, 12, 11, 9, 8, 6, 4, 3, 1, 0),
        ),
        "puncture_coordinate": 80,
    },
    "T009-C03": {
        "n": 100,
        "k": 20,
        "block_length": 33,
        "operation": "append_zero",
        "polynomials": (
            (14, 13, 11, 10, 9, 6, 5, 4, 2, 1),
            (21, 15, 14, 13, 10, 9, 7, 5, 1, 0),
            (27, 26, 23, 22, 21, 20, 18, 17, 16, 15, 13, 11, 6, 5, 4, 0),
        ),
    },
}


def _row_basis(rows, width):
    pivots = {}
    for row in rows:
        value = row
        for col in range(width - 1, -1, -1):
            if (value >> col) & 1:
                if col in pivots:
                    value ^= pivots[col]
                else:
                    pivots[col] = value
                    break
    return [pivots[col] for col in sorted(pivots)]


def build_matrix(config_id):
    """Return a deterministic independent-row basis of the QC code."""
    try:
        spec = PARAMETERS[config_id]
    except KeyError as exc:
        raise ValueError("unsupported configuration") from exc
    m = spec["block_length"]
    raw_rows = []
    # A degree-three QC generator is the vector (g0,g1,g2) over
    # GF(2)[x]/(x^m-1); its m cyclic shifts span the code.
    for shift in range(m):
        row = 0
        for component, exponents in enumerate(spec["polynomials"]):
            for exponent in exponents:
                row |= 1 << (component * m + (exponent + shift) % m)
        raw_rows.append(row)
    basis = _row_basis(raw_rows, 3 * m)
    if len(basis) != spec["k"]:
        raise ValueError(f"QC generator rank is {len(basis)}, expected {spec['k']}")
    matrix = []
    for row in basis:
        bits = [(row >> col) & 1 for col in range(3 * m)]
        if spec["operation"] == "puncture":
            bits.pop(spec["puncture_coordinate"])
        elif spec["operation"] == "append_zero":
            bits.append(0)
        matrix.append(bits)
    if any(len(row) != spec["n"] for row in matrix):
        raise ValueError("constructed matrix has the wrong length")
    return matrix
