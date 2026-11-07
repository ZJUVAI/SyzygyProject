"""Replay the published 70-vertex Alegre-Fiol-Yebra graph witness."""

from pathlib import Path


def _load_upper_triangle(path):
    edges = set()
    for raw_line in path.read_text(encoding="ascii").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        values = [int(value) for value in line.split()]
        source, neighbors = values[0], values[1:]
        for target in neighbors:
            edges.add((min(source, target), max(source, target)))
    return {"n": 70, "edges": [list(edge) for edge in sorted(edges)]}


def run_code():
    path = Path(__file__).parent / "data" / "reference" / "afy_70_adjlist_nx.txt"
    return _load_upper_triangle(path)
