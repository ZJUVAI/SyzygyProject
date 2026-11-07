"""Frozen public arc130 graph input and exact integer cutwidth helpers."""

from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
SOURCE_PATH = TASK_DIR / "data" / "source" / "arc130.mtx.rnd"
VERTEX_COUNT = 130
EDGE_COUNT = 715


def load_graph():
    lines = SOURCE_PATH.read_text(encoding="utf-8").splitlines()
    if len(lines) != EDGE_COUNT + 2 or lines[1].split() != ["130", "130", "715"]:
        raise ValueError("frozen arc130 input has an unexpected header or line count")
    edges = []
    seen = set()
    for line_number, line in enumerate(lines[2:], start=3):
        fields = line.split()
        if len(fields) != 2:
            raise ValueError(f"invalid source edge on line {line_number}")
        left, right = map(int, fields)
        if not (1 <= left <= VERTEX_COUNT and 1 <= right <= VERTEX_COUNT) or left == right:
            raise ValueError(f"invalid source endpoint on line {line_number}")
        edge = tuple(sorted((left, right)))
        if edge in seen:
            raise ValueError(f"duplicate source edge on line {line_number}")
        seen.add(edge)
        edges.append(edge)
    return tuple(edges)


def cut_profile(ordering, edges=None):
    """Return all n-1 prefix cut sizes by exact difference-array arithmetic."""
    if edges is None:
        edges = load_graph()
    position = [0] * (VERTEX_COUNT + 1)
    for index, vertex in enumerate(ordering):
        position[vertex] = index
    difference = [0] * VERTEX_COUNT
    for left, right in edges:
        lo, hi = sorted((position[left], position[right]))
        difference[lo] += 1
        difference[hi] -= 1
    profile = []
    crossing = 0
    for cut in range(VERTEX_COUNT - 1):
        crossing += difference[cut]
        profile.append(crossing)
    return profile


def cutwidth(ordering, edges=None):
    return max(cut_profile(ordering, edges))
