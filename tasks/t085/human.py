"""Finite patch of the classical triangular-lattice circle covering."""
from fractions import Fraction as F
import os


def _text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T085-C01") != "T085-C01":
        raise ValueError("unsupported configuration")
    # A rational lower approximation to sqrt(3), times a small safety factor.
    root = F(1732050807568877293527446341505872366942805253810380628055806979, 10**63)
    scale = F(999, 1000)
    centers = [(scale * root * (q + F(t, 2)), scale * F(3 * t, 2))
               for q in range(-2, 3) for t in range(-2, 3)
               if max(abs(q), abs(t), abs(q + t)) <= 2]
    # The finite patch has 19 lattice sites; two allowed repeated centers make 21 circles.
    centers.extend([(F(0), F(0)), (F(0), F(0))])
    return {"radius": "7/2", "centers": [[_text(x), _text(y)] for x, y in centers]}
