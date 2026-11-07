"""Exact checker for the fixed CG:SHOP 2020 convex-partition instance."""

from __future__ import annotations

from collections import defaultdict, deque
from decimal import Decimal
from functools import cmp_to_key
import json
from pathlib import Path

CONFIG_ID = "T095-C01"
_EXPECTED = {
    "instance": "uniform-0000500-1",
    "point_count": 500,
    "input_coordinates": "exact integer coordinates",
    "partition": "straight-line planar graph; all input points are vertices; bounded faces are empty convex polygons",
    "objective": "minimize number of internal convex faces",
}
_TASK_DIR = Path(__file__).parent
_INSTANCE_PATH = _TASK_DIR / "data/source/uniform-0000500-1.instance.json"


def _int_coord(value, label):
    if isinstance(value, bool):
        raise ValueError(f"{label} must be an integer coordinate")
    if isinstance(value, int):
        return value
    if isinstance(value, Decimal) and value.is_finite() and value == value.to_integral_value():
        return int(value)
    raise ValueError(f"{label} must be an exact finite integer coordinate")


def load_points():
    try:
        raw = json.loads(_INSTANCE_PATH.read_text(), parse_float=Decimal)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("The pinned CG:SHOP instance file is missing or invalid") from exc
    if raw.get("type") != "Instance" or raw.get("name") != _EXPECTED["instance"]:
        raise ValueError("The pinned input is not uniform-0000500-1")
    entries = raw.get("points")
    if not isinstance(entries, list) or len(entries) != _EXPECTED["point_count"]:
        raise ValueError("The fixed instance must contain exactly 500 points")
    out = []
    for expected_id, item in enumerate(entries):
        if not isinstance(item, dict) or item.get("i") != expected_id:
            raise ValueError("Input point ids must be consecutive from zero")
        out.append((_int_coord(item.get("x"), "x"), _int_coord(item.get("y"), "y")))
    if len(set(out)) != len(out):
        raise ValueError("The pinned input contains duplicate point coordinates")
    return out


def _cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])


def _on_segment(a, b, p):
    return (_cross(a, b, p) == 0
            and min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
            and min(a[1], b[1]) <= p[1] <= max(a[1], b[1]))


def _segments_intersect(a, b, c, d):
    o1, o2 = _cross(a, b, c), _cross(a, b, d)
    o3, o4 = _cross(c, d, a), _cross(c, d, b)
    if o1 == 0 and _on_segment(a, b, c): return True
    if o2 == 0 and _on_segment(a, b, d): return True
    if o3 == 0 and _on_segment(c, d, a): return True
    if o4 == 0 and _on_segment(c, d, b): return True
    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)


def _hull_with_collinear_boundary(points):
    ordered = sorted(range(len(points)), key=lambda i: (points[i][0], points[i][1]))
    lower, upper = [], []
    for i in ordered:
        while len(lower) >= 2 and _cross(points[lower[-2]], points[lower[-1]], points[i]) < 0:
            lower.pop()
        lower.append(i)
    for i in reversed(ordered):
        while len(upper) >= 2 and _cross(points[upper[-2]], points[upper[-1]], points[i]) < 0:
            upper.pop()
        upper.append(i)
    hull = lower[:-1] + upper[:-1]
    if len(hull) < 3 or len(set(hull)) != len(hull):
        raise ValueError("The fixed input must have a nondegenerate convex hull")
    return hull


def _area2(cycle, points):
    return sum(points[cycle[i]][0] * points[cycle[(i+1) % len(cycle)]][1]
               - points[cycle[(i+1) % len(cycle)]][0] * points[cycle[i]][1]
               for i in range(len(cycle)))


def _angle_half(v):
    return 0 if v[1] > 0 or (v[1] == 0 and v[0] >= 0) else 1


def _angle_compare(origin, points, ia, ib):
    va = (points[ia][0]-points[origin][0], points[ia][1]-points[origin][1])
    vb = (points[ib][0]-points[origin][0], points[ib][1]-points[origin][1])
    ha, hb = _angle_half(va), _angle_half(vb)
    if ha != hb:
        return -1 if ha < hb else 1
    det = va[0]*vb[1] - va[1]*vb[0]
    if det:
        return -1 if det > 0 else 1
    return 0


def _face_cycles(points, edges):
    neighbors = [[] for _ in points]
    for u, v in edges:
        neighbors[u].append(v)
        neighbors[v].append(u)
    for u in range(len(points)):
        neighbors[u].sort(key=cmp_to_key(lambda a, b, u=u: _angle_compare(u, points, a, b)))
        if len(set(neighbors[u])) != len(neighbors[u]):
            raise ValueError("Duplicate graph neighbors")
        for i in range(1, len(neighbors[u])):
            a, b = neighbors[u][i-1], neighbors[u][i]
            va = (points[a][0]-points[u][0], points[a][1]-points[u][1])
            vb = (points[b][0]-points[u][0], points[b][1]-points[u][1])
            if va[0]*vb[1] - va[1]*vb[0] == 0 and va[0]*vb[0]+va[1]*vb[1] > 0:
                raise ValueError("Two incident edges overlap on the same ray")
    seen = set()
    cycles = []
    directed = {(u, v) for u, v in edges} | {(v, u) for u, v in edges}
    for start in directed:
        if start in seen:
            continue
        cycle = []
        edge = start
        while edge not in seen:
            seen.add(edge)
            u, v = edge
            cycle.append(u)
            around = neighbors[v]
            try:
                back = around.index(u)
            except ValueError as exc:
                raise ValueError("Malformed planar embedding") from exc
            w = around[(back - 1) % len(around)]
            edge = (v, w)
            if len(cycle) > len(directed) + 1:
                raise ValueError("Face walk did not close")
        if edge != start:
            raise ValueError("Planar face walks overlap inconsistently")
        cycles.append(cycle)
    if seen != directed:
        raise ValueError("Not all directed edges were assigned to a face")
    return cycles


