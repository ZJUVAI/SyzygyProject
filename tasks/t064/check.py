"""Exact rational checker for a non-obtuse triangulation of ortho_40."""
import hashlib
import json
import sys
from functools import cmp_to_key, lru_cache
from fractions import Fraction
from math import lcm
from pathlib import Path


CONFIG_ID = "T064-C01"
INSTANCE_UID = "ortho_40_56a6f463"
INSTANCE_SHA256 = "f379e17cc7b4370d092ed37dcb6293dcb01c71d4f4c8e6cc4418c39ce178cad7"
MAX_STEINER = 2000

# Let the shared verification-process limits, rather than Python's decimal
# digit default, bound arbitrary-precision rational coordinate strings.
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


@lru_cache(maxsize=1)
def _instance():
    path = Path(__file__).with_name("data") / "source" / "ortho40.instance.json"
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INSTANCE_SHA256:
        raise ValueError("fixed ortho40 input file hash does not match")
    data = json.loads(raw)
    if data.get("instance_uid") != INSTANCE_UID or data.get("num_points") != 40:
        raise ValueError("fixed input does not match T064-C01")
    if data.get("num_constraints") != 0 or data.get("additional_constraints") != []:
        raise ValueError("T064-C01 requires no additional constraints")
    if not (len(data["points_x"]) == len(data["points_y"]) == 40):
        raise ValueError("fixed input must have 40 coordinates")
    points = tuple((Fraction(x), Fraction(y)) for x, y in zip(data["points_x"], data["points_y"]))
    boundary = tuple(data["region_boundary"])
    if len(boundary) != 40 or set(boundary) != set(range(40)):
        raise ValueError("fixed boundary must contain each input vertex once")
    polygon = tuple(points[i] for i in boundary)
    if _area2(polygon) == 0:
        raise ValueError("fixed polygon has zero area")
    return data, points, boundary, polygon


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _dot(a, b, c):
    return (b[0] - a[0]) * (c[0] - a[0]) + (b[1] - a[1]) * (c[1] - a[1])


def _area2(points):
    return sum(a[0] * b[1] - b[0] * a[1]
               for a, b in zip(points, points[1:] + points[:1]))


