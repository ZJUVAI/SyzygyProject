import pytest
from itertools import combinations

from tasks.t053.check import validate
from tasks.t053.init_program import run_code

CONFIG = {"id": "T053-C01", "parameters": {"v": 24, "k": 14, "t": 4}}


def test_seed_is_exact_cover():
    result = run_code()
    checked = validate(result, CONFIG)
    assert checked["objective"] == len(result["blocks"])
    assert checked["verification_status"] == "exact"
    assert checked["details"]["covered_four_subsets"] == 10626


def test_duplicate_blocks_rejected():
    b = list(range(14))
    with pytest.raises(ValueError, match="duplicate blocks"):
        validate({"blocks": [b, b]}, CONFIG)


@pytest.mark.parametrize("bad", [[True] + list(range(1, 14)), list(range(1, 15)), list(range(10))])
def test_bad_block_rejected(bad):
    with pytest.raises(ValueError):
        validate({"blocks": [bad]}, CONFIG)


def test_claimed_score_is_ignored():
    out = run_code()
    claimed = dict(out, objective=-1)
    checked = validate(claimed, CONFIG)
    assert checked["objective"] == len(out["blocks"])
    assert checked["details"]["claimed_objective_ignored"] is True


def test_unsupported_configuration_is_rejected(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T053-C02")
    with pytest.raises(ValueError, match="unsupported configuration"):
        run_code()
