from fractions import Fraction
from itertools import combinations
import json
from types import SimpleNamespace

import pytest

from tasks.t017.check import validate
from tasks.t017.human import SOLUTION
from tasks.t017.init_program import run_code


CONFIG = {"id": "T017-C01", "parameters": {"n": 11}, "direction": "maximize", "human_reference": "1/27"}


def test_goldberg_witness_exact_score():
    result = validate(SOLUTION, CONFIG)
    assert result["objective"] == "1/27"
    assert result["verification_status"] == "exact"
    assert result["details"] == {"triangles_checked": 165}


def test_seed_is_valid_and_positive():
    assert Fraction(validate(run_code(), CONFIG)["objective"]) > 0


def test_search_accepts_a_saved_rational_warm_start(tmp_path, monkeypatch):
    from tasks.t017 import evolution

    witness = tmp_path / "warm_start.json"
    witness.write_text(json.dumps(SOLUTION))
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG["id"])
    monkeypatch.setenv("MATHBENCH_WARM_START", str(witness))
    monkeypatch.setenv("MATHBENCH_EVOLUTION_SECONDS", "1")
    times = iter([0, 0, 2])  # Enter the first restart, then stop before optimization.
    monkeypatch.setattr(evolution, "time", SimpleNamespace(monotonic=lambda: next(times)))

    assert validate(evolution.run_code(), CONFIG)["objective"] == "1/27"


@pytest.mark.parametrize("bad", [
    {"points": [[0, 0]] * 11},
    {"points": [[-1, 0]] + [[i / 10, (i / 10) ** 2] for i in range(1, 11)]},
])
def test_invalid_inputs_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)
