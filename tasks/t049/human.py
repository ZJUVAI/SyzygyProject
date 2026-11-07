"""Reconstruct the s=6 triangular-lattice hexagon in Erdős--Fishburn."""

from fractions import Fraction


def run_code():
    points = []
    # Axial coordinates for a radius-5 hexagon: max(|i|, |j|, |i+j|) <= 5.
    for i in range(-5, 6):
        for j in range(-5, 6):
            if max(abs(i), abs(j), abs(i + j)) <= 5:
                points.append({
                    "x": [str(Fraction(2 * i + j, 2))],
                    "y": ["0", str(Fraction(j, 2))],
                })
    return {
        "minimal_polynomial": [-3, 0, 1],
        "isolating_interval": ["1", "2"],
        "points": points,
    }
