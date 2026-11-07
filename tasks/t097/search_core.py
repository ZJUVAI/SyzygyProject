"""Independent rational triangulation and convex merge search for T097."""
import json
import os
import random
from fractions import Fraction
from pathlib import Path


TASK_DIR = Path(__file__).parent
INPUT_PATH = TASK_DIR / "data/source/socg_fixed92.instance.json"


def load_boundary():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01")
    if config_id != "T097-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    instance = json.loads(INPUT_PATH.read_text())
    return [(p["x"], p["y"]) for p in instance["outer_boundary"]]


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def point_on_segment(p, a, b):
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def point_inside(p, polygon):
    inside = False
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if point_on_segment(p, a, b):
            return True
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + Fraction((p[1] - a[1]) * (b[0] - a[0])) / (b[1] - a[1])
            if x > p[0]:
                inside = not inside
    return inside


def segment_inside(p, q, polygon):
    if p == q:
        return point_inside(p, polygon)
    dx, dy = q[0] - p[0], q[1] - p[1]
    ts = {0, 1}
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        ex, ey = b[0] - a[0], b[1] - a[1]
        den = dx * ey - dy * ex
        qpx, qpy = a[0] - p[0], a[1] - p[1]
        if den:
            t = Fraction(qpx * ey - qpy * ex, den)
            u = Fraction(qpx * dy - qpy * dx, den)
            if 0 <= t <= 1 and 0 <= u <= 1:
                ts.add(t)
        elif qpx * dy - qpy * dx == 0:
            for r in (a, b):
                if dx and min(p[0], q[0]) <= r[0] <= max(p[0], q[0]):
                    ts.add(Fraction(r[0] - p[0], dx))
                elif dy and min(p[1], q[1]) <= r[1] <= max(p[1], q[1]):
                    ts.add(Fraction(r[1] - p[1], dy))
    ordered = sorted(ts)
    for left, right in zip(ordered, ordered[1:]):
        t = (left + right) / 2
        point = (p[0] + t * dx, p[1] + t * dy)
        if not point_inside(point, polygon):
            return False
    return True


def convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 2:
        return points
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def hull_is_contained(hull, boundary):
    if len(hull) < 3 or any(not point_inside(p, boundary) for p in hull):
        return False
    return all(segment_inside(a, b, boundary) for a, b in zip(hull, hull[1:] + hull[:1]))


def triangulate(boundary):
    vertices = list(boundary)
    area2 = sum(a[0] * b[1] - a[1] * b[0]
                for a, b in zip(vertices, vertices[1:] + vertices[:1]))
    if area2 < 0:
        vertices.reverse()
    if area2 == 0:
        raise ValueError("fixed polygon has zero area")
    triangles = []
    while len(vertices) > 3:
        found = False
        n = len(vertices)
        for i in range(n):
            a, b, c = vertices[i - 1], vertices[i], vertices[(i + 1) % n]
            if cross(a, b, c) <= 0:
                continue
            def in_triangle(p):
                return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0
            if any(in_triangle(p) for j, p in enumerate(vertices)
                   if j not in {(i - 1) % n, i, (i + 1) % n}):
                continue
            triangles.append([a, b, c])
            del vertices[i]
            found = True
            break
        if not found:
            raise ValueError("ear clipping found no ear in the fixed simple polygon")
    triangles.append(vertices)
    return triangles


def encode_solution(polygons, metadata=None):
    result = {
        "algebraic_field": {"minimal_polynomial": ["0", "1"], "isolating_interval": ["-1", "1"]},
        "polygons": [[[[str(x)], [str(y)]] for x, y in polygon] for polygon in polygons],
    }
    if metadata is not None:
        result["search_metadata"] = metadata
    return result


def initial_solution():
    boundary = load_boundary()
    triangles = triangulate(boundary)
    return encode_solution(triangles, {"construction": "exact ear clipping", "initial_triangle_count": len(triangles)})


def greedy_merge(seed, seed_value=0, max_sweeps=1):
    boundary = load_boundary()
    polygons = [[tuple(point) for point in poly] for poly in seed]
    rng = random.Random(seed_value)
    attempted = merged = 0
    sweeps_run = 0
    for _ in range(max_sweeps):
        sweeps_run += 1
        changed = False
        pairs = [(i, j) for i in range(len(polygons)) for j in range(i + 1, len(polygons))]
        rng.shuffle(pairs)
        for i, j in pairs:
            if i >= len(polygons) or j >= len(polygons):
                continue
            attempted += 1
            hull = convex_hull(polygons[i] + polygons[j])
            if hull_is_contained(hull, boundary):
                polygons[i] = hull
                del polygons[j]
                merged += 1
                changed = True
                break
        if not changed:
            break
    return polygons, {"construction": "seeded greedy convex-hull merges from the public polygon triangulation",
                      "seed": seed_value, "sweeps": sweeps_run, "sweep_limit": max_sweeps,
                      "candidate_pairs_checked": attempted,
                      "merges": merged, "comparison_data_read": False}


def seed_from_env(default=0):
    text = os.environ.get("MATHBENCH_SEED", str(default))
    try:
        return int(text)
    except ValueError:
        raise ValueError("MATHBENCH_SEED must be an integer")
