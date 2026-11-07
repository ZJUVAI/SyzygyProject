"""Cold-start exact triangulation for the public T097 polygon."""
import json
import os
from pathlib import Path


# EVOLVE-BLOCK-START
def run_code():
    config_id = os.environ.get("MATHBENCH_CONFIG_ID", "T097-C01")
    if config_id != "T097-C01":
        raise ValueError(f"unsupported configuration: {config_id}")
    source = Path(__file__).parent / "data/source/socg_fixed92.instance.json"
    boundary = [(p["x"], p["y"]) for p in json.loads(source.read_text())["outer_boundary"]]

    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    vertices = list(boundary)
    if sum(a[0] * b[1] - a[1] * b[0]
           for a, b in zip(vertices, vertices[1:] + vertices[:1])) < 0:
        vertices.reverse()
    triangles = []
    while len(vertices) > 3:
        n = len(vertices)
        for i in range(n):
            a, b, c = vertices[i - 1], vertices[i], vertices[(i + 1) % n]
            if cross(a, b, c) <= 0:
                continue

            def in_triangle(p):
                return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0

            if any(in_triangle(p) for j, p in enumerate(vertices)
                   if j not in {(i - 1) % n, i, (i + 1) % n}):
                continue
            triangles.append([a, b, c])
            del vertices[i]
            break
        else:
            raise ValueError("ear clipping failed for the fixed simple polygon")
    triangles.append(vertices)
    return {
        "algebraic_field": {"minimal_polynomial": ["0", "1"], "isolating_interval": ["-1", "1"]},
        "polygons": [[[[str(x)], [str(y)]] for x, y in triangle] for triangle in triangles],
        "search_metadata": {"construction": "exact ear clipping", "initial_triangle_count": len(triangles)},
    }
# EVOLVE-BLOCK-END
