"""Exact checks for the fixed Gset G70 maximum-cut instance."""

import json
import hashlib
from pathlib import Path


_INSTANCE = json.loads((Path(__file__).parent / "data" / "instance.json").read_text())
_SOURCE_PATH = Path(__file__).parent / "data" / "source" / "G70"
_SOURCE_BYTES = _SOURCE_PATH.read_bytes()
_SOURCE_SHA256 = "0d965a2ff1444cc71d7740824b5b3a5e09fc1843cbf6d90691b52d5221987061"
_NORMALIZED_SHA256 = "76223a8eea98e77f0c1769f49c42a7d202fa5d62a47c872ed7b9d179d0f23085"
_NORMALIZED = json.dumps(
    {key: _INSTANCE[key] for key in ("instance_id", "n", "m", "edges")},
    separators=(",", ":"), ensure_ascii=True).encode()
if (_INSTANCE.get("source_sha256") != _SOURCE_SHA256
        or hashlib.sha256(_SOURCE_BYTES).hexdigest() != _SOURCE_SHA256
        or hashlib.sha256(_NORMALIZED).hexdigest() != _NORMALIZED_SHA256
        or _INSTANCE.get("normalized_graph_sha256") != _NORMALIZED_SHA256):
    raise RuntimeError("pinned Gset graph input hash mismatch")
_SOURCE_LINES = _SOURCE_BYTES.decode("ascii").splitlines()
_SOURCE_HEADER = [int(value) for value in _SOURCE_LINES[0].split()]
_SOURCE_EDGES = [[int(value) - 1 for value in line.split()[:2]] +
                 [int(line.split()[2])] for line in _SOURCE_LINES[1:]]
if (_SOURCE_HEADER != [_INSTANCE["n"], _INSTANCE["m"]]
        or len(_SOURCE_EDGES) != _INSTANCE["m"]
        or _SOURCE_EDGES != _INSTANCE["edges"]):
    raise RuntimeError("archived Stanford G70 does not match normalized graph")
_N = _INSTANCE["n"]
_EDGES = _INSTANCE["edges"]
_PARAMETERS = {
    "instance": _INSTANCE["instance_id"],
    "n": _N,
    "m": _INSTANCE["m"],
    "weights": "all +1",
    "graph_sha256": _INSTANCE["source_sha256"],
    "normalized_graph_sha256": _NORMALIZED_SHA256,
}


def validate(solution, config, strict=False):
    """Check a partition and recompute its integer cut exactly."""
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    parameters = config.get("parameters", config)
    if parameters != _PARAMETERS:
        raise ValueError("configuration does not match the pinned Gset graph")
    labels = solution.get("labels")
    if not isinstance(labels, list) or len(labels) != _N:
        raise ValueError(f"labels must contain exactly {_N} vertex sides")
    if any(type(side) is not int or side not in (0, 1) for side in labels):
        raise ValueError("each side must be integer 0 or 1; bool is not accepted")
    cut = sum(weight for u, v, weight in _EDGES if labels[u] != labels[v])
    return {
        "objective": cut,
        "verification_status": "exact",
        "details": {"n": _N, "m": len(_EDGES), "cut_edges": cut,
                    "graph_sha256": _INSTANCE["source_sha256"]},
    }