def _check_cycle_convex(cycle, points):
    if len(cycle) < 3 or len(set(cycle)) != len(cycle):
        raise ValueError("Every bounded face must be a simple polygon")
    if _area2(cycle, points) <= 0:
        raise ValueError("Bounded face orientation or area is invalid")
    n = len(cycle)
    for i in range(n):
        if _cross(points[cycle[i]], points[cycle[(i+1) % n]],
                  points[cycle[(i+2) % n]]) < 0:
            raise ValueError("Every bounded face must be convex")


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError("Unknown T095 configuration")
    params = config.get("parameters")
    if (not isinstance(params, dict) or params.keys() != _EXPECTED.keys()
            or any(type(params[k]) is not type(v) or params[k] != v
                   for k, v in _EXPECTED.items())):
        raise ValueError("T095 parameters do not match the fixed instance")
    if config.get("direction") != "minimize":
        raise ValueError("T095 is a minimization configuration")
    if not isinstance(solution, dict) or not isinstance(solution.get("edges"), list):
        raise ValueError("Solution must contain an edges list")
    points = load_points()
    n = len(points)
    raw_edges = solution["edges"]
    if len(raw_edges) > 3*n - 6:
        raise ValueError("Too many edges for a simple planar graph")
    edges, edge_set = [], set()
    for edge in raw_edges:
        if not isinstance(edge, dict) or set(edge) != {"i", "j"}:
            raise ValueError("Each edge must contain exactly integer endpoint ids i and j")
        u, v = edge["i"], edge["j"]
        if type(u) is not int or type(v) is not int or not (0 <= u < n and 0 <= v < n):
            raise ValueError("Edge endpoint ids must be valid integer point ids")
        if u == v:
            raise ValueError("Self-loop edges are invalid")
        key = (min(u, v), max(u, v))
        if key in edge_set:
            raise ValueError("Duplicate edges are invalid")
        edge_set.add(key)
        edges.append(key)

    degrees = [0] * n
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
        a, b = points[u], points[v]
        for k, p in enumerate(points):
            if k not in (u, v) and _on_segment(a, b, p):
                raise ValueError("An edge passes through a third input point")

    for i, (u, v) in enumerate(edges):
        common = {u, v}
        a, b = points[u], points[v]
        for x, y in edges[i+1:]:
            shared = common & {x, y}
            c, d = points[x], points[y]
            if not shared:
                if _segments_intersect(a, b, c, d):
                    raise ValueError("Graph edges cross or touch away from a shared endpoint")
            else:
                shared_vertex = next(iter(shared))
                p = points[shared_vertex]
                q = points[v if shared_vertex == u else u]
                r = points[y if shared_vertex == x else x]
                va = (q[0]-p[0], q[1]-p[1])
                vb = (r[0]-p[0], r[1]-p[1])
                if va[0]*vb[1] - va[1]*vb[0] == 0 and va[0]*vb[0]+va[1]*vb[1] > 0:
                    raise ValueError("Incident edges overlap beyond their shared endpoint")

    if any(degree == 0 for degree in degrees):
        raise ValueError("Every input point must be used as a graph vertex")
    adjacency = [[] for _ in points]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    reached = {0}
    todo = [0]
    while todo:
        u = todo.pop()
        for v in adjacency[u]:
            if v not in reached:
                reached.add(v)
                todo.append(v)
    if len(reached) != n:
        raise ValueError("The partition graph must be connected")

    hull = _hull_with_collinear_boundary(points)
    for a, b in zip(hull, hull[1:] + hull[:1]):
        if (min(a, b), max(a, b)) not in edge_set:
            raise ValueError("Every consecutive convex-hull boundary edge is required")

    cycles = _face_cycles(points, edges)
    if len(cycles) != len(edges) - n + 2:
        raise ValueError("The planar face count fails Euler's formula")
    bounded = [cycle for cycle in cycles if _area2(cycle, points) > 0]
    outer = [cycle for cycle in cycles if _area2(cycle, points) < 0]
    if len(outer) != 1 or len(bounded) != len(edges) - n + 1:
        raise ValueError("The embedding must have one outer face and the expected bounded faces")

    face_area2 = 0
    for cycle in bounded:
        _check_cycle_convex(cycle, points)
        for p_id, p in enumerate(points):
            if p_id in cycle:
                continue
            signs = [_cross(points[cycle[i]], points[cycle[(i+1) % len(cycle)]], p)
                     for i in range(len(cycle))]
            if all(sign >= 0 for sign in signs):
                raise ValueError("A bounded face contains another input point")
        face_area2 += _area2(cycle, points)
    hull_area2 = abs(_area2(hull, points))
    if face_area2 != hull_area2:
        raise ValueError("Bounded faces do not exactly cover the convex hull area")
    return {
        "objective": len(bounded),
        "objective_value": len(bounded),
        "verification_status": "exact",
        "details": {
            "point_count": n,
            "edge_count": len(edges),
            "face_count": len(bounded),
            "convex_hull_vertex_count_including_collinear": len(hull),
            "hull_area_twice": hull_area2,
            "bounded_face_area_twice_sum": face_area2,
            "euler_edge_face_check": len(edges) - n + 1,
            "claimed_score_ignored": True,
        },
    }
