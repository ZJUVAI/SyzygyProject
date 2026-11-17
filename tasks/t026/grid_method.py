"""Cartesian-grid orthogonal triangulation used by the reconstructed baseline."""
import json
from fractions import Fraction
from pathlib import Path


def load_polygon():
    path = Path(__file__).with_name("data") / "source" / "ortho40.instance.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    points = list(zip(data["points_x"], data["points_y"]))
    return data, points


def _inside(x, y, polygon):
    inside = False
    for (ax, ay), (bx, by) in zip(polygon, polygon[1:] + polygon[:1]):
        if (ay > y) != (by > y):
            x_hit = Fraction(ax) + (y - ay) * (bx - ax) / (by - ay)
            if x_hit > x:
                inside = not inside
    return inside


def build_grid(pattern=0):
    data, original = load_polygon()
    polygon = [original[i] for i in data["region_boundary"]]
    xs = sorted({x for x, _ in original})
    ys = sorted({y for _, y in original})
    cells = []
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            cx = Fraction(xs[i] + xs[i + 1], 2)
            cy = Fraction(ys[j] + ys[j + 1], 2)
            if _inside(cx, cy, polygon):
                cells.append((i, j))

    used = set(original)
    for i, j in cells:
        used.update(((xs[i], ys[j]), (xs[i + 1], ys[j]),
                     (xs[i + 1], ys[j + 1]), (xs[i], ys[j + 1])))
    extras = sorted(used.difference(original))
    all_points = original + extras
    index = {point: i for i, point in enumerate(all_points)}
    edges = set()
    for i, j in cells:
        ll = index[(xs[i], ys[j])]
        lr = index[(xs[i + 1], ys[j])]
        ur = index[(xs[i + 1], ys[j + 1])]
        ul = index[(xs[i], ys[j + 1])]
        use_other_diagonal = (pattern == 1 and (i + j) % 2 == 1) or (
            pattern == 2 and (i + j) % 2 == 0
        )
        if use_other_diagonal:
            triangles = ((ll, lr, ul), (lr, ur, ul))
        else:
            triangles = ((ll, lr, ur), (ll, ur, ul))
        for tri in triangles:
            for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
                edges.add(tuple(sorted((a, b))))

    def encode(value):
        return str(value)

    return {
        "instance_uid": data["instance_uid"],
        "steiner_points_x": [encode(x) for x, _ in extras],
        "steiner_points_y": [encode(y) for _, y in extras],
        "edges": [list(edge) for edge in sorted(edges)],
        "construction_metadata": {
            "method": "uniform Cartesian grid at all input x/y coordinates",
            "inside_grid_cells": len(cells),
            "diagonal_pattern": pattern,
            "reference_data_read": False,
        },
    }
