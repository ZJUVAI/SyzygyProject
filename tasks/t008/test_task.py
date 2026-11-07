import pytest
from itertools import combinations

from tasks.t008.check import validate
from tasks.t008.init_program import run_code

CONFIG = {"id": "T008-C01", "parameters": {"v": 24, "k": 14, "t": 4}}


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


def test_c02_public_witness_is_exact_cover():
    import json
    from pathlib import Path
    from tasks.t008.sota import run_code as public_cover
    config = {"id": "T008-C02", "parameters": {"v": 20, "k": 10, "t": 4}}
    import os
    old = os.environ.get("MATHBENCH_CONFIG_ID")
    os.environ["MATHBENCH_CONFIG_ID"] = "T008-C02"
    try:
        result = public_cover()
    finally:
        if old is None:
            os.environ.pop("MATHBENCH_CONFIG_ID", None)
        else:
            os.environ["MATHBENCH_CONFIG_ID"] = old
    checked = validate(result, config)
    assert checked["objective"] == 36
    assert checked["details"]["total_t_subsets"] == 4845
    forged = dict(result, objective=-100)
    assert validate(forged, config) == checked
    damaged = dict(result, blocks=result["blocks"][:-1])
    with pytest.raises(ValueError, match="covering misses"):
        validate(damaged, config)


def test_c02_initial_program_is_valid(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T008-C02")
    result = run_code()
    checked = validate(result, CONFIG | {"id": "T008-C02", "parameters": {"v": 20, "k": 10, "t": 4}})
    assert checked["verification_status"] == "exact"
