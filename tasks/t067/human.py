"""Rebuild Fredricksen and Sweet's published symmetric partition of [1,536]."""

import json
from pathlib import Path


def run_code():
    data_path = Path(__file__).parent / "data" / "fredricksen_sweet_536_halfsets.json"
    payload = json.loads(data_path.read_text())
    n = payload["n"]
    modulus = payload["modulus"]
    exceptional = set(payload["exceptional_elements"])
    colors = [None] * n
    for color, representatives in enumerate(payload["representatives"]):
        for value in representatives:
            for member in (value, modulus - value):
                if member in exceptional and member != value:
                    continue
                if not 1 <= member <= n:
                    raise ValueError("representative expands outside [1,n]")
                if colors[member - 1] is not None:
                    raise ValueError("overlapping representative sets")
                colors[member - 1] = color
    if any(color is None for color in colors):
        raise ValueError("published representative sets do not cover [1,n]")
    return {"n": n, "colors": colors}
