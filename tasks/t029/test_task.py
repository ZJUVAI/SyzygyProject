"""Tests for the exact rational 3x3 matrix multiplication rank task."""
import copy
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import sys

import pytest

from tasks.t029.baseline import run_code as baseline_run
from tasks.t029.check import validate
from tasks.t029.evolution import run_code as evolution_run
from tasks.t029.human import run_code as human_run
from tasks.t029.init_program import run_code as seed_run
from tasks.t029.reference import run_code as reference_run

TASK = Path(__file__).parent
CONFIG = json.loads((TASK / "task.json").read_text())["configurations"][0]


def test_human_witness_reconstructs_and_exactly_verifies():
    source = TASK / "data" / "source" / "3x3x3_tensor.mpl.bz2"
    witness = TASK / "data" / "laderman_rank23.json"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == (
        "c145cff7708b8472de23e0112c0722cae05f08bed2d9883b8dbf98cbb843169e"
    )
    assert hashlib.sha256(witness.read_bytes()).hexdigest() == (
        "c1debbeebc30dd64034ae83e1cbe9f5f7f3f112cbe7fe8db54cb152313994977"
    )
    assert human_run() == reference_run()
    assert len(human_run()["terms"]) == 23
    assert validate(human_run(), CONFIG)["objective"] == 23


def test_seed_and_strassen_baseline_are_valid_and_count_terms():
    seed = seed_run()
    baseline = baseline_run()
    assert validate(seed, CONFIG)["objective"] == 27
    assert validate(baseline, CONFIG)["objective"] == 26
    assert seed != baseline
    assert baseline["search_metadata"]["reference_data_read"] is False


def test_exact_rational_coefficients_and_fraction_api():
    candidate = seed_run()
    term = candidate["terms"][0]
    alpha_index = term["alpha"].index(1)
    beta_index = term["beta"].index(1)
    term["alpha"][alpha_index] = "1/2"
    term["beta"][beta_index] = Fraction(2, 1)
    assert validate(candidate, CONFIG)["objective"] == 27


def test_replaced_term_with_duplicate_breaks_exact_tensor_identity():
    candidate = seed_run()
    candidate["terms"][1] = copy.deepcopy(candidate["terms"][0])
    with pytest.raises(ValueError, match="tensor identity fails"):
        validate(candidate, CONFIG)


def test_rejects_invalid_dimensions_types_nonfinite_and_zero_factor():
    candidate = seed_run()
    candidate["terms"][0]["alpha"] = [1] * 8
    with pytest.raises(ValueError, match="nine"):
        validate(candidate, CONFIG)

    for invalid in (True, 0.5, "0.5", "1/0", "NaN", float("nan"), float("inf"), -float("inf")):
        damaged = seed_run()
        damaged["terms"][0]["alpha"][0] = invalid
        with pytest.raises(ValueError):
            validate(damaged, CONFIG)

    candidate = seed_run()
    candidate["terms"][0]["gamma"] = [0] * 9
    with pytest.raises(ValueError, match="zero factor"):
        validate(candidate, CONFIG)


def test_rejects_wrong_configuration_and_term_limit():
    with pytest.raises(ValueError, match="configuration"):
        validate(seed_run(), {"parameters": {**CONFIG["parameters"], "field": "F2"}})
    too_many = seed_run()
    too_many["terms"].append(copy.deepcopy(too_many["terms"][0]))
    with pytest.raises(ValueError, match="between 1 and 27"):
        validate(too_many, CONFIG)


def test_claimed_score_is_ignored_and_objective_is_recomputed():
    candidate = seed_run()
    candidate["claimed_objective"] = -1000000
    result = validate(candidate, CONFIG)
    assert result["objective"] == len(candidate["terms"]) == 27
    assert result["details"]["claimed_objective_ignored"] is True
    candidate["claimed_objective"] = math.inf
    assert validate(candidate, CONFIG)["objective"] == 27


def test_evolution_run_code_returns_valid_json_construction():
    first = evolution_run()
    second = evolution_run()
    assert first["terms"] == second["terms"]
    assert validate(first, CONFIG)["objective"] <= 27
    assert first["search_metadata"]["reference_data_read"] is False


def test_shared_generation_runner_handles_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(__import__("os").environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
