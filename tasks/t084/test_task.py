import os
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t084.baseline import run_code as baseline_run_code
from tasks.t084.check import validate
from tasks.t084.evolution import run_code as evolution_run_code
from tasks.t084.human import run_code as human_run_code
from tasks.t084.init_program import run_code as init_run_code
from tasks.t084.reference import run_code as reference_run_code


CONFIG = {"id": "T084-C01", "parameters": {"cardinality": 31, "order": 3, "integer_domain": True},
          "direction": "minimize", "human_reference": 19407}


def test_public_human_and_reference_are_exactly_reproduced():
    expected = {
        "objective": 19407,
        "verification_status": "exact",
        "details": {"cardinality": 31, "order": 3, "triple_sums_checked": 5456,
                    "claimed_objective_ignored": True},
    }
    assert validate(human_run_code(), CONFIG) == expected
    assert validate(reference_run_code(), CONFIG) == expected


def test_initial_program_is_valid():
    result = validate(init_run_code(), CONFIG)
    assert result["verification_status"] == "exact"
    assert result["details"]["triple_sums_checked"] == 5456
    assert result["objective"] == 4 ** 29


def test_greedy_baseline_is_valid_without_comparison_data():
    result = validate(baseline_run_code(), CONFIG)
    assert result["verification_status"] == "exact"
    assert result["details"]["triple_sums_checked"] == 5456


def test_evolution_entry_runs_and_returns_a_valid_set(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "12")
    result = validate(evolution_run_code(), CONFIG)
    assert result["verification_status"] == "exact"
    assert result["details"]["triple_sums_checked"] == 5456


@pytest.mark.parametrize("elements", [
    [0] * 31,
    [False] + list(range(1, 31)),
    [0.0] + list(range(1, 31)),
    [float("nan")] + list(range(1, 31)),
    [float("inf")] + list(range(1, 31)),
    ["+1"] + list(range(1, 31)),
    ["01"] + list(range(1, 31)),
    list(range(30)),
    list(range(31)),
])
def test_duplicate_noninteger_and_invalid_triple_sums_are_rejected(elements):
    with pytest.raises(ValueError):
        validate({"elements": elements, "objective": -999, "score": 999}, CONFIG)


def test_arbitrary_size_integer_strings_and_translation():
    offset = 10 ** 5000
    translated = [str(offset + value) for value in human_run_code()["elements"]]
    assert validate({"elements": translated}, CONFIG)["objective"] == 19407


def test_claimed_scores_do_not_change_any_validation_field():
    solution = human_run_code()
    original = validate(solution, CONFIG)
    forged = dict(solution, objective=-1, score=0, claimed_score=float("nan"))
    assert validate(forged, CONFIG) == original


def test_decimal_strings_are_canonical_and_exact():
    witness = human_run_code()["elements"]
    as_strings = [str(value) for value in witness]
    assert validate(as_strings, CONFIG)["objective"] == 19407
    with pytest.raises(ValueError):
        validate(["-0"] + witness[1:], CONFIG)
    with pytest.raises(ValueError):
        validate(["1.0"] + witness[1:], CONFIG)


@pytest.mark.parametrize("parameters", [
    {"cardinality": 31, "order": 3, "integer_domain": False},
    {"cardinality": 31, "order": 3, "integer_domain": True, "extra": 1},
    {"cardinality": True, "order": 3, "integer_domain": True},
    {"cardinality": 31, "order": False, "integer_domain": True},
    {"cardinality": 30, "order": 3, "integer_domain": True},
])
def test_invalid_configuration_rejected(parameters):
    with pytest.raises(ValueError):
        validate(human_run_code(), {"id": "T084-C01", "parameters": parameters})


def test_invalid_configuration_id_rejected():
    with pytest.raises(ValueError):
        validate(human_run_code(), {"id": "T084-C02", "parameters": CONFIG["parameters"]})


def test_runner_error_and_timeout_controls():
    env = dict(os.environ)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise SystemExit(7)"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
