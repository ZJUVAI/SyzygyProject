"""Exact task-local checks for partial MaxSAT configuration T055-C01."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t055.check import PARAMETERS, validate
from tasks.t055.maxsat import HARD, NVAR, SOFT, INSTANCE_SHA256, instance_path, score_assignment

ROOT = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def test_pinned_instance_and_public_assignment_are_exact():
    from tasks.t055.reference import run_code

    assert hashlib.sha256(instance_path().read_bytes()).hexdigest() == INSTANCE_SHA256
    assert len(HARD) == 6150
    assert len(SOFT) == 649
    assert all(weight == 1 and len(clause) == 1 for weight, clause in SOFT)
    solution = run_code()
    checked = validate(solution, CONFIG, strict=True)
    assert len(solution["assignment"]) == NVAR == 1630
    assert checked["objective"] == 587
    assert checked["details"]["hard_clauses_satisfied"] == 6150
    assert checked["details"]["soft_unsatisfied_weight"] == 62
    path = ROOT / "data/reference/mse2026_boums_60_assignment.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "c129d0fded17b46dca93fe9a4c3c2273926c346c78578bfec2e922023a746543"


def test_human_dpll_baseline_is_independent_and_exact():
    from tasks.t055.human import run_code

    solution = run_code()
    result = validate(solution, CONFIG, strict=True)
    assert result["objective"] == 360
    assert result["details"]["hard_clauses_satisfied"] == 6150
    assert score_assignment(solution["assignment"], HARD, SOFT)["soft_cost"] == 289
    path = ROOT / "data/reference/human_dpll_assignment.json"
    saved = json.loads(path.read_text())
    assert saved["assignment"] == [int(value) for value in solution["assignment"]]


def test_independent_recount_and_declared_scores_are_ignored():
    from tasks.t055.reference import run_code

    solution = run_code()
    assignment = solution["assignment"]
    hard_satisfied = sum(
        any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
        for clause in HARD
    )
    soft_satisfied_weight = sum(
        weight for weight, clause in SOFT
        if any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
    )
    assert hard_satisfied == 6150
    assert soft_satisfied_weight == 587
    checked = validate(solution, CONFIG, strict=True)
    assert checked["objective"] == soft_satisfied_weight
    assert validate({**solution, "objective": -5}, CONFIG) == checked
    assert validate({**solution, "score": float("nan")}, CONFIG) == checked
    assert validate({**solution, "claimed_score": {"false": True}}, CONFIG) == checked


def test_checker_rejects_malformed_and_hard_violating_assignments():
    from tasks.t055.init_program import run_code

    valid = run_code()
    assert validate(valid, CONFIG)["objective"] == 360
    with pytest.raises(ValueError, match="exactly 1630"):
        validate({"assignment": valid["assignment"][:-1]}, CONFIG)
    with pytest.raises(ValueError, match="booleans"):
        validate({"assignment": [0] * NVAR}, CONFIG)
    with pytest.raises(ValueError, match="booleans"):
        validate({"assignment": [False] * (NVAR - 1) + [float("nan")]}, CONFIG)
    with pytest.raises(ValueError, match="violates"):
        validate({"assignment": [False] * NVAR}, CONFIG)
    with pytest.raises(ValueError, match="unsupported"):
        validate(valid, {"parameters": {**PARAMETERS, "variables": 1629}})


def test_all_five_program_entries_and_runner_controls(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T055-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "1")
    from tasks.t055.init_program import run_code as init_run
    from tasks.t055.baseline import run_code as baseline_run
    from tasks.t055.human import run_code as human_run
    from tasks.t055.reference import run_code as reference_run
    from tasks.t055.evolution import run_code as evolution_run

    for run in (init_run, baseline_run, human_run, reference_run, evolution_run):
        result = run()
        assert validate(result, CONFIG, strict=True)["verification_status"] == "exact"

    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T055 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T055 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
