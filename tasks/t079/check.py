"""Exact checker for Kakeya sets in F_31^3 represented by one line per direction."""

from itertools import product

P = 31
CONFIG_ID = "T079-C01"
PARAMETERS = {
    "field_order": 31,
    "dimension": 3,
    "direction_count": 993,
    "construction": "one affine line in each projective direction",
    "objective": "cardinality of the union of the represented lines",
}


def directions():
    """Canonical representatives with the last nonzero coordinate equal to 1."""
    out = []
    for a, b in product(range(P), repeat=2):
        out.append((a, b, 1))
    for a in range(P):
        out.append((a, 1, 0))
    out.append((1, 0, 0))
    return tuple(out)


CANONICAL_DIRECTIONS = directions()
_DIRECTION_SET = set(CANONICAL_DIRECTIONS)


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_config(config):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError("unsupported T079 configuration")
    params = config.get("parameters")
    if not isinstance(params, dict) or params.keys() != PARAMETERS.keys():
        raise ValueError("unsupported T079 parameters")
    if any(type(params[k]) is not type(v) or params[k] != v for k, v in PARAMETERS.items()):
        raise ValueError("unsupported T079 parameters")


def line_points(origin, direction):
    ox, oy, oz = origin
    dx, dy, dz = direction
    return {
        ((ox + t * dx) % P, (oy + t * dy) % P, (oz + t * dz) % P)
        for t in range(P)
    }


def validate(solution, config=None, strict=False):
    """Check all 993 directions and compute the union exactly over F_31^3."""
    _validate_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be a JSON object")
    raw_lines = solution.get("lines")
    if not isinstance(raw_lines, list):
        raise ValueError("lines must be a list")
    if len(raw_lines) != len(CANONICAL_DIRECTIONS):
        raise ValueError("exactly 993 direction-line records are required")

    seen = set()
    union = set()
    for record in raw_lines:
        if not isinstance(record, dict) or record.keys() != {"direction", "origin"}:
            raise ValueError("each line record must contain direction and origin")
        raw_direction = record["direction"]
        raw_origin = record["origin"]
        if (not isinstance(raw_direction, (list, tuple)) or len(raw_direction) != 3
                or not all(_is_int(x) for x in raw_direction)):
            raise ValueError("direction must contain three integer coordinates")
        if (not isinstance(raw_origin, (list, tuple)) or len(raw_origin) != 3
                or not all(_is_int(x) for x in raw_origin)):
            raise ValueError("origin must contain three integer coordinates")
        direction = tuple(raw_direction)
        origin = tuple(raw_origin)
        if direction not in _DIRECTION_SET:
            raise ValueError("direction is not a canonical projective representative")
        if direction in seen:
            raise ValueError("duplicate projective direction")
        if any(x < 0 or x >= P for x in origin):
            raise ValueError("origin coordinate is outside 0..30")
        seen.add(direction)
        union.update(line_points(origin, direction))

    if seen != _DIRECTION_SET:
        raise ValueError("every projective direction must occur exactly once")
    objective = len(union)
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "field_order": P,
            "dimension": 3,
            "projective_directions_checked": len(seen),
            "line_points_generated": P * len(seen),
            "union_cardinality": objective,
            "full_space_cardinality": P ** 3,
            "claimed_objective_ignored": True,
        },
    }
