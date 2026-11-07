"""Exact validator for the fixed CG:SHOP polygon-packing instance."""

from fractions import Fraction

from tasks.t093.instance import (
    AVAILABLE_COUNT, INSTANCE_NAME, INSTANCE_SHA256, ITEM_LIMIT, TYPE_COUNT,
    bboxes_have_positive_overlap, load_instance, polygon_bbox, translate_polygon,
    translate_triangles,
)

CONFIG_ID = "T093-C01"
PARAMETERS = {
    "instance": INSTANCE_NAME,
    "container_vertices": 15,
    "item_types": TYPE_COUNT,
    "available_items_total": AVAILABLE_COUNT,
    "movement": "integer translations only; rotations forbidden",
    "feasibility": "each selected simple polygon is contained in the container; item interiors are pairwise disjoint; boundary contact is allowed",
    "objective": "maximize the sum of values of selected items",
}


def _typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_typed_equal(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_typed_equal(a, b) for a, b in zip(left, right))
    return left == right


def _check_config(config):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError(f"configuration id must be {CONFIG_ID}")
    if not _typed_equal(config.get("parameters"), PARAMETERS):
        raise ValueError("configuration does not match the frozen polygon-packing instance")
    if config.get("direction") != "maximize":
        raise ValueError("packed item value is a maximization objective")


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _tri_bbox(triangle):
    return (min(p[0] for p in triangle), min(p[1] for p in triangle),
            max(p[0] for p in triangle), max(p[1] for p in triangle))


def _positive_bbox_overlap(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1])


def _clip_polygon_by_triangle(subject, triangle):
    """Clip a polygon against a CCW triangle with exact rational arithmetic."""
    output = list(subject)
    for a, b in zip(triangle, triangle[1:] + triangle[:1]):
        if not output:
            return []
        old = output
        output = []
        start = old[-1]
        start_side = _cross(a, b, start)
        for end in old:
            end_side = _cross(a, b, end)
            start_inside = start_side >= 0
            end_inside = end_side >= 0
            if start_inside and end_inside:
                output.append(end)
            elif start_inside and not end_inside:
                t = Fraction(start_side, start_side - end_side)
                output.append((start[0] + t * (end[0] - start[0]),
                               start[1] + t * (end[1] - start[1])))
            elif not start_inside and end_inside:
                t = Fraction(start_side, start_side - end_side)
                output.append((start[0] + t * (end[0] - start[0]),
                               start[1] + t * (end[1] - start[1])))
                output.append(end)
            start, start_side = end, end_side
    return output


def _triangle_intersection_area(tri_a, bbox_a, tri_b, bbox_b):
    if not _positive_bbox_overlap(bbox_a, bbox_b):
        return Fraction(0)
    clipped = _clip_polygon_by_triangle(tri_a, tri_b)
    if len(clipped) < 3:
        return Fraction(0)
    area2 = sum(a[0] * b[1] - b[0] * a[1]
                for a, b in zip(clipped, clipped[1:] + clipped[:1]))
    return abs(area2) / 2


def _interiors_overlap(tris_a, bbox_a, tris_b, bbox_b):
    if not bboxes_have_positive_overlap(bbox_a, bbox_b):
        return False
    bboxes_a = [_tri_bbox(tri) for tri in tris_a]
    bboxes_b = [_tri_bbox(tri) for tri in tris_b]
    for tri_a, ta in zip(tris_a, bboxes_a):
        for tri_b, tb in zip(tris_b, bboxes_b):
            if _triangle_intersection_area(tri_a, ta, tri_b, tb) > 0:
                return True
    return False


def _translated_bbox(poly, dx, dy):
    x0, y0, x1, y1 = polygon_bbox(poly)
    return x0 + dx, y0 + dy, x1 + dx, y1 + dy


def placement_geometry(item_id, dx, dy, placed, data, container_tri_bboxes=None):
    """Return the exact polygon geometry when one proposed placement is valid."""
    item = data["items"][item_id]
    bbox = _translated_bbox(item["polygon"], dx, dy)
    container_bbox = data["container_bbox"]
    if (bbox[0] < container_bbox[0] or bbox[1] < container_bbox[1] or
            bbox[2] > container_bbox[2] or bbox[3] > container_bbox[3]):
        return None
    triangles = translate_triangles(item["triangles"], dx, dy)
    item_tri_bboxes = [_tri_bbox(tri) for tri in triangles]
    if container_tri_bboxes is None:
        container_tri_bboxes = [_tri_bbox(tri) for tri in data["container_triangles"]]
    inside_area = Fraction(0)
    for tri, tri_bbox in zip(triangles, item_tri_bboxes):
        for ctri, ctri_bbox in zip(data["container_triangles"], container_tri_bboxes):
            inside_area += _triangle_intersection_area(tri, tri_bbox, ctri, ctri_bbox)
    if inside_area != Fraction(item["area2"], 2):
        return None
    for old_triangles, old_bbox in placed:
        if _interiors_overlap(triangles, bbox, old_triangles, old_bbox):
            return None
    return triangles, bbox


def validate(solution, config, strict=False):
    del strict
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    item_ids = solution.get("item_indices")
    xs = solution.get("x_translations")
    ys = solution.get("y_translations")
    for name, values in (("item_indices", item_ids), ("x_translations", xs), ("y_translations", ys)):
        if not isinstance(values, list) or any(type(value) is not int for value in values):
            raise ValueError(f"{name} must be a list of integers; booleans are not accepted")
    count = len(item_ids)
    if count > ITEM_LIMIT or len(xs) != count or len(ys) != count:
        raise ValueError("placement arrays must have equal lengths and contain at most 50 items")
    if any(item_id < 0 or item_id >= TYPE_COUNT for item_id in item_ids):
        raise ValueError("item indices must be in the range 0 through 43")

    data = load_instance()
    container = data["container"]
    container_triangles = data["container_triangles"]
    container_bbox = data["container_bbox"]
    container_area = Fraction(data["container_area2"], 2)
    container_tri_bboxes = [_tri_bbox(tri) for tri in container_triangles]
    triangle_area = sum(
        _triangle_intersection_area(tri, bbox, tri, bbox)
        for tri, bbox in zip(container_triangles, container_tri_bboxes)
    )
    if triangle_area != container_area:
        raise ValueError("frozen container triangulation failed its exact area check")

    counts = [0] * TYPE_COUNT
    total_value = 0
    placed = []
    for item_id, dx, dy in zip(item_ids, xs, ys):
        item = data["items"][item_id]
        counts[item_id] += 1
        if counts[item_id] > item["quantity"]:
            raise ValueError("selected item multiplicity exceeds the available quantity")
        geometry = placement_geometry(item_id, dx, dy, placed, data, container_tri_bboxes)
        if geometry is None:
            raise ValueError("selected item is outside the container or overlaps a previous item")
        placed.append(geometry)
        total_value += item["value"]

    return {
        "objective": total_value,
        "verification_status": "exact",
        "details": {
            "instance": INSTANCE_NAME,
            "instance_sha256": INSTANCE_SHA256,
            "container_vertices": len(container),
            "item_types": TYPE_COUNT,
            "available_items_total": AVAILABLE_COUNT,
            "selected_items": count,
            "selected_type_counts": counts,
            "claimed_objective_ignored": True,
        },
    }
