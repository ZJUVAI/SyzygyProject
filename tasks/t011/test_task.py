import math

import pytest

from tasks.t011.check import validate
from tasks.t011.human import run_code


def config():
    return {
        "id": "T011-C01",
        "parameters": {
            "n": 16,
            "space": "S2",
            "objective": "minimum pairwise angular separation in radians",
        },
    }


def test_public_witness_has_certified_lower_bound(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T011-C01")
    result = validate(run_code(), config(), strict=True)
    assert result["verification_status"] == "certified"
    lo, hi = result["details"]["angle_interval"]
    assert 0 < lo <= hi <= math.pi
    assert result["objective"] == lo
    assert result["details"]["pairs_checked"] == 120


def test_claimed_score_does_not_change_recomputed_score(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T011-C01")
    solution = run_code()
    expected = validate(solution, config(), strict=True)
    solution["objective"] = "1/2"
    assert validate(solution, config(), strict=True) == expected


def test_rejects_damaged_duplicate_wrong_size_and_invalid_coordinates(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T011-C01")
    solution = run_code()
    solution["points"][0] = [0, 0, 0]
    with pytest.raises(ValueError):
        validate(solution, config(), strict=True)

    solution = run_code()
    solution["points"][1] = solution["points"][0]
    with pytest.raises(ValueError):
        validate(solution, config(), strict=True)

    solution = run_code()
    solution["points"].pop()
    with pytest.raises(ValueError):
        validate(solution, config(), strict=True)

    solution = run_code()
    solution["points"][0][0] = True
    with pytest.raises(ValueError):
        validate(solution, config(), strict=True)

    solution = run_code()
    solution["points"][0][0] = float("nan")
    with pytest.raises(ValueError):
        validate(solution, config(), strict=True)


def test_rejects_unsupported_configuration():
    with pytest.raises(ValueError):
        validate({"points": []}, {"id": "T011-C02", "parameters": {}}, strict=True)
