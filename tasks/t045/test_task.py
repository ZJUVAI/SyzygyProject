"""Exact checks for the fixed gd96a minimum linear arrangement task."""

import hashlib
import os
from pathlib import Path
import sys

import pytest

from tasks.t045.check import PARAMETERS, validate
from tasks.t045.graph import EDGE_COUNT, VERTICES, load_graph

ROOT = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def test_graph_source_and_configuration_are_exact():
    n, edges = load_graph()
    assert (n, len(edges)) == (1096, 1676)
    assert len(set(edges)) == EDGE_COUNT
    graph_file = ROOT / "data/source/gd96a.rmf"
    assert hashlib.sha256(graph_file.read_bytes()).hexdigest() == (
        "a3f6f97b8c084f41b6312a02544d71b293bfb8e809f627e4c5e7a04495061f4c")


def test_checker_rejects_broken_permutations_and_ignores_claims():
    from tasks.t045.reference import run_code

    valid = run_code()
    checked = validate(valid, CONFIG, strict=True)
    assert checked["objective"] == 147653
    ordering = valid["ordering"]
    position = [0] * (VERTICES + 1)
    for rank, vertex in enumerate(ordering, start=1):
        position[vertex] = rank
    _, edges = load_graph()
    independently_recomputed = sum(abs(position[u + 1] - position[v + 1]) for u, v in edges)
    assert independently_recomputed == 147653
    with pytest.raises(ValueError, match="exactly once"):
        validate({"ordering": ordering[:-1]}, CONFIG)
    with pytest.raises(ValueError, match="exactly once"):
        validate({"ordering": []}, CONFIG)
    duplicate = ordering[:]
    duplicate[0] = duplicate[1]
    with pytest.raises(ValueError, match="permutation"):
        validate({"ordering": duplicate}, CONFIG)
    with pytest.raises(ValueError, match="bool"):
        validate({"ordering": [True] + ordering[1:]}, CONFIG)
    with pytest.raises(ValueError, match="integers"):
        validate({"ordering": [float("nan")] + ordering[1:]}, CONFIG)
    out_of_range = ordering[:]
    out_of_range[0] = 0
    with pytest.raises(ValueError, match="range"):
        validate({"ordering": out_of_range}, CONFIG)
    assert validate({**valid, "objective": -1}, CONFIG) == checked
    assert validate({**valid, "score": float("nan")}, CONFIG) == checked
    assert validate({**valid, "claimed_score": {"forged": True}}, CONFIG) == checked


def test_all_five_program_entries_are_valid_and_seeded(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T045-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "1")
    monkeypatch.setenv("MATHBENCH_ADJACENT_SWEEPS", "2")
    from tasks.t045.init_program import run_code as init_run
    from tasks.t045.baseline import run_code as baseline_run
    from tasks.t045.human import run_code as human_run
    from tasks.t045.reference import run_code as reference_run
    from tasks.t045.evolution import run_code as evolution_run

    results = {}
    for name, run in (("init", init_run), ("baseline", baseline_run), ("human", human_run),
                      ("reference", reference_run), ("evolution", evolution_run)):
        result = run()
        results[name] = result
        assert validate(result, CONFIG)["verification_status"] == "exact"
    assert results["human"]["ordering"] == results["reference"]["ordering"]


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T045 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T045 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
