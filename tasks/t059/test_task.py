"""Exact graph integrity, clique, entry-point, and worker-control tests."""

import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t059.check import PARAMETERS, validate
from tasks.t059.graph import N, RAW_SHA256, load_graph

HERE = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def _human():
    return json.loads((HERE / "data/reference/human_2005_clique80.json").read_text())


def test_human_clique_and_independent_edge_set_verification():
    vertices = _human()["vertices"]
    checked = validate({"vertices": vertices}, CONFIG)
    assert checked["objective"] == 80
    assert checked["verification_status"] == "exact"

    # Independent parser and edge-set representation, distinct from graph.py's bitsets.
    edges = set()
    raw_digest = hashlib.sha256()
    raw_bytes = 0
    with gzip.open(HERE / "data/source/C2000.9.clq.gz", "rb") as stream:
        for raw in stream:
            raw_digest.update(raw)
            raw_bytes += len(raw)
            fields = raw.split()
            if fields and fields[0] == b"e":
                u, v = int(fields[1]) - 1, int(fields[2]) - 1
                edges.add((min(u, v), max(u, v)))
    assert raw_digest.hexdigest() == RAW_SHA256
    assert raw_bytes == 19602828
    assert len(edges) == 1799532
    assert all((min(u, v), max(u, v)) in edges
               for i, u in enumerate(vertices) for v in vertices[i + 1:])


def test_empty_and_single_vertex_boundary_cliques():
    assert validate({"vertices": []}, CONFIG)["objective"] == 0
    assert validate({"vertices": [1999]}, CONFIG)["objective"] == 1


def test_compressed_source_hash_and_graph_shape():
    assert hashlib.sha256((HERE / "data/source/C2000.9.clq.gz").read_bytes()).hexdigest() == (
        "936ec5806f6e58fbe1f28a87f018cd064dece5eae8ab29013040d47857fd1639"
    )
    assert len(load_graph()) == N == 2000
    assert all(row.bit_count() > 0 for row in load_graph())


@pytest.mark.parametrize("bad", [
    None,
    {},
    {"vertices": None},
    {"vertices": ()},
    {"vertices": [True]},
    {"vertices": [1.0]},
    {"vertices": [float("nan")]},
    {"vertices": [float("inf")]},
    {"vertices": [-1]},
    {"vertices": [2000]},
    {"vertices": [3, 3]},
])
def test_invalid_candidate_types_ranges_and_duplicates_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


def test_nonedge_is_rejected_and_claims_are_ignored():
    adjacency = load_graph()
    nonneighbor = next(v for v in range(N) if v != 0 and not ((adjacency[0] >> v) & 1))
    with pytest.raises(ValueError, match="not adjacent"):
        validate({"vertices": [0, nonneighbor]}, CONFIG)

    vertices = _human()["vertices"]
    base = validate({"vertices": vertices}, CONFIG)
    for name, forged in [("objective", 10000), ("score", float("nan")),
                         ("claimed_score", {"value": float("inf")})]:
        candidate = {"vertices": vertices, name: forged}
        assert validate(candidate, CONFIG) == base
    with pytest.raises(ValueError):
        validate({"vertices": vertices}, {"parameters": {"instance": "C1000.9", "vertices": 1000, "edges": 450079}})


@pytest.mark.parametrize("module,expected", [
    ("tasks.t059.init_program", 1),
    ("tasks.t059.baseline", None),
    ("tasks.t059.human", 80),
    ("tasks.t059.reference", 80),
    ("tasks.t059.evolution", None),
])
def test_all_five_run_code_entries(module, expected, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T059-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "1")
    result = importlib.import_module(module).run_code()
    value = validate(result, CONFIG)["objective"]
    if expected is not None:
        assert value == expected
    assert type(value) is int
    if module.endswith(("baseline", "evolution")):
        assert result["search_metadata"]["budget"]["mode"] == (
            "fixed iterations; runner generation timeout 300 seconds"
        )


def test_search_does_not_read_human_or_reference_assets_and_seed_is_standalone():
    for filename in ("baseline.py", "evolution.py"):
        source = (HERE / filename).read_text()
        assert "tasks.t059.human" not in source
        assert "tasks.t059.reference" not in source
        assert "data/reference" not in source
    init_source = (HERE / "init_program.py").read_text()
    assert "# EVOLVE-BLOCK-START" in init_source
    assert "# EVOLVE-BLOCK-END" in init_source
    assert "tasks.t059" not in init_source


def test_worker_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise SystemExit('intentional worker error')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.15)