def _on_segment(a, b, p):
    return (_cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _orientation(a, b, c):
    value = _cross(a, b, c)
    return (value > 0) - (value < 0)


def _segments_intersect(a, b, c, d):
    if (max(a[0], b[0]) < min(c[0], d[0])
            or max(c[0], d[0]) < min(a[0], b[0])
            or max(a[1], b[1]) < min(c[1], d[1])
            or max(c[1], d[1]) < min(a[1], b[1])):
        return False
    o1, o2 = _orientation(a, b, c), _orientation(a, b, d)
    o3, o4 = _orientation(c, d, a), _orientation(c, d, b)
    if o1 == 0 and _on_segment(a, b, c):
        return True
    if o2 == 0 and _on_segment(a, b, d):
        return True
    if o3 == 0 and _on_segment(c, d, a):
        return True
    if o4 == 0 and _on_segment(c, d, b):
        return True
    return o1 * o2 < 0 and o3 * o4 < 0


def _point_location(point, polygon):
    """Return -1 outside, 0 on boundary, +1 inside, using exact rationals."""
    inside = False
    x, y = point
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        if _on_segment(a, b, point):
            return 0
        if (a[1] > y) != (b[1] > y):
            x_hit = a[0] + Fraction((y - a[1]) * (b[0] - a[0]), b[1] - a[1])
            if x_hit > x:
                inside = not inside
    return 1 if inside else -1


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("boolean coordinate is not allowed")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("coordinate must be finite")
        return Fraction.from_float(value)
    if isinstance(value, str):
        if not value:
            raise ValueError("coordinate text is empty")
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            raise ValueError("coordinate string must be a finite rational") from exc
    raise ValueError("coordinates must be integers, finite floats, or rational strings")


def _validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    cid = config.get("id", CONFIG_ID)
    params = config.get("parameters", config)
    if cid != CONFIG_ID or not isinstance(params, dict):
        raise ValueError("unsupported T064 configuration")
    if params.get("instance_uid", INSTANCE_UID) != INSTANCE_UID:
        raise ValueError("configuration must use the fixed ortho40 instance")
    if params.get("coordinate_domain", "rational") != "rational":
        raise ValueError("this checker accepts exact rational-coordinate constructions")


def _validate_edge_intersections(points, edges):
    for i, (u, v) in enumerate(edges):
        a, b = points[u], points[v]
        for j in range(i + 1, len(edges)):
            w, z = edges[j]
            common = {u, v}.intersection((w, z))
            c, d = points[w], points[z]
            if not _segments_intersect(a, b, c, d):
                continue
            if common:
                joint = points[next(iter(common))]
                other1 = points[(v if u in common else u)]
                other2 = points[(z if w in common else w)]
                # Collinear rays from a shared endpoint overlap beyond that point.
                if _cross(joint, other1, other2) == 0 and _dot(joint, other1, other2) > 0:
                    raise ValueError("edges overlap beyond a shared endpoint")
                continue
            raise ValueError("edges cross or touch without a shared vertex")


def _edge_inside_polygon(a, b, polygon):
    # Any non-endpoint intersection with the polygon boundary is forbidden.
    for c, d in zip(polygon, polygon[1:] + polygon[:1]):
        if not _segments_intersect(a, b, c, d):
            continue
        if _cross(a, b, c) == 0 and _cross(a, b, d) == 0:
            # A boundary edge may span several consecutive collinear input
            # segments. Exact interior samples below decide whether it leaves
            # the polygon at either end.
            continue
        # A graph endpoint may meet the boundary. A polygon corner in the
        # interior of an edge is not a graph vertex and is not permitted.
        if (a == c or a == d or b == c or b == d
                or _on_segment(c, d, a) or _on_segment(c, d, b)):
            continue
        raise ValueError("an edge crosses the polygon boundary")

    # Check the open portions between all polygon corners met by this segment.
    breaks = {Fraction(0), Fraction(1)}
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p in polygon:
        if _on_segment(a, b, p):
            t = Fraction(p[0] - a[0], dx) if dx else Fraction(p[1] - a[1], dy)
            breaks.add(t)
    ordered = sorted(breaks)
    for left, right in zip(ordered, ordered[1:]):
        t = (left + right) / 2
        sample = (a[0] + t * dx, a[1] + t * dy)
        if _point_location(sample, polygon) < 0:
            raise ValueError("an edge leaves the polygon")


def _check_boundary_coverage(points, edges, polygon):
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        dx = b[0] - a[0]
        axis = 0 if dx else 1
        length = b[axis] - a[axis]
        intervals = []
        for u, v in edges:
            p, q = points[u], points[v]
            if _on_segment(a, b, p) and _on_segment(a, b, q):
                t1 = Fraction(p[axis] - a[axis], length)
                t2 = Fraction(q[axis] - a[axis], length)
                intervals.append((min(t1, t2), max(t1, t2)))
        intervals.sort()
        end = Fraction(0)
        for left, right in intervals:
            if left != end or right <= left:
                raise ValueError("boundary edge coverage has a gap or overlap")
            end = right
        if end != 1:
            raise ValueError("a polygon boundary segment is not fully covered")


def _faces(points, edges, vertex_count):
    adjacency = [[] for _ in range(vertex_count)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)

    def compare(center, u, v):
        a = (points[u][0] - points[center][0], points[u][1] - points[center][1])
        b = (points[v][0] - points[center][0], points[v][1] - points[center][1])
        ha = 0 if a[1] > 0 or (a[1] == 0 and a[0] >= 0) else 1
        hb = 0 if b[1] > 0 or (b[1] == 0 and b[0] >= 0) else 1
        if ha != hb:
            return -1 if ha < hb else 1
        turn = a[0] * b[1] - a[1] * b[0]
        if turn:
            return -1 if turn > 0 else 1
        raise ValueError("two incident edges have the same direction")

    for center in range(vertex_count):
        adjacency[center].sort(key=cmp_to_key(lambda u, v: compare(center, u, v)))

    visited = set()
    positive = []
    negative_count = 0
    for u, v in ((u, v) for edge in edges for u, v in (edge, edge[::-1])):
        start = (u, v)
        if start in visited:
            continue
        cycle = []
        current = start
        for _ in range(2 * len(edges) + 1):
            if current in visited:
                break
            visited.add(current)
            x, y = current
            cycle.append(x)
            around = adjacency[y]
            reverse_index = around.index(x)
            current = (y, around[(reverse_index - 1) % len(around)])
            if current == start:
                break
        if current != start:
            raise ValueError("planar face walk did not close")
        area = _area2(tuple(points[i] for i in cycle))
        if area == 0:
            raise ValueError("degenerate zero-area face in triangulation")
        if area > 0:
            if len(cycle) != 3 or len(set(cycle)) != 3:
                raise ValueError("every bounded face must be a triangle")
            tri = tuple(points[i] for i in cycle)
            for i in range(3):
                if _dot(tri[i], tri[(i + 1) % 3], tri[(i + 2) % 3]) < 0:
                    raise ValueError("triangle has an obtuse angle")
            positive.append(area)
        else:
            negative_count += 1
    if len(visited) != 2 * len(edges) or negative_count != 1:
        raise ValueError("embedding must have one outer face and all edge sides visited")
    return positive


def validate(solution, config, strict=False):
    _validate_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    data, original, boundary, polygon = _instance()
    if "instance_uid" in solution and solution["instance_uid"] != INSTANCE_UID:
        raise ValueError("solution instance_uid does not match")

    sx, sy = solution.get("steiner_points_x"), solution.get("steiner_points_y")
    if not isinstance(sx, list) or not isinstance(sy, list) or len(sx) != len(sy):
        raise ValueError("Steiner coordinate arrays must be lists of equal length")
    if len(sx) > MAX_STEINER:
        raise ValueError("too many Steiner points")
    steiner = tuple((_fraction(x), _fraction(y)) for x, y in zip(sx, sy))
    points = original + steiner
    if len(set(points)) != len(points):
        raise ValueError("duplicate coordinates are not allowed")
    scale = 1
    for point in points:
        scale = lcm(scale, point[0].denominator, point[1].denominator)
    exact_points = tuple((int(x * scale), int(y * scale)) for x, y in points)
    exact_polygon = tuple(exact_points[i] for i in boundary)
    for point in exact_points[len(original):]:
        if _point_location(point, exact_polygon) < 0:
            raise ValueError("Steiner points must lie in the polygon closure")

    raw_edges = solution.get("edges")
    if not isinstance(raw_edges, list):
        raise ValueError("edges must be a list")
    vertex_count = len(points)
    if len(raw_edges) > max(0, 3 * vertex_count - 6):
        raise ValueError("edge count exceeds a planar graph bound")
    edges = []
    seen = set()
    for edge in raw_edges:
        if not isinstance(edge, list) or len(edge) != 2:
            raise ValueError("each edge must be a pair of vertex indices")
        u, v = edge
        if any(isinstance(x, bool) or not isinstance(x, int) for x in (u, v)):
            raise ValueError("edge indices must be integers, not booleans")
        if u < 0 or v < 0 or u >= vertex_count or v >= vertex_count or u == v:
            raise ValueError("edge endpoint is out of range or a self-loop")
        key = tuple(sorted((u, v)))
        if key in seen:
            raise ValueError("duplicate undirected edge")
        seen.add(key)
        edges.append(key)
    if not edges:
        raise ValueError("triangulation has no edges")

    degree = [0] * vertex_count
    adjacency = [[] for _ in range(vertex_count)]
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
        adjacency[u].append(v)
        adjacency[v].append(u)
    if any(d < 2 for d in degree):
        raise ValueError("every listed vertex must be part of the triangulation")
    reached = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in reached:
                reached.add(v)
                stack.append(v)
    if len(reached) != vertex_count:
        raise ValueError("triangulation graph must be connected")

    _validate_edge_intersections(exact_points, edges)
    for u, v in edges:
        _edge_inside_polygon(exact_points[u], exact_points[v], exact_polygon)
    _check_boundary_coverage(exact_points, edges, exact_polygon)

    triangle_areas2 = _faces(exact_points, edges, vertex_count)
    polygon_area2_scaled = abs(_area2(exact_polygon))
    if sum(triangle_areas2, Fraction(0)) != polygon_area2_scaled:
        raise ValueError("bounded triangles do not cover the complete polygon area")
    expected_faces = len(edges) - vertex_count + 1
    if len(triangle_areas2) != expected_faces:
        raise ValueError("Euler face count does not match a connected triangulation")

    return {
        "objective": len(steiner),
        "verification_status": "exact",
        "details": {
            "instance_uid": INSTANCE_UID,
            "coordinate_domain": "exact rational coordinates; finite floats are interpreted as exact binary rationals",
            "input_vertices": len(original),
            "steiner_points": len(steiner),
            "total_vertices": vertex_count,
            "edges": len(edges),
            "bounded_triangles": len(triangle_areas2),
            "polygon_area2": str(Fraction(polygon_area2_scaled, scale * scale)),
            "triangle_area2_sum": str(Fraction(sum(triangle_areas2, Fraction(0)), scale * scale)),
            "all_edges_inside": True,
            "all_boundary_segments_covered": True,
            "all_triangles_nonobtuse": True,
            "claimed_objective_ignored": True,
        },
    }
