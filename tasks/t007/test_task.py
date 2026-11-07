import pytest

from tasks.t007.check import validate
from tasks.t007.human import run_code as human_run_code
from tasks.t007.init_program import run_code as init_run_code
from tasks.t007.reference import run_code as reference_run_code

CONFIG = {"id": "T007-C01", "parameters": {"marks": 29}, "direction": "minimize", "human_reference": 623}


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


@pytest.mark.parametrize(("config_id", "count", "objective"), [
    ("T007-C02", 30, 680),
    ("T007-C03", 32, 784),
])
def test_expansion_human_reference_and_seed(monkeypatch, config_id, count, objective):
    config = {"id": config_id, "parameters": {"marks": count}, "direction": "minimize",
              "human_reference": objective}
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", config_id)
    expected = {"objective": objective, "verification_status": "exact",
                "details": {"marks": count, "differences_checked": count * (count - 1) // 2}}
    assert validate(human_run_code(), config) == expected
    assert validate(reference_run_code(), config) == expected
    assert validate(init_run_code(), config)["verification_status"] == "exact"


def test_expansion_claimed_score_is_ignored(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T007-C02")
    out = human_run_code()
    out["claimed_score"] = -1
    assert validate(out, {"parameters": {"marks": 30}})["objective"] == 680


def test_expansion_rejects_invalid_ruler():
    with pytest.raises(ValueError):
        validate({"marks": list(range(30)), "claimed_score": -1},
                 {"parameters": {"marks": 30}})
