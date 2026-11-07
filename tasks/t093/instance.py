"""Frozen CG:SHOP 2024 polygon-packing instance and exact geometry helpers."""

from functools import lru_cache
import hashlib
import json
from pathlib import Path


INSTANCE_NAME = "random_cf2_74ae2d30_50"
INSTANCE_SHA256 = "f2ad180face7d410ec40cf531d8bbf4a5631a9a6c18f9d7a73579717abca9c92"
SOURCE_PATH = Path(__file__).resolve().parent / "data" / "source" / f"{INSTANCE_NAME}.cgshop2024_instance.json"
TYPE_COUNT = 44
AVAILABLE_COUNT = 50
ITEM_LIMIT = 50


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def area2(poly):
    return sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(poly, poly[1:] + poly[:1]))


def _on_segment(a, b, p):
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def _segments_intersect(a, b, c, d):
    o1, o2, o3, o4 = cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b)
    if o1 == 0 and _on_segment(a, b, c):
        return True
    if o2 == 0 and _on_segment(a, b, d):
        return True
    if o3 == 0 and _on_segment(c, d, a):
        return True
    if o4 == 0 and _on_segment(c, d, b):
        return True
    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)


def triangulate(poly):
    """Exact ear clipping for a simple integer polygon; returns CCW triangles."""
    if not isinstance(poly, (tuple, list)) or len(poly) < 3:
        raise ValueError("polygon must have at least three vertices")
    points = list(poly)
    if any(not isinstance(p, (tuple, list)) or len(p) != 2 or
           any(type(c) is not int for c in p) for p in points):
        raise ValueError("polygon vertices must use integer coordinates")
    points = [tuple(p) for p in points]
    if len(set(points)) != len(points):
        raise ValueError("polygon has repeated vertices")

    # Drop a collinear middle vertex. A reversal along an edge is not a simple
    # polygon and is rejected below.
    changed = True
    while changed and len(points) > 3:
        changed = False
        for i in range(len(points)):
            a, b, c = points[i - 1], points[i], points[(i + 1) % len(points)]
            if cross(a, b, c) == 0:
                if not _on_segment(a, c, b):
                    raise ValueError("polygon backtracks along a boundary edge")
                points.pop(i)
                changed = True
                break
    signed = area2(points)
    if signed == 0:
        raise ValueError("polygon has zero area")
    if signed < 0:
        points.reverse()

    n = len(points)
    for i in range(n):
        a, b = points[i], points[(i + 1) % n]
        for j in range(i + 1, n):
            if j == i or j == (i + 1) % n or (j + 1) % n == i:
                continue
            c, d = points[j], points[(j + 1) % n]
            if _segments_intersect(a, b, c, d):
                raise ValueError("polygon boundary self-intersects")

    remaining = list(range(n))
    triangles = []
    while len(remaining) > 3:
        found = False
        for k, current in enumerate(remaining):
            prev = remaining[k - 1]
            nxt = remaining[(k + 1) % len(remaining)]
            a, b, c = points[prev], points[current], points[nxt]
            if cross(a, b, c) <= 0:
                continue
            occupied = False
            for other in remaining:
                if other in (prev, current, nxt):
                    continue
                p = points[other]
                if cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0:
                    occupied = True
                    break
            if occupied:
                continue
            triangles.append((a, b, c))
            remaining.pop(k)
            found = True
            break
        if not found:
            raise ValueError("exact ear clipping could not triangulate polygon")
    a, b, c = (points[i] for i in remaining)
    if cross(a, b, c) <= 0:
        raise ValueError("polygon triangulation ended with a degenerate triangle")
    triangles.append((a, b, c))
    if sum(abs(cross(*tri)) for tri in triangles) != abs(area2(poly)):
        raise ValueError("triangulation does not preserve polygon area")
    return tuple(triangles)


def _typed_int_list(value, name):
    if not isinstance(value, list) or any(type(x) is not int for x in value):
        raise ValueError(f"{name} must be a list of integers")
    return value


@lru_cache(maxsize=1)
def load_instance():
    raw = SOURCE_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INSTANCE_SHA256:
        raise ValueError("frozen instance SHA-256 mismatch")
    data = json.loads(raw)
    if data.get("instance_name") != INSTANCE_NAME or data.get("type") != "cgshop2024_instance":
        raise ValueError("unexpected instance identity or format")
    if type(data.get("num_items")) is not int or data["num_items"] != TYPE_COUNT:
        raise ValueError("unexpected item type count")
    container_obj = data.get("container")
    container_x = _typed_int_list(container_obj.get("x"), "container.x")
    container_y = _typed_int_list(container_obj.get("y"), "container.y")
    if len(container_x) != len(container_y):
        raise ValueError("container coordinate arrays have different lengths")
    container = tuple(zip(container_x, container_y))
    item_defs = data.get("items")
    if not isinstance(item_defs, list) or len(item_defs) != TYPE_COUNT:
        raise ValueError("unexpected item definitions")
    items = []
    for item in item_defs:
        if type(item.get("value")) is not int or item["value"] < 0:
            raise ValueError("item values must be nonnegative integers")
        if type(item.get("quantity")) is not int or item["quantity"] < 0:
            raise ValueError("item quantities must be nonnegative integers")
        x = _typed_int_list(item.get("x"), "item.x")
        y = _typed_int_list(item.get("y"), "item.y")
        if len(x) != len(y):
            raise ValueError("item coordinate arrays have different lengths")
        polygon = tuple(zip(x, y))
        triangles = triangulate(polygon)
        items.append({"value": item["value"], "quantity": item["quantity"],
                      "polygon": polygon, "triangles": triangles,
                      "area2": abs(area2(polygon))})
    if sum(i["quantity"] for i in items) != AVAILABLE_COUNT:
        raise ValueError("unexpected total available item count")
    container_triangles = triangulate(container)
    return {"container": container, "container_triangles": container_triangles,
            "container_bbox": polygon_bbox(container), "container_area2": abs(area2(container)),
            "items": tuple(items), "metadata": data.get("meta", {})}


def translate_polygon(poly, dx, dy):
    return tuple((x + dx, y + dy) for x, y in poly)


def translate_triangles(triangles, dx, dy):
    return tuple(tuple((x + dx, y + dy) for x, y in tri) for tri in triangles)


def polygon_bbox(poly):
    return min(p[0] for p in poly), min(p[1] for p in poly), max(p[0] for p in poly), max(p[1] for p in poly)


def bboxes_have_positive_overlap(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])
