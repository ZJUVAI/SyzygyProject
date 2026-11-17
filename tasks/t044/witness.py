"""Read a 70-vertex graph from a published adjacency list."""


def load_upper_triangle(path):
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
