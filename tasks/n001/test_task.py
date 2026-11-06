import json
from pathlib import Path
import pytest
from tasks.n001.check import validate
from tasks.n001.init_program import run_code as run_seed
from tasks.n001.baseline import run_code as run_baseline
from tasks.n001.human import run_human
from tasks.n001.reference import run_code as run_reference

CONFIG = {"id": "N001-C01", "parameters": {"q": 7, "power": 5}}

def test_seed_and_score_derived():
    sol = run_seed(); sol["objective"] = -10
    result = validate(sol, CONFIG)
    assert result["objective"] == 243
    assert result["details"]["claimed_objective_mismatch"]

def test_reference_witness_exact():
    for sol in (run_human(), run_reference()):
        result = validate(sol, CONFIG, strict=True)
        assert result["objective"] == 367
        assert result["verification_status"] == "exact"

def test_baseline_valid(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0.05")
    assert validate(run_baseline(), CONFIG)["verification_status"] == "exact"

@pytest.mark.parametrize("bad", [
    {"words": [[0, 1, 2, 3]]},
    {"words": [[0, 1, 2, 3, 7]]},
    {"words": [[True, 1, 2, 3, 4]]},
    {"words": [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]]},
    {"words": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]},
])
def test_invalid_rejected(bad):
    with pytest.raises(ValueError): validate(bad, CONFIG)

def test_config_rejected():
    with pytest.raises(ValueError): validate({"words": []}, {"id": "N001-C02", "parameters": {"q": 7, "power": 5}})
