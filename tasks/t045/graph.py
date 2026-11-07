"""Pinned gd96a input loader with exact structural checks."""

from pathlib import Path

GRAPH_PATH = Path(__file__).resolve().parent / "data" / "source" / "gd96a.rmf"
VERTICES = 1096
EDGE_COUNT = 1676


def load_graph():
    lines = GRAPH_PATH.read_text(encoding="ascii").splitlines()
    if not lines:
        raise ValueError("graph source is empty")
    header = lines[0].split()
    if header != ["p", "ghct", str(VERTICES), str(EDGE_COUNT)]:
        raise ValueError("gd96a header does not match the pinned configuration")
    edges = []
    seen = set()
    for line_no, line in enumerate(lines[1:], start=2):
        parts = line.split()
        if len(parts) != 4 or parts[0] != "e":
            raise ValueError(f"malformed graph edge at line {line_no}")
        u, v, weight = map(int, parts[1:])
        if not (1 <= u <= VERTICES and 1 <= v <= VERTICES) or u == v or weight != 1:
            raise ValueError(f"invalid unweighted edge at line {line_no}")
        edge = (min(u - 1, v - 1), max(u - 1, v - 1))
        if edge in seen:
            raise ValueError(f"duplicate undirected edge at line {line_no}")
        seen.add(edge)
        edges.append(edge)
    if len(edges) != EDGE_COUNT:
        raise ValueError("graph edge count does not match the pinned configuration")
    return VERTICES, tuple(edges)
