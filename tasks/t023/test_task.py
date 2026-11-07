import json
from pathlib import Path

import pytest

from tasks.t023.check import validate
from tasks.t023.human import run_code as human_run

CONFIG = {
    "id": "T023-C01",
    "parameters": {"strength": 4, "columns": 20, "alphabet_size": 2,
                   "rows_upper_bound": 6196},
    "direction": "minimize",
    "human_reference": 65,
}


def test_human_nist_witness_is_valid_and_recomputed():
    solution = human_run()
    result = validate({**solution, "claimed_objective": -100}, CONFIG)
    assert len(solution["array"]) == 65
    assert result["objective"] == 65
    assert result["verification_status"] == "exact"
    assert result["details"]["projection_count"] == 4845
    assert result["details"]["uncovered_tuples"] == 0
    assert result["details"]["claimed_objective_ignored"] is True


def test_row_upper_bound_is_enforced():
    cfg = {**CONFIG, "parameters": {**CONFIG["parameters"], "rows_upper_bound": 64}}
    with pytest.raises(ValueError, match="row count"):
        validate(human_run(), cfg)


def test_missing_projection_rejected():
    from itertools import product
    rows = [list(bits) + [0] * 16 for bits in product((0, 1), repeat=4)]
    rows.pop()
    with pytest.raises(ValueError, match="misses"):
        validate({"array": rows}, CONFIG)


def test_duplicate_rows_and_wrong_width_rejected():
    row = [0] * 20
    with pytest.raises(ValueError, match="duplicate"):
        validate({"array": [row, row]}, CONFIG)
    with pytest.raises(ValueError, match="columns"):
        validate({"array": [[0] * 19]}, CONFIG)


@pytest.mark.parametrize("bad", [True, -1, 2, 0.0, float("nan"), float("inf"), "0"])
def test_invalid_entries_rejected(bad):
    row = [0] * 20
    row[0] = bad
    with pytest.raises(ValueError, match="integers"):
        validate({"array": [row]}, CONFIG)


def test_bad_solution_shape_and_row_limit_rejected():
    with pytest.raises(ValueError, match="array"):
        validate([], CONFIG)
    cfg = {**CONFIG, "parameters": {**CONFIG["parameters"], "rows_upper_bound": 1}}
    with pytest.raises(ValueError, match="row count"):
        validate(human_run(), cfg)


def test_search_baseline_is_deterministic_and_valid(monkeypatch):
    from tasks.t023.baseline import run_code as search_run
    monkeypatch.setenv("MATHBENCH_SEED", "7")
    first = search_run()
    second = search_run()
    assert first["array"] == second["array"]
    assert first["search_metadata"]["iterations"] == 512
    assert validate(first, CONFIG)["objective"] == len(first["array"])


def test_zero_second_budget_falls_back_to_valid_seed(monkeypatch):
    from tasks.t023.baseline import run_code as search_run
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    solution = search_run()
    assert solution["search_metadata"]["fallback"] == "Hamming weight <= 4 seed"
    assert len(solution["array"]) == 6196
    assert validate(solution, CONFIG)["objective"] == 6196
