"""Reconstruct the published PGL(2,11) permutation code for length 12."""

import os

from tasks.t052.check import PARAMETERS, validate

Q = 11


def _projective_matrices():
    # Each projective matrix class has one representative whose first nonzero
    # entry in row-major order is 1. Enumerating only these representatives
    # avoids duplicate scalar multiples.
    for a in range(Q):
        for b in range(Q):
            for c in range(Q):
                for d in range(Q):
                    entries = (a, b, c, d)
                    first = next((value for value in entries if value), None)
                    if first != 1 or (a * d - b * c) % Q == 0:
                        continue
                    yield a, b, c, d


def _action(matrix):
    a, b, c, d = matrix
    values = []
    for point in range(Q):
        denominator = (c * point + d) % Q
        numerator = (a * point + b) % Q
        values.append(Q if denominator == 0 else (numerator * pow(denominator, -1, Q)) % Q)
    values.append(Q if c == 0 else (a * pow(c, -1, Q)) % Q)
    return values


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T052-C01") != "T052-C01":
        raise ValueError("unsupported configuration")
    codewords = [_action(matrix) for matrix in _projective_matrices()]
    result = {"codewords": codewords}
    validate(result, {"parameters": PARAMETERS}, strict=True)
    return result


if __name__ == "__main__":
    print({"codeword_count": len(run_code()["codewords"])})
