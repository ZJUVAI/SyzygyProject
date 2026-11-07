"""Exact vertical-decomposition checks for polygon covers over Q(alpha)."""
from functools import cmp_to_key


def add(f, a, b):
    return f.add(a, b)


def sub(f, a, b):
    return f.sub(a, b)


def mul(f, a, b):
    return f.mul(a, b)


def div(f, a, b):
    return f.div(a, b)


def cross(f, a, b, c):
    return sub(f, mul(f, sub(f, b[0], a[0]), sub(f, c[1], a[1])),
               mul(f, sub(f, b[1], a[1]), sub(f, c[0], a[0])))


def compare_points(f, p, q):
    result = f.compare(p[0], q[0])
    return result if result else f.compare(p[1], q[1])


def point_on_segment(f, p, a, b):
    if f.sign(cross(f, a, b, p)):
        return False
    return (f.compare(p[0], min_field(f, a[0], b[0])) >= 0
            and f.compare(p[0], max_field(f, a[0], b[0])) <= 0
            and f.compare(p[1], min_field(f, a[1], b[1])) >= 0
            and f.compare(p[1], max_field(f, a[1], b[1])) <= 0)


def min_field(f, a, b):
    return a if f.compare(a, b) <= 0 else b


def max_field(f, a, b):
    return a if f.compare(a, b) >= 0 else b


def signed_double_area(f, polygon):
    total = f.const(0)
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        total = add(f, total, sub(f, mul(f, a[0], b[1]), mul(f, a[1], b[0])))
    return total


def validate_simple_boundary(f, polygon):
    n = len(polygon)
    if n < 3 or f.sign(signed_double_area(f, polygon)) <= 0:
        raise ValueError("the fixed input boundary must have positive counterclockwise area")
    segments = list(zip(polygon, polygon[1:] + polygon[:1]))
    for i, (a, b) in enumerate(segments):
        if a == b:
            raise ValueError("input boundary has a zero-length edge")
        for j in range(i + 1, n):
            c, d = segments[j]
            adjacent = j == i + 1 or (i == 0 and j == n - 1)
            if adjacent:
                continue
            o1, o2 = f.sign(cross(f, a, b, c)), f.sign(cross(f, a, b, d))
            o3, o4 = f.sign(cross(f, c, d, a)), f.sign(cross(f, c, d, b))
            if (o1 * o2 < 0 and o3 * o4 < 0
                    or (o1 == 0 and point_on_segment(f, c, a, b))
                    or (o2 == 0 and point_on_segment(f, d, a, b))
                    or (o3 == 0 and point_on_segment(f, a, c, d))
                    or (o4 == 0 and point_on_segment(f, b, c, d))):
                raise ValueError("fixed input boundary is not simple")


def _point_in_polygon(f, point, polygon):
    x, y = point
    inside = False
    for a, b in zip(polygon, polygon[1:] + polygon[:1]):
        ay, by = f.compare(a[1], y), f.compare(b[1], y)
        if (ay > 0) != (by > 0):
            x_intersection = add(f, a[0], div(f,
                mul(f, sub(f, y, a[1]), sub(f, b[0], a[0])), sub(f, b[1], a[1])))
            if f.compare(x_intersection, x) > 0:
                inside = not inside
    return inside


def _point_in_convex_piece(f, point, polygon):
    return all(f.sign(cross(f, a, b, point)) >= 0
               for a, b in zip(polygon, polygon[1:] + polygon[:1]))


def _segment_intersection_x(f, p, q, r, s):
    rx, ry = sub(f, q[0], p[0]), sub(f, q[1], p[1])
    sx, sy = sub(f, s[0], r[0]), sub(f, s[1], r[1])
    den = sub(f, mul(f, rx, sy), mul(f, ry, sx))
    if not den:
        return None
    qpx, qpy = sub(f, r[0], p[0]), sub(f, r[1], p[1])
    t = div(f, sub(f, mul(f, qpx, sy), mul(f, qpy, sx)), den)
    u = div(f, sub(f, mul(f, qpx, ry), mul(f, qpy, rx)), den)
    if (f.compare(t, f.const(0)) < 0 or f.compare(t, f.const(1)) > 0
            or f.compare(u, f.const(0)) < 0 or f.compare(u, f.const(1)) > 0):
        return None
    return add(f, p[0], mul(f, t, rx))


def _y_at_x(f, a, b, x):
    return add(f, a[1], div(f, mul(f, sub(f, x, a[0]), sub(f, b[1], a[1])), sub(f, b[0], a[0])))


def certify_cover(f, domain, pieces):
    """Prove union(pieces) equals domain by checking every open arrangement cell."""
    raw_segments = [(a, b) for poly in [domain, *pieces]
                    for a, b in zip(poly, poly[1:] + poly[:1])]
    segments_by_key = {}
    for a, b in raw_segments:
        if compare_points(f, a, b) <= 0:
            key = (a, b)
        else:
            key = (b, a)
        segments_by_key[key] = key
    segments = list(segments_by_key)
    critical_x = {p[0] for poly in [domain, *pieces] for p in poly}
    for i, (a, b) in enumerate(segments):
        aminx, amaxx = min_field(f, a[0], b[0]), max_field(f, a[0], b[0])
        aminy, amaxy = min_field(f, a[1], b[1]), max_field(f, a[1], b[1])
        for c, d in segments[i + 1:]:
            if (f.compare(amaxx, min_field(f, c[0], d[0])) < 0
                    or f.compare(max_field(f, c[0], d[0]), aminx) < 0
                    or f.compare(amaxy, min_field(f, c[1], d[1])) < 0
                    or f.compare(max_field(f, c[1], d[1]), aminy) < 0):
                continue
            x = _segment_intersection_x(f, a, b, c, d)
            if x is not None:
                critical_x.add(x)
    ordered_x = sorted(critical_x, key=cmp_to_key(lambda a, b: f.compare(a, b)))
    checked = 0
    for xleft, xright in zip(ordered_x, ordered_x[1:]):
        if f.compare(xleft, xright) == 0:
            continue
        x = div(f, add(f, xleft, xright), f.const(2))
        y_values = []
        for a, b in segments:
            lo, hi = min_field(f, a[0], b[0]), max_field(f, a[0], b[0])
            if f.compare(lo, x) < 0 and f.compare(x, hi) < 0:
                y_values.append(_y_at_x(f, a, b, x))
        y_values.sort(key=cmp_to_key(lambda a, b: f.compare(a, b)))
        unique_y = []
        for y in y_values:
            if not unique_y or f.compare(y, unique_y[-1]) != 0:
                unique_y.append(y)
        for ylo, yhi in zip(unique_y, unique_y[1:]):
            if f.compare(ylo, yhi) == 0:
                continue
            y = div(f, add(f, ylo, yhi), f.const(2))
            sample = (x, y)
            in_domain = _point_in_polygon(f, sample, domain)
            in_cover = any(_point_in_convex_piece(f, sample, poly) for poly in pieces)
            checked += 1
            if in_domain != in_cover:
                raise ValueError("convex pieces do not cover exactly the fixed polygon")
    if checked == 0:
        raise ValueError("arrangement produced no open cells to verify")
    return checked
