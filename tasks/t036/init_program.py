"""Simple standalone 700-edge seed for T036."""

import os
from itertools import combinations


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T036-C01") != "T036-C01":
        raise ValueError("unsupported T036 configuration")
    edges = []
    for edge in combinations(range(50), 2):
        edges.append(list(edge))
        if len(edges) == 700:
            break
    return {"vertices": 50, "edges": edges}
