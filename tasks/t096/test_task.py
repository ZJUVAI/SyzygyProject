import json
import os
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from mathbench.evaluate import _run
from tasks.t096.baseline import run_code as baseline_run
from tasks.t096.check import CONFIG_ID, _EXPECTED, validate
from tasks.t096.evolution import run_code as evolution_run
from tasks.t096.human import run_code as human_run
from tasks.t096.init_program import run_code as init_run
from tasks.t096.reference import run_code as reference_run

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / "task.json").read_text())["configurations"][0]


def test_five_entries_and_exact_circle_baseline():
    for run in (init_run, baseline_run, evolution_run, human_run, reference_run):
        value = validate(run(), CONFIG)
        assert value["verification_status"] == "certified"
        assert Fraction(value["objective"]) > 0
    assert validate(human_run(), CONFIG)["objective"] == "1/1"
    assert validate(reference_run(), CONFIG)["objective"] == "1/1"


def test_nonconstant_radius_rayleigh_interval_matches_independent_exact_formula():
    # rho=1+(1/2)cos(2theta), f=1 has Q=2/sqrt(3).
    witness = {
        "rho": {"constant": "1", "cos": ["0", "1/2"], "sin": ["0", "0"]},
        "trial": {"constant": "1", "cos": [], "sin": []},
        "rho_lower_bound": "1/2",
        "series_terms": 52,
    }
    result = validate(witness, CONFIG)
    lo, hi = map(Fraction, result["details"]["objective_interval"])
    # Squaring these rational inequalities certifies lo <= 2/sqrt(3) <= hi.
    assert 3 * lo * lo <= 4
    assert 3 * hi * hi >= 4
    assert result["objective"] == result["details"]["rayleigh_quotient_upper_bound"]
    assert "not a two-sided interval for the first eigenvalue" in result["details"]["objective_interval_meaning"]


def test_sine_coefficients_are_supported_for_curve_and_trial():
    witness = {
        "rho": {"constant": "1", "cos": ["0", "1/2"], "sin": ["0", "1/4"]},
        "trial": {"constant": "1", "cos": ["0"], "sin": ["1/8"]},
        "rho_lower_bound": "2/5",
        "series_terms": 18,
    }
    result = validate(witness, CONFIG)
    assert result["verification_status"] == "certified"
    assert Fraction(result["details"]["objective_interval"][0]) <= Fraction(result["objective"])


def test_false_lower_bound_with_negative_leading_polynomial_is_rejected():
    witness = {
        "rho": {"constant": "1", "cos": ["0", "1/2"], "sin": ["0", "0"]},
        "trial": {"constant": "1", "cos": [], "sin": []},
        "rho_lower_bound": "3/2",
        "series_terms": 8,
    }
    with pytest.raises(ValueError, match="lower bound"):
        validate(witness, CONFIG)


def test_bad_closure_nonpositive_radius_zero_trial_and_invalid_numbers():
    base = reference_run()
    bad = json.loads(json.dumps(base))
    bad["rho"]["cos"] = ["1"]
    bad["rho"]["sin"] = ["0"]
    with pytest.raises(ValueError, match="first Fourier"):
        validate(bad, CONFIG)
    bad = json.loads(json.dumps(base))
    bad["rho_lower_bound"] = "0"
    with pytest.raises(ValueError, match="strictly positive"):
        validate(bad, CONFIG)
    bad = json.loads(json.dumps(base))
    bad["trial"]["constant"] = "0"
    with pytest.raises(ValueError, match="nonzero"):
        validate(bad, CONFIG)
    for invalid in (True, 0.5, float("nan"), "1/0"):
        bad = json.loads(json.dumps(base))
        bad["rho_lower_bound"] = invalid
        with pytest.raises(ValueError):
            validate(bad, CONFIG)


def test_fixed_parameters_and_forged_scores():
    with pytest.raises(ValueError, match="fixed"):
        validate(reference_run(), {
            "id": CONFIG_ID,
            "parameters": {**_EXPECTED, "dimension": True},
            "direction": "minimize",
        })
    result = validate(reference_run(), CONFIG)
    for key, value in (("objective", -100), ("score", float("nan")), ("claimed_score", {"fake": 1})):
        assert validate({**reference_run(), key: value}, CONFIG) == result


def test_runner_error_and_timeout_controls():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T096 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T096 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
