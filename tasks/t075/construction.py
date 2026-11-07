"""Recursive H6 construction used to rebuild the traditional witness."""
import json
from pathlib import Path


TEMPLATE_PATH = Path(__file__).parent / "data/source/h6_template.json"


def load_h6():
    data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    if data.get("vertices") != 6:
        raise ValueError("unexpected H6 template")
    edges = [tuple(e) for e in data["edges_zero_based"]]
    if len(edges) != 10 or len(set(edges)) != 10:
        raise ValueError("unexpected H6 edge list")
    return edges


def build_iterated_h6(parts=6):
    """Build one H6 blow-up with an H6 copy inside every part."""
    if parts != 6:
        raise ValueError("T075 uses six parts of size six")
    h6 = load_h6()
    block_size = 6
    edges = set()
    # Outer blow-up: every template edge induces a complete tripartite triple set.
    for a, b, c in h6:
        for x in range(a * block_size, (a + 1) * block_size):
            for y in range(b * block_size, (b + 1) * block_size):
                for z in range(c * block_size, (c + 1) * block_size):
                    edges.add((x, y, z))
    # Repeat the same construction recursively inside each of the six parts.
    for part in range(6):
        offset = part * block_size
        for a, b, c in h6:
            edges.add((offset + a, offset + b, offset + c))
    if len(edges) != 2220:
        raise AssertionError("unexpected two-level H6 blow-up edge count")
    return {"edges": [list(e) for e in sorted(edges)]}
