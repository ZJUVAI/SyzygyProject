"""Exact verifier for the fixed DIMACS DSJC1000.5 graph coloring task."""

from __future__ import annotations

from pathlib import Path

from mathbench.graph_bits import load_adjacency


_TASK_DIR = Path(__file__).parent
_INPUT_PATH = _TASK_DIR / "data" / "DSJC1000.5.bits"
_INPUT_SHA256 = "ec284de01b9716dc1db3fd0f851122b61ae263623c5ba2a8c7a5f48986894779"
_VERTICES = 1000
_EDGES = 249826


def load_graph():
    """Load the verified packed graph and expose the task's set-based API."""
    masks = load_adjacency(_INPUT_PATH, _VERTICES, _EDGES, _INPUT_SHA256)
    adjacency = tuple(
        frozenset(v for v in range(_VERTICES) if mask & (1 << v))
        for mask in masks
    )
    edges = tuple(
        (u, v)
        for u, mask in enumerate(masks)
        for v in range(u + 1, _VERTICES)
        if mask & (1 << v)
    )
    return adjacency, edges


def validate(solution, config, strict=False):
    """Check all edges and recompute the exact number of distinct colors."""
    del strict  # Feasibility and the objective use exact integer operations.
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    if config.get("id", "T038-C01") != "T038-C01":
        raise ValueError("configuration id must be T038-C01")
    params = config.get("parameters", config)
    expected = {
        "instance": "DSJC1000.5",
        "vertices": _VERTICES,
        "edges": _EDGES,
        "input_sha256": _INPUT_SHA256,
    }
    if not isinstance(params, dict) or any(params.get(k) != v for k, v in expected.items()):
        raise ValueError("configuration must fix the trusted DSJC1000.5 graph")
    colors = solution.get("colors")
    if not isinstance(colors, list) or len(colors) != _VERTICES:
        raise ValueError("colors must be a list with one entry for each of 1000 vertices")
    if any(type(color) is not int for color in colors):
        raise ValueError("color labels must be integers, not bool or numeric values")
    _, edges = load_graph()
    for edge_index, (u, v) in enumerate(edges):
        if colors[u] == colors[v]:
            raise ValueError(f"edge {edge_index} ({u}, {v}) has equal endpoint colors")
    objective = len(set(colors))
    return {
        "objective": objective,
        "verification_status": "exact",
        "details": {
            "instance": "DSJC1000.5",
            "vertices": _VERTICES,
            "edges_checked": _EDGES,
            "distinct_colors_recomputed": objective,
            "claimed_objective_ignored": True,
            "claimed_score_ignored": True,
            "input_sha256": _INPUT_SHA256,
        },
    }
