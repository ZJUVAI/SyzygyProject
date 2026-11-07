import copy
import pytest
from tasks.t032.check import validate
from tasks.t032.human import run_code

CONFIG = {"parameters": {"rows": 14, "columns": 19, "forbidden_submatrix": [3, 3]}}


def test_published_witness_and_recount():
    s = run_code()
    assert validate(s, CONFIG)["objective"] == 126
    s["objective"] = -999
    assert validate(s, CONFIG)["objective"] == 126


def test_bad_all_ones_block_rejected():
    s = {"matrix": [[0] * 19 for _ in range(14)]}
    for i in range(3):
        for j in range(3):
            s["matrix"][i][j] = 1
    with pytest.raises(ValueError):
        validate(s, CONFIG)


def test_repeated_rows_are_allowed_when_feasible():
    s = {"matrix": [[0] * 19 for _ in range(14)]}
    s["matrix"][0] = [1] * 19
    s["matrix"][1] = [1] * 19
    # Two identical rows are valid: a forbidden block needs three rows.
    assert validate(s, CONFIG)["objective"] == 38
    s["matrix"][2] = [1] * 19
    with pytest.raises(ValueError):
        validate(s, CONFIG)


@pytest.mark.parametrize("bad", [True, 0.0, float("nan"), 2])
def test_bad_entry_types_rejected(bad):
    s = {"matrix": [[0] * 19 for _ in range(14)]}
    s["matrix"][0][0] = bad
    with pytest.raises(ValueError):
        validate(s, CONFIG)


def test_dimensions_rejected():
    with pytest.raises(ValueError):
        validate({"matrix": [[0] * 19 for _ in range(13)]}, CONFIG)


def test_seed_zero_baseline_returns_global_incumbent():
    from tasks.t032.baseline import run_code as baseline_run

    result = baseline_run()
    meta = result["search_metadata"]
    value = validate(result, CONFIG)["objective"]
    assert meta["actual_steps"] == 10000
    assert meta["kicks"] == 10
    assert value == meta["incumbent_score"] == meta["returned_score"]
    assert value >= meta["final_search_state_score"]
    assert value == 117
