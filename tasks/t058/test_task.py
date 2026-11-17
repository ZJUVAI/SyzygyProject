import pytest

from tasks.t058.check import validate
from tasks.t058.human import run_code as human_run_code
from tasks.t058.init_program import run_code as init_run_code
from tasks.t058.reference import run_code as reference_run_code

CONFIG = {"id": "T058-C01", "parameters": {"marks": 29}, "direction": "minimize", "human_reference": 623}


def test_public_human_and_reference():
    expected = {"objective": 623, "verification_status": "exact", "details": {"marks": 29, "differences_checked": 406}}
    assert validate(human_run_code(), CONFIG) == expected
    assert validate(reference_run_code(), CONFIG) == expected


def test_initializer_is_valid():
    out = validate(init_run_code(), CONFIG)
    assert out["verification_status"] == "exact"
    assert isinstance(out["objective"], int)


@pytest.mark.parametrize("marks", [
    [0] * 29,
    [False] + list(range(1, 29)),
    [0.0] + list(range(1, 29)),
    list(range(28)),
    list(range(29)),
])
def test_invalid_or_non_golomb_rejected(marks):
    with pytest.raises(ValueError):
        validate({"marks": marks, "claimed_score": -1000}, CONFIG)


def test_translation_is_score_invariant():
    marks = [x + 17 for x in human_run_code()["marks"]]
    assert validate(marks, CONFIG)["objective"] == 623
