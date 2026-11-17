"""Exact checks for the fixed Q9 induced-path task."""

import hashlib
import os
from pathlib import Path
import sys

import pytest

from tasks.t041.check import PARAMETERS, validate

ROOT = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def _replay(transitions):
    vertices = [0]
    for coordinate in transitions:
        vertices.append(vertices[-1] ^ (1 << coordinate))
    return vertices


def test_fixed_reference_and_human_witnesses_are_exact():
    from tasks.t041.human import run_code as human_run
    from tasks.t041.reference import run_code as reference_run

    human = human_run()
    reference = reference_run()
    assert validate(human, CONFIG, strict=True)["objective"] == 190
    assert validate(reference, CONFIG, strict=True)["objective"] == 191
    for name, expected in (("wynn_q9_190.json", "3f74e9ce45736179738ae16fb447e4c5ea7cb594ea776b930fa5c7acbac00882"),
                           ("orland_v3_q9_191.json", "fff784d8d79ec56682765735ad3263d9978338279ea1854f43438ea9bd37b7a4")):
        path = ROOT / "data/reference" / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        import json
        witness = json.loads(path.read_text())
        assert witness["vertices"] == _replay(witness["transitions"])
        assert witness["length_edges"] == len(witness["transitions"])


def test_exact_score_independent_recalculation_and_claimed_score_ignored():
    from tasks.t041.reference import run_code

    solution = run_code()
    vertices = solution["vertices"]
    independently_counted_edges = sum((u ^ v).bit_count() == 1 for u, v in zip(vertices, vertices[1:]))
    assert independently_counted_edges == 191
    for i, u in enumerate(vertices):
        for j in range(i + 2, len(vertices)):
            assert (u ^ vertices[j]).bit_count() != 1
    checked = validate(solution, CONFIG, strict=True)
    assert checked["objective"] == independently_counted_edges
    assert validate({**solution, "objective": -1}, CONFIG) == checked
    assert validate({**solution, "score": float("nan")}, CONFIG) == checked
    assert validate({**solution, "claimed_score": {"forged": True}}, CONFIG) == checked


def test_checker_rejects_bad_vertices_and_chords():
    from tasks.t041.init_program import run_code

    valid = run_code()
    assert validate(valid, CONFIG)["objective"] == 9
    with pytest.raises(ValueError, match="at least one edge"):
        validate({"vertices": [0]}, CONFIG)
    with pytest.raises(ValueError, match="range"):
        validate({"vertices": [-1, 0]}, CONFIG)
    with pytest.raises(ValueError, match="range"):
        validate({"vertices": [0, 512]}, CONFIG)
    with pytest.raises(ValueError, match="bool"):
        validate({"vertices": [False, 1]}, CONFIG)
    with pytest.raises(ValueError, match="integers"):
        validate({"vertices": [0, 1.0]}, CONFIG)
    with pytest.raises(ValueError, match="integers"):
        validate({"vertices": [0, float("nan")]}, CONFIG)
    with pytest.raises(ValueError, match="distinct"):
        validate({"vertices": [0, 1, 0]}, CONFIG)
    with pytest.raises(ValueError, match="not adjacent"):
        validate({"vertices": [0, 3]}, CONFIG)
    with pytest.raises(ValueError, match="nonconsecutive"):
        validate({"vertices": [0, 1, 3, 2]}, CONFIG)
    with pytest.raises(ValueError, match="unsupported"):
        validate(valid, {"parameters": {**PARAMETERS, "dimension": 8}})


def test_all_five_program_entries_return_valid_paths(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T041-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "2")
    from tasks.t041.init_program import run_code as init_run
    from tasks.t041.baseline import run_code as baseline_run
    from tasks.t041.human import run_code as human_run
    from tasks.t041.reference import run_code as reference_run
    from tasks.t041.evolution import run_code as evolution_run

    results = []
    for run in (init_run, baseline_run, human_run, reference_run, evolution_run):
        result = run()
        assert validate(result, CONFIG, strict=True)["verification_status"] == "exact"
        results.append(result)
    assert len(results[3]["vertices"]) == 192
    assert len(results[2]["vertices"]) == 191


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T041 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T041 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
