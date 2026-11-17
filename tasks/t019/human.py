"""Rebuild the 32-point Erdős–Szekeres construction from the published recursion."""

from functools import lru_cache


def build_points():
    @lru_cache(None)
    def s_kl(k, ell):
        if k <= 2 or ell <= 2:
            return ((0, 0),)
        r = k + ell - 1
        # This is the integer realization P_r specified in §2 of the source.
        dx = 3 * 4 ** (r - 1)
        dy = (3 * r + 1) * 4 ** (r - 1)
        left = s_kl(k - 1, ell)
        right = tuple((x + dx, y + dy) for x, y in s_kl(k, ell - 1))
        return left + right

    t = 7
    scale = (t + 1) * 4 ** (t + 1)
    points = []
    wx = wy = 0
    for i in range(t - 1):
        layer = s_kl(t - i, i + 2)
        points.extend((wx * scale + x, wy * scale + y) for x, y in layer)
        if i < t - 2:
            wx += 3 * (t - i)
            wy -= 3 * i
    return {"points": points, "claimed_objective": 32}


def run_code():
    """Expose the reconstructed human construction through the task contract."""
    return build_points()


if __name__ == "__main__":
    import json
    print(json.dumps(run_code(), separators=(",", ":")))
