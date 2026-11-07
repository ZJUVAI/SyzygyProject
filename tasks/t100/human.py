"""Rebuild the published LPS H* construction for (n,e)=(50,700)."""

import os


def build_human_graph():
    # H* has parts A=(23), B=(23), C=(4), all cross-edges, except
    # 13 edges from c_0 to distinct vertices of B are deleted.
    part_a = range(0, 23)
    part_b = range(23, 46)
    part_c = range(46, 50)
    edges = []
    for left in part_a:
        for right in part_b:
            edges.append([left, right])
        for right in part_c:
            edges.append([left, right])
    for left in part_b:
        for right in part_c:
            if not (right == 46 and left < 36):
                edges.append([left, right])
    return {"vertices": 50, "edges": edges}


def run_code():
    if os.environ.get("MATHBENCH_CONFIG_ID", "T100-C01") != "T100-C01":
        raise ValueError("unsupported T100 configuration")
    return build_human_graph()
