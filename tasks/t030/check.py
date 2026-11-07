"""Exact verifier for the fixed DIMACS DSJC1000.5 graph coloring task."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


_TASK_DIR = Path(__file__).parent
_INPUT_PATH = _TASK_DIR / "data" / "instance.json"
_INPUT_SHA256 = "51550de59559742f72c2da8e3963edab39124cd8f334eb63cae10d9bb3f132bd"
_VERTICES = 1000
_EDGES = 249826


def load_graph():
    """Load and verify the task input. It contains only the graph instance."""
    raw = _INPUT_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != _INPUT_SHA256:
        raise RuntimeError("trusted DSJC1000.5 input hash does not match the frozen snapshot")
    payload = json.loads(raw)
    if not isinstance(payload, dict) or payload.get("instance") != "DSJC1000.5":
        raise RuntimeError("trusted input is not DSJC1000.5")
    if payload.get("vertices") != _VERTICES:
        raise RuntimeError("trusted graph has the wrong vertex count")
    edges = payload.get("edges")
    if not isinstance(edges, list) or len(edges) != _EDGES:
        raise RuntimeError("trusted graph has the wrong edge count")
    adjacency = [set() for _ in range(_VERTICES)]
    seen = set()
    for edge in edges:
        if (not isinstance(edge, list) or len(edge) != 2
                or any(type(v) is not int for v in edge)):
            raise RuntimeError("trusted graph contains a malformed edge")
        u, v = edge
        if not (0 <= u < _VERTICES and 0 <= v < _VERTICES) or u == v:
            raise RuntimeError("trusted graph contains an invalid endpoint")
        key = (u, v) if u < v else (v, u)
        if key in seen:
            raise RuntimeError("trusted graph contains a duplicate edge")
        seen.add(key)
        adjacency[u].add(v)
        adjacency[v].add(u)
    return tuple(frozenset(neighbors) for neighbors in adjacency), tuple(edges)


def validate(solution, config, strict=False):
    """Check all edges and recompute the exact number of distinct colors."""
    del strict  # Feasibility and the objective use exact integer operations.
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    if config.get("id", "T030-C01") != "T030-C01":
        raise ValueError("configuration id must be T030-C01")
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
