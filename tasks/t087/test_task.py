import os
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t087.baseline import run_code as baseline_run_code
from tasks.t087.check import validate
from tasks.t087.evolution import run_code as evolution_run_code
from tasks.t087.human import run_code as human_run_code
from tasks.t087.init_program import run_code as init_run_code
from tasks.t087.reference import run_code as reference_run_code


CONFIG = {
    "id": "T087-C01",
    "parameters": {
        "steps": 480,
        "step_size": "13/4800",
        "support": "13/10",
        "height_domain": "nonnegative_rational",
    },
    "direction": "maximize",
    "human_reference": 0.361601515732983,
}


def test_public_ai_certificate_exact_replay():
    result = validate(reference_run_code(), CONFIG)
    assert result["objective"] == "2378625/5958277"
    assert result["objective_value"] == result["objective"]
    assert result["verification_status"] == "exact"
    assert result["details"]["l1_norm"] == "8801/72000"
    assert result["details"]["minimum_autocorrelation"] == "82459/13824000"
    assert result["details"]["minimum_location"] == {"type": "grid_node", "k": 216}
    assert result["details"]["claimed_objective_ignored"] is True


def test_human_formula_reconstruction_exact_score():
    result = validate(human_run_code(), CONFIG)
    assert result["objective"] == "15833948850637600/43788391811747427"
    assert len(human_run_code()["heights"]) == 480


def test_uniform_seed_checks_endpoint_interpolation():
    result = validate(init_run_code(), CONFIG)
    assert result["objective"] == "30/169"
    assert result["details"]["minimum_location"] == {"type": "endpoint", "t": "1"}
    assert result["details"]["continuous_interval_check"] == (
        "all 370 grid nodes and t=1 exact interpolation")


def test_baseline_and_evolution_entries_are_valid(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "42")
    for output in (baseline_run_code(), evolution_run_code()):
        result = validate(output, CONFIG)
        assert result["verification_status"] == "exact"
        assert result["details"]["steps"] == 480


@pytest.mark.parametrize("heights", [
    [1] * 479,
    [1] * 481,
    [0] * 480,
    [True] + [1] * 479,
    [-1] + [1] * 479,
    [float("nan")] + [1] * 479,
    [float("inf")] + [1] * 479,
    ["1//2"] + [1] * 479,
    ["-1/4"] + [1] * 479,
])
def test_invalid_heights_rejected(heights):
    with pytest.raises(ValueError):
        validate({"heights": heights, "objective": "999/1"}, CONFIG)


def test_exact_rational_strings_and_binary_float_heights():
    fractions = validate({"heights": ["1/2"] * 480}, CONFIG)
    assert fractions["objective"] == "30/169"
    binary = validate({"heights": [0.5] * 480}, CONFIG)
    assert binary["objective"] == "30/169"


def test_claimed_objective_and_scores_do_not_change_result():
    solution = reference_run_code()
    original = validate(solution, CONFIG)
    forged = dict(solution, objective=-1, score=float("nan"), claimed_score="0")
    assert validate(forged, CONFIG) == original


@pytest.mark.parametrize("config", [
    {"id": "T087-C02", "parameters": CONFIG["parameters"]},
    {"id": "T087-C01", "parameters": {**CONFIG["parameters"], "steps": 479}},
    {"id": "T087-C01", "parameters": {**CONFIG["parameters"], "step_size": "1/480"}},
    {"id": "T087-C01", "parameters": {**CONFIG["parameters"], "extra": 1}},
])
def test_inexact_configuration_rejected(config):
    with pytest.raises(ValueError):
        validate(init_run_code(), config)


def test_runner_error_and_timeout_controls():
    env = dict(os.environ)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise SystemExit(9)"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
