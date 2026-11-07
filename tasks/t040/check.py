"""Exact rational checker for inscribed-polytope volume configurations."""
from fractions import Fraction
from tasks.t040.init_program import CONFIG_SIZES
from functools import reduce
from itertools import combinations
import math

_CONFIG = {
    "id": "T040-C01",
    "parameters": {
        "n": 11,
        "space": "unit sphere S2 in R3",
        "objective": "Euclidean volume of the convex hull",
        "objective_unit": "unit-radius cubed",
    },
}


def _q(value):
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("invalid rational coordinate") from exc
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("coordinates must be finite")
        return Fraction.from_float(value)
    raise ValueError("coordinates must be integers, finite floats, or rational strings")


def _cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def _dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Fraction())


def _canonical_plane(normal, d):
    vals = tuple(normal) + (d,)
    den = math.lcm(*(v.denominator for v in vals))
    ints = [v.numerator * (den // v.denominator) for v in vals]
    g = reduce(math.gcd, (abs(v) for v in ints))
    ints = [v // g for v in ints]
    first = next(v for v in ints if v)
    if first < 0:
        ints = [-v for v in ints]
    return tuple(ints)


def _hull2(points, indices, axes):
    """Return the exact monotone-chain hull of coplanar points in projection."""
    coords = sorted((points[i][axes[0]], points[i][axes[1]], i) for i in indices)
    def turn(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower = []
    for p in coords:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(coords):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return [p[2] for p in lower[:-1] + upper[:-1]]


def _exact_hull_volume(points):
    faces = {}
    triples_seen = 0
    n = len(points)
    for i, j, k in combinations(range(n), 3):
        normal = _cross(tuple(points[j][m]-points[i][m] for m in range(3)),
                        tuple(points[k][m]-points[i][m] for m in range(3)))
        if normal == (0, 0, 0):
            continue
        d = -_dot(normal, points[i])
        signs = [_dot(normal, p) + d for p in points]
        if any(s > 0 for s in signs) and any(s < 0 for s in signs):
            continue
        # Orient the plane so its interior is in the non-positive halfspace.
        if any(s > 0 for s in signs):
            normal = tuple(-v for v in normal)
            d = -d
            signs = [-s for s in signs]
        key = _canonical_plane(normal, d)
        face = faces.setdefault(key, {"normal": normal, "indices": set()})
        face["indices"].update(idx for idx, s in enumerate(signs) if s == 0)
        triples_seen += 1

    if len(faces) < 4:
        raise ValueError("points do not span a three-dimensional convex hull")
    volume6 = Fraction()
    triangles = 0
    for face in faces.values():
        nvec = face["normal"]
        drop = max(range(3), key=lambda axis: abs(nvec[axis]))
        if drop == 0:
            axes = (1, 2)
        elif drop == 1:
            axes = (0, 2)
        else:
            axes = (0, 1)
        polygon = _hull2(points, face["indices"], axes)
        if len(polygon) < 3:
            raise ValueError("degenerate supporting face")
        a, b, c = (points[polygon[t]] for t in range(3))
        orientation = _cross(tuple(b[m]-a[m] for m in range(3)),
                             tuple(c[m]-a[m] for m in range(3)))
        if _dot(orientation, nvec) < 0:
            polygon.reverse()
        p0 = points[polygon[0]]
        for t in range(1, len(polygon)-1):
            p1, p2 = points[polygon[t]], points[polygon[t+1]]
            volume6 += _dot(p0, _cross(p1, p2))
            triangles += 1
    volume = volume6 / 6
    if volume <= 0:
        raise ValueError("failed to orient the convex hull boundary")
    return volume, len(faces), triangles, triples_seen


def _parse_points(solution, n):
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    if "points" in solution:
        raw_points = solution["points"]
        if not isinstance(raw_points, (list, tuple)):
            raise ValueError("points must be a list")
        if any(not isinstance(p, (list, tuple)) or len(p) != 3 for p in raw_points):
            raise ValueError("each point must have three coordinates")
        points = [tuple(_q(x) for x in p) for p in raw_points]
        representation = "exact Cartesian coordinates"
    elif "stereographic" in solution:
        raw_points = solution["stereographic"]
        if not isinstance(raw_points, (list, tuple)):
            raise ValueError("stereographic parameters must be a list")
        points = []
        for pair in raw_points:
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                raise ValueError("each stereographic parameter must be a pair")
            u, v = (_q(x) for x in pair)
            den = 1 + u*u + v*v
            points.append((2*u/den, 2*v/den, (1-u*u-v*v)/den))
        representation = "rational stereographic parameters; south pole is omitted"
    else:
        raise ValueError("solution must contain points or stereographic parameters")
    if len(points) != n:
        raise ValueError(f"expected exactly {n} points")
    if len(set(points)) != n:
        raise ValueError("duplicate points are not allowed")
    for p in points:
        if sum((x*x for x in p), Fraction()) != 1:
            raise ValueError("every point must lie exactly on the unit sphere")
    return points, representation


def validate(solution, config, strict=False):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    n = CONFIG_SIZES.get(config.get("id"))
    if n is None or config.get("parameters") != dict(_CONFIG["parameters"], n=n):
        raise ValueError("unsupported configuration")
    points, representation = _parse_points(solution, n)
    volume, face_count, triangle_count, supporting_triples = _exact_hull_volume(points)
    return {
        "objective": str(volume),
        "objective_value": str(volume),
        "verification_status": "exact",
        "details": {
            "objective_name": "convex_hull_volume",
            "hull_method": "exact rational supporting-plane enumeration and exact coplanar-face hulls",
            "supporting_triples_checked": math.comb(n, 3),
            "supporting_triples_found": supporting_triples,
            "unique_supporting_planes": face_count,
            "triangles_after_face_triangulation": triangle_count,
            "input_representation": representation,
            "claimed_objective_ignored": True,
        },
    }
