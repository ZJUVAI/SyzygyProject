"""Exact checker for a minimum convex cover of the fixed socg_fixed92 region."""
import hashlib
import json
from pathlib import Path

from tasks.t097.algebraic import RealAlgebraicField
from tasks.t097.geometry import certify_cover, cross, signed_double_area, validate_simple_boundary

TASK_DIR = Path(__file__).parent
INSTANCE_PATH = TASK_DIR / "data/source/socg_fixed92.instance.json"
INSTANCE_SHA256 = "573eb5e64a29369d17396fca899008702ba154865ec9ae343db173cd9aa04f38"
PARAMETERS = {
    "instance": "socg_fixed92",
    "instance_sha256": INSTANCE_SHA256,
    "boundary_vertices": 92,
    "holes": 0,
    "cover_domain": "all real convex polygons",
    "overlap_allowed": True,
}


def _fixed_domain(field):
    raw = INSTANCE_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INSTANCE_SHA256:
        raise ValueError("fixed public input checksum mismatch")
    source = json.loads(raw)
    if (source.get("name") != PARAMETERS["instance"] or source.get("n") != 92
            or source.get("holes") != [] or len(source.get("outer_boundary", [])) != 92):
        raise ValueError("fixed public input metadata mismatch")
    polygon = []
    for point in source["outer_boundary"]:
        if (not isinstance(point, dict) or type(point.get("x")) is not int
                or type(point.get("y")) is not int):
            raise ValueError("fixed input coordinates must be integers")
        polygon.append((field.const(point["x"]), field.const(point["y"])))
    validate_simple_boundary(field, polygon)
    return polygon


def _parse_pieces(field, raw_pieces):
    if not isinstance(raw_pieces, list) or not raw_pieces:
        raise ValueError("solution must contain at least one convex polygon")
    pieces = []
    for raw in raw_pieces:
        if not isinstance(raw, list) or len(raw) < 3:
            raise ValueError("each convex polygon needs at least three vertices")
        polygon = []
        for point in raw:
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError("each polygon vertex must be an [x,y] pair")
            polygon.append((field.element(point[0]), field.element(point[1])))
        if len(set(polygon)) != len(polygon):
            raise ValueError("a convex polygon cannot repeat a vertex")
        area = field.sign(signed_double_area(field, polygon))
        if area == 0:
            raise ValueError("convex polygons must have positive area")
        if area < 0:
            polygon.reverse()
        for a, b in zip(polygon, polygon[1:] + polygon[:1]):
            if a == b:
                raise ValueError("convex polygons cannot contain zero-length edges")
            if any(field.sign(cross(field, a, b, p)) < 0 for p in polygon):
                raise ValueError("a submitted polygon is not convex")
        pieces.append(polygon)
    return pieces


def validate(solution, config, strict=False):
    if (not isinstance(config, dict) or config.get("id") != "T097-C01"
            or config.get("direction") != "minimize"
            or not isinstance(config.get("parameters"), dict)
            or config["parameters"] != PARAMETERS
            or any(type(config["parameters"].get(k)) is not type(v) for k, v in PARAMETERS.items())):
        raise ValueError("unsupported configuration, objective direction, or parameters")
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    field = RealAlgebraicField(solution.get("algebraic_field"))
    domain = _fixed_domain(field)
    pieces = _parse_pieces(field, solution.get("polygons"))
    checked_cells = certify_cover(field, domain, pieces)
    count = len(pieces)
    return {
        "objective": count,
        "objective_value": count,
        "verification_status": "certified",
        "details": {
            "instance": PARAMETERS["instance"],
            "convex_polygon_count": count,
            "total_piece_vertices": sum(map(len, pieces)),
            "algebraic_field_degree": field.degree,
            "verified_open_arrangement_cells": checked_cells,
            "coverage_method": "Exact vertical decomposition of the full segment arrangement in one real algebraic number field. Every open cell is classified against the input polygon and the union of convex pieces; all sets are closed, so equality of interiors establishes equality of the closed regions.",
            "claimed_score_ignored": True,
        },
    }
