import pytest

from tasks.t057.check import validate
from tasks.t057.human import run_code as human

CONFIG = {"id": "T057-C01", "parameters": {"max_cardinality": 512, "integer_interval": [-1000000, 1000000]}}


def test_human_exact_counts_and_interval():
    result = validate(human(), CONFIG, strict=True)
    assert result["details"]["sumset_size"] == 59
    assert result["details"]["difference_set_size"] == 55
    lo, hi = map(float, result["details"]["objective_interval"])
    assert lo <= 1.0597930945472454 <= hi
    assert result["verification_status"] == "certified"


@pytest.mark.parametrize("value", [True, 1.0, "1"])
def test_non_integer_rejected(value):
    with pytest.raises(ValueError):
        validate({"set": [0, 1, value]}, CONFIG)


@pytest.mark.parametrize("values", [[0, 0], [0], list(range(513)), [-1000001, 0, 1], [0, 1, 2]])
def test_invalid_sets_rejected(values):
    with pytest.raises(ValueError):
        validate({"set": values}, CONFIG)


def test_claimed_score_is_not_used():
    result = validate({**human(), "objective": -999}, CONFIG)
    assert result["details"]["sumset_size"] == 59
    assert result["details"]["claimed_objective_mismatch"]
