"""Simple initial construction: the Delaunay triangulation of the fixed input."""

from __future__ import annotations

import json
import os
from decimal import Decimal
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T095-C01") != "T095-C01":
        raise ValueError("unknown T095 configuration")
    data_path = Path(__file__).parent / "data/source/uniform-0000500-1.instance.json"
    raw = json.loads(data_path.read_text(), parse_float=Decimal)
    pts = []
    for point in raw["points"]:
        x, y = point["x"], point["y"]
        if isinstance(x, Decimal): x = int(x)
        if isinstance(y, Decimal): y = int(y)
        pts.append((x, y))
    simplices = Delaunay(np.asarray(pts, dtype=float)).simplices
    edges = set()
    for triangle in simplices:
        tri = list(map(int, triangle))
        for k, u in enumerate(tri):
            v = tri[(k+1) % 3]
            edges.add((min(u, v), max(u, v)))
    return {"edges": [{"i": u, "j": v} for u, v in sorted(edges)]}
