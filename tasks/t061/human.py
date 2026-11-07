"""Rebuild the 100-vertex, 133-edge C6-saturated construction in Theorem 1.5(a)."""

import os


CONFIG_ID = "T061-C01"


def build_human_graph():
    # Core graph H, decoded from Figure 1(a) of Lan et al. (2025).
    x1, x2, y1, y2, y3, y4, a0, b0, c0 = range(9)
    edges = {
        (x1, x2), (x1, y1), (x1, y2), (x1, a0),
        (x2, y3), (x2, y4), (x2, c0),
        (y2, y1), (y2, y3), (y2, y4),
        (a0, b0), (b0, c0),
    }
    # n=3t+1 with t=33: add t-3=30 paths and one leaf at y4.
    for i in range(1, 31):
        a, b, c = 9 + 3 * (i - 1), 10 + 3 * (i - 1), 11 + 3 * (i - 1)
        edges.update({(a, b), (b, c), (x1, a), (x2, c)})
    z1 = 99
    edges.add((y4, z1))
    canonical = [[min(u, v), max(u, v)] for u, v in edges]
    canonical.sort()
    return {"vertices": 100, "edges": canonical}


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", CONFIG_ID)
    if chosen != CONFIG_ID:
        raise ValueError(f"unsupported configuration: {chosen}")
    return build_human_graph()
