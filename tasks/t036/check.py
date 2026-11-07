"""Exact checker for rectilinear drawings of the complete graph K28."""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations

N = 28
CONFIG_ID = "T036-C01"


def _coordinate(value):
    if type(value) is int:
        # Keep integer arithmetic on the hot path. Fractions are retained
        # only for coordinates explicitly supplied as rational strings.
        return value
    if isinstance(value, str):
        try:
            result = Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("coordinate strings must be exact rational numbers") from exc
        if str(result) != value:
            raise ValueError("rational coordinate strings must be canonical")
        return result
    raise ValueError("coordinates must be integers or canonical rational strings; floats and bools are invalid")


def _orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _proper_cross(a, b, c, d):
    return (_orientation(a, b, c) * _orientation(a, b, d) < 0
            and _orientation(c, d, a) * _orientation(c, d, b) < 0)


def validate(solution, config, strict=False):
    del strict  # Feasibility and objective are exact for every candidate.
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    if config.get("id", CONFIG_ID) != CONFIG_ID:
        raise ValueError("configuration id must be T036-C01")
    params = config.get("parameters", config)
    expected = {
        "vertices": N,
        "graph": "complete graph K28",
        "general_position": "no three points collinear",
        "crossing_definition": "unordered pairs of disjoint straight edges whose relative interiors intersect",
    }
    if not isinstance(params, dict) or any(params.get(k) != v for k, v in expected.items()):
        raise ValueError("configuration must fix the complete graph K28")
    raw = solution.get("points")
    if not isinstance(raw, list) or len(raw) != N:
        raise ValueError("points must contain exactly 28 coordinate pairs")
    points = []
    for point in raw:
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError("each point must be a two-element list")
        points.append((_coordinate(point[0]), _coordinate(point[1])))
    if len(set(points)) != N:
        raise ValueError("all 28 points must be distinct")
    triple_checks = 0
    for i, j, k in combinations(range(N), 3):
        if _orientation(points[i], points[j], points[k]) == 0:
            raise ValueError(f"points {i}, {j}, and {k} are collinear")
        triple_checks += 1
    crossings = 0
    pair_checks = 0
    # Each four-set has three pairings into disjoint edges.
    for i, j, k, l in combinations(range(N), 4):
        q = (points[i], points[j], points[k], points[l])
        crossings += _proper_cross(q[0], q[1], q[2], q[3])
        crossings += _proper_cross(q[0], q[2], q[1], q[3])
        crossings += _proper_cross(q[0], q[3], q[1], q[2])
        pair_checks += 3
    return {
        "objective": crossings,
        "verification_status": "exact",
        "details": {
            "vertices": N,
            "general_position_triples_checked": triple_checks,
            "disjoint_edge_pairings_checked": pair_checks,
            "crossings_recomputed": crossings,
            "claimed_objective_ignored": True,
            "claimed_score_ignored": True
        }
    }
