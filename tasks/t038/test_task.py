import copy
import os
import sys

import pytest

from tasks.t038.check import validate
from tasks.t038 import baseline, evolution, human, init_program


CONFIG = {"parameters": {"order": 12}}


def test_starter_and_classical_baseline_are_valid():
    assert validate(init_program.run_code(), CONFIG)["objective"] == 1
    result = baseline.run_code()
    assert validate(result, CONFIG)["objective"] == 2


def test_human_witness_and_reference_are_valid():
    result = human.run_code()
    checked = validate(result, CONFIG)
    assert checked["objective"] == 5
    assert checked["details"]["orthogonal_pairs_checked"] == 10


@pytest.mark.parametrize("field,value", [
    ("objective", 999),
    ("score", -1),
    ("claimed_score", 999999),
    ("objective", float("nan")),
    ("score", float("nan")),
    ("claimed_score", float("nan")),
])
def test_all_claim_fields_leave_the_full_verification_result_unchanged(field, value):
    solution = human.run_code()
    expected = validate(solution, CONFIG)
    altered = copy.deepcopy(solution)
    altered[field] = value
    actual = validate(altered, CONFIG)
    assert actual == expected
    assert actual["objective"] == 5
    assert actual["details"]["claimed_objective_ignored"] is True


def test_broken_latin_row_rejected():
    result = init_program.run_code()
    result["squares"][0][0][0] = result["squares"][0][0][1]
    with pytest.raises(ValueError):
        validate(result, CONFIG)


def test_duplicate_square_is_rejected_by_orthogonality():
    square = init_program.run_code()["squares"][0]
    with pytest.raises(ValueError, match="not orthogonal"):
        validate({"squares": [square, copy.deepcopy(square)]}, CONFIG)


@pytest.mark.parametrize("value", [True, 1.0, float("nan"), float("inf"), "1"])
def test_non_integer_or_non_finite_symbol_rejected(value):
    result = init_program.run_code()
    result["squares"][0][0][0] = value
    with pytest.raises(ValueError):
        validate(result, CONFIG)


def test_empty_family_is_valid_boundary_case():
    assert validate({"squares": []}, CONFIG)["objective"] == 0


def test_evolution_preserves_valid_incumbent_and_records_actual_run():
    old = dict(os.environ)
    try:
        os.environ.update({"MATHBENCH_CONFIG_ID": "T038-C01", "MATHBENCH_SEED": "123", "MATHBENCH_SEARCH_ITERATIONS": "3"})
        result = evolution.run_code()
    finally:
        os.environ.clear()
        os.environ.update(old)
    assert validate(result, CONFIG)["objective"] >= 2
    assert result["search_metadata"]["seed"] == 123
    assert result["search_metadata"]["iterations_run"] == 3
    assert result["search_metadata"]["budget"]["iteration_limit"] == 3


def test_program_errors_and_timeouts_are_reported_by_runner():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
