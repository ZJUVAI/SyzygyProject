"""Decode the fixed Shadoks viewer polygons from the archived CGSHOP page."""
import re
import os
import hashlib
from fractions import Fraction
from pathlib import Path


def _round_integer(value):
    floor = value.numerator // value.denominator
    candidates = (floor, floor + 1)
    best = min(candidates, key=lambda n: abs(value - n))
    if abs(value - best) >= Fraction(1, 1000):
        raise ValueError("viewer coordinate is not within display precision of an integer")
    return best


def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01")
    if config_id != "T097-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    source_path = Path(__file__).parent / "data/source/socg_fixed92_solution.html"
    raw_html = source_path.read_bytes()
    if hashlib.sha256(raw_html).hexdigest() != "3d5d8c4107e79622cf349ac23bcf49826eb8257502a767915ff9601b9b5e1270":
        raise ValueError("archived viewer source checksum mismatch")
    html = raw_html.decode("utf-8")
    matches = re.findall(r'<polygon class="backPoly polySoluce"[^>]*points="([^"]+)"', html)
    polygons = []
    for display_points in matches:
        polygon = []
        for pair in display_points.split():
            sx, sy = (Fraction(value) for value in pair.split(","))
            x = Fraction(96) + sx * Fraction(176, 225)
            y = Fraction(832) - sy * Fraction(176, 225)
            polygon.append([_round_integer(x), _round_integer(y)])
        polygons.append(polygon)
    if len(polygons) != 15:
        raise ValueError("archived source must contain the published 15-polygon solution")
    return {
        "algebraic_field": {"minimal_polynomial": ["0", "1"], "isolating_interval": ["-1", "1"]},
        "polygons": [[[[str(x)], [str(y)]] for x, y in polygon] for polygon in polygons],
        "reconstruction_metadata": {
            "source": "archived Shadoks CGSHOP 2023 viewer HTML",
            "affine_scale": "225/176",
            "display_rounding_tolerance": "1/1000",
            "coordinate_status": "nearby integers inferred from rounded display coordinates; original submitted coordinates are not recovered uniquely",
        },
    }
