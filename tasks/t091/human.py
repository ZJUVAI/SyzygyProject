"""Reconstruct OA(4096,63,2,4) from the dual of a binary double-error BCH code."""
import os


def _mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 64:
            a ^= 0x43
    return result


def _power(a, e):
    result = 1
    while e:
        if e & 1:
            result = _mul(result, a)
        a = _mul(a, a)
        e >>= 1
    return result


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T091-C01") != "T091-C01":
        raise ValueError("unsupported configuration")
    # Columns are the binary coordinates of (alpha^i, alpha^(3i)) in GF(64)^2.
    powers = []
    a = 1
    for _ in range(63):
        powers.append(a)
        a = _mul(a, 2)
    if a != 1 or len(set(powers)) != 63:
        raise RuntimeError("GF(64) primitive element check failed")
    labels = [powers[i] | (_power(powers[i], 3) << 6) for i in range(63)]
    rows = []
    for form in range(4096):
        row = 0
        for j, label in enumerate(labels):
            row |= ((form & label).bit_count() & 1) << j
        rows.append(row)
    return {"rows": rows}
