import os
import sys

import pytest

from tasks.t046.baseline import run_code as baseline_run
from tasks.t046.check import validate
from tasks.t046.human import run_code as human_run
from tasks.t046.init_program import run_code as seed_run
from tasks.t046.reference import run_code as reference_run
from tasks.t046.evolution import run_code as evolution_run


CONFIG = {
    "id": "T046-C01",
    "parameters": {
        "degree_at_most": 146,
        "interval": [0, 1],
        "coefficient_domain": "nonzero integer polynomials",
    },
    "direction": "minimize",
    "human_reference": 1.1210387714598537e-44,
}


def test_human_reference_and_monomial_seed_are_valid_distinct_constructions():
    human = human_run()
    reference = reference_run()
    seed = seed_run()
    result = validate(human, CONFIG, strict=True)
    assert human["coefficients"] == reference["coefficients"]
    assert seed["coefficients"] == [0] * 146 + [1]
    assert result["objective"] == "1/89202980794122492566142873090593446023921664"
    assert result["details"]["objective_interval"] == [result["objective"]] * 2
    assert result["details"]["degree"] == 146
    assert result["verification_status"] == "certified"
    assert validate(seed, CONFIG, strict=True)["objective"] == "1"


def test_known_polynomial_norms_are_certified_exactly():
    assert validate({"coefficients": [1]}, CONFIG, True)["objective"] == "1"
    assert validate({"coefficients": [0, 1, -1]}, CONFIG, True)["objective"] == "1/4"
    assert validate({"coefficients": [-1, 2]}, CONFIG, True)["objective"] == "1"


def test_trailing_zero_coefficients_do_not_change_the_polynomial():
    plain = validate({"coefficients": [0, 1, -1]}, CONFIG, True)
    padded = validate({"coefficients": [0, 1, -1, 0, 0]}, CONFIG, True)
    assert plain == padded


@pytest.mark.parametrize(
    "solution",
    [
        {},
        {"coefficients": []},
        {"coefficients": [0, 0]},
        {"coefficients": [True]},
        {"coefficients": [1.0]},
        {"coefficients": [float("nan")]},
        {"coefficients": [float("inf")]},
        {"coefficients": [0] * 148 + [1]},
        [1, 2, 3],
    ],
)
def test_invalid_polynomial_inputs_are_rejected(solution):
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)


def test_configuration_is_fixed():
    with pytest.raises(ValueError, match="degree_at_most=146"):
        validate({"coefficients": [1]}, {"parameters": {"degree_at_most": 100}})
    with pytest.raises(ValueError, match="degree_at_most=146"):
        validate({"coefficients": [1]}, {"parameters": {"degree_at_most": 146, "interval": [0, 1]}})


def test_forged_objective_fields_cannot_change_any_validation_result():
    solution = seed_run()
    baseline = validate(solution, CONFIG, strict=True)
    for key in ("objective", "score", "claimed_score"):
        forged = {**solution, key: "not-the-score"}
        assert validate(forged, CONFIG, strict=True) == baseline
    assert baseline["details"]["claimed_objective_ignored"] is True


def test_search_is_seeded_bounded_and_does_not_read_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "19")
    first = baseline_run()
    second = baseline_run()
    assert first == second
    assert evolution_run() == first
    meta = first["search_metadata"]
    assert meta["iteration_limit"] == 74
    assert meta["iterations"] == 74
    assert meta["reference_data_read"] is False
    assert validate(first, CONFIG, strict=True)["details"]["degree"] == 146


def test_zero_second_search_budget_returns_a_valid_construction(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    result = baseline_run()
    assert result["search_metadata"]["iterations"] == 0
    assert result["coefficients"] == [0] * 146 + [1]
    assert validate(result, CONFIG)["details"]["degree"] == 146


def test_runner_reports_program_errors_and_timeouts():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
