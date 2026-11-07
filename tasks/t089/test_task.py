import json
import os
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from mathbench.evaluate import _run
from tasks.t089.baseline import run_code as baseline_run_code
from tasks.t089.check import _fourier_polynomial, _last_negative_root, validate
from tasks.t089.evolution import run_code as evolution_run_code
from tasks.t089.human import run_code as human_run_code
from tasks.t089.init_program import run_code as init_run_code
from tasks.t089.reference import run_code as reference_run_code


CONFIG = json.loads((Path(__file__).parent / "task.json").read_text())["configurations"][0]


def test_fourier_transform_is_exact_on_monomials_and_human_witness():
    assert _fourier_polynomial([Fraction(0), Fraction(1)]) == [Fraction(1, 2), Fraction(-1)]
    result = validate(human_run_code(), CONFIG)
    assert result["verification_status"] == "certified"
    assert result["details"]["fourier_coefficients_ascending"] == ["-1/1000", "-3/2", "1"]
    assert result["details"]["last_negative_to_positive_root_p"] == result["details"]["last_negative_to_positive_root_q"]
    assert abs(float(Fraction(result["objective_value"])) - 0.47767694163617652) < 1e-15
    assert result["details"]["claimed_score_ignored"] is True


def test_even_contact_is_not_mistaken_for_the_last_sign_change():
    # -(t-1)^2(t-3) stays negative on both sides of t=1, then crosses at 3.
    assert _last_negative_root([Fraction(-3), Fraction(7), Fraction(-5), Fraction(1)]) == (
        Fraction(3), Fraction(3)
    )


def test_simple_start_baseline_and_evolution_are_valid():
    for program in (init_run_code(), baseline_run_code(), evolution_run_code(), reference_run_code()):
        result = validate(program, CONFIG)
        assert result["verification_status"] == "certified"
        assert Fraction(result["objective_value"]) > 0


@pytest.mark.parametrize("coefficients", [
    ["1", "0", "1"],              # f(0) is not strictly negative
    ["-1", "4"],                  # Fourier transform is positive at zero
    ["-1", "0", "-1"],            # not eventually nonnegative
    [True, "-3/2", "1"],           # bool is not a rational coefficient
    [float("nan"), "-3/2", "1"],   # non-finite input
    [float("inf"), "-3/2", "1"],
    ["-1/0", "-3/2", "1"],        # malformed rational
    ["-1"],                         # constant negative polynomial
])
def test_invalid_coefficients_are_rejected(coefficients):
    with pytest.raises(ValueError):
        validate({"coefficients": coefficients, "claimed_score": -100}, CONFIG)


def test_claimed_objective_and_scores_do_not_change_recomputation():
    solution = reference_run_code()
    original = validate(solution, CONFIG)
    forged = dict(solution, objective=-1, score=float("nan"), claimed_score="0")
    assert validate(forged, CONFIG) == original


@pytest.mark.parametrize("config", [
    {**CONFIG, "id": "T089-C02"},
    {**CONFIG, "parameters": {**CONFIG["parameters"], "dimension": 2}},
    {**CONFIG, "parameters": {**CONFIG["parameters"], "dimension": True}},
    {**CONFIG, "direction": "maximize"},
])
def test_wrong_configuration_is_rejected(config):
    with pytest.raises(ValueError):
        validate(init_run_code(), config)


def test_runner_error_and_timeout_controls():
    env = dict(os.environ)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise SystemExit(9)"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
