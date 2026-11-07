"""Standalone Cartesian-grid seed from the public fixed polygon input."""
import json
import os
from fractions import Fraction
from pathlib import Path


def _inside(x, y, polygon):
    inside = False
    for (ax, ay), (bx, by) in zip(polygon, polygon[1:] + polygon[:1]):
        if (ay > y) != (by > y):
            x_hit = Fraction(ax) + (y - ay) * (bx - ax) / (by - ay)
            if x_hit > x:
                inside = not inside
    return inside


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T064-C01") != "T064-C01":
        raise ValueError("unsupported T064 configuration")
    seed = int(os.environ.get("MATHBENCH_SEED", "0"))
    input_path = Path(__file__).with_name("data") / "source" / "ortho40.instance.json"
    data = json.loads(input_path.read_text(encoding="utf-8"))
    original = list(zip(data["points_x"], data["points_y"]))
    polygon = [original[i] for i in data["region_boundary"]]
    # EVOLVE-BLOCK-START
    xs, ys = sorted({x for x, _ in original}), sorted({y for _, y in original})
    cells = []
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if _inside(Fraction(xs[i] + xs[i + 1], 2),
                       Fraction(ys[j] + ys[j + 1], 2), polygon):
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
        ll, lr = index[(xs[i], ys[j])], index[(xs[i + 1], ys[j])]
        ur, ul = index[(xs[i + 1], ys[j + 1])], index[(xs[i], ys[j + 1])]
        for tri in ((ll, lr, ur), (ll, ur, ul)):
            for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
                edges.add(tuple(sorted((a, b))))
    # EVOLVE-BLOCK-END
    return {
        "instance_uid": data["instance_uid"],
        "steiner_points_x": [str(x) for x, _ in extras],
        "steiner_points_y": [str(y) for _, y in extras],
        "edges": [list(edge) for edge in sorted(edges)],
        "seed": seed,
    }
