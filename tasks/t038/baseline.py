"""MacNeish product construction from GF(3) and GF(4), yielding two MOLS."""
import os


def _gf4_mul(a, b):
    """Multiply two GF(4) bit encodings modulo x^2+x+1."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def _square(slope3, slope4):
    out = []
    for r in range(12):
        row = []
        r3, r4 = divmod(r, 4)
        for c in range(12):
            c3, c4 = divmod(c, 4)
            value3 = (r3 + slope3 * c3) % 3
            value4 = r4 ^ _gf4_mul(slope4, c4)
            row.append(4 * value3 + value4)
        out.append(row)
    return out


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T038-C01") != "T038-C01":
        raise ValueError("unsupported configuration")
    # MacNeish product: one common slope choice in GF(3) and GF(4) gives
    # two coordinatewise distinct slopes and therefore two orthogonal squares.
    return {
        "squares": [_square(1, 1), _square(2, 2)],
        "construction": "MacNeish product GF(3) x GF(4)",
        "objective": 2,
    }
