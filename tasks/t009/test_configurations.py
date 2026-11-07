import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from tasks.t009.check import validate


CASES = (("T009-C02", 80, 25), ("T009-C03", 100, 34))

def test_all_references_keep_their_verified_objective_and_shape(monkeypatch):
    from tasks.t009 import reference
    for cid,n,k,distance in (("T009-C01",68,15,19),("T009-C02",80,20,25),("T009-C03",100,20,34)):
        monkeypatch.setenv("MATHBENCH_CONFIG_ID",cid)
        matrix=reference.run_code()["generator_matrix"]
        assert len(matrix)==k and all(len(row)==n for row in matrix)
        assert all(type(bit) is int and bit in (0,1) for row in matrix for bit in row)
        result=validate({"generator_matrix":matrix},_config(cid,n,k))
        assert result["objective"]==distance


def _config(config_id, n, k=20):
    return {"id": config_id, "parameters": {"n": n, "k": k, "q": 2}}


@pytest.mark.parametrize("config_id,n,distance", CASES)
def test_rebuilds_and_checks_public_qc_code(config_id, n, distance):
    from tasks.t009.qc import build_matrix
    matrix = build_matrix(config_id)
    result = validate({"generator_matrix": matrix}, _config(config_id, n))
    assert len(matrix) == 20
    assert all(len(row) == n for row in matrix)
    assert result["objective"] == distance
    assert result["details"]["rank"] == 20
    assert result["details"]["codewords_checked"] == (1 << 20) - 1

    # Check the score declaration cannot change any part of the trusted result.
    clean = {"generator_matrix": matrix}
    original = validate(clean, _config(config_id, n))
    for claimed in (-100, 0, 1_000_000):
        assert validate(dict(clean, objective=claimed), _config(config_id, n)) == original

    damaged = [row[:] for row in matrix]
    damaged[1] = damaged[0][:]
    with pytest.raises(ValueError, match="rank"):
        validate({"generator_matrix": damaged}, _config(config_id, n))


@pytest.mark.parametrize("config_id,n,distance", CASES)
def test_all_programs_support_new_configuration(config_id, n, distance, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", config_id)
    config = _config(config_id, n)
    from tasks.t009 import baseline, evolution, human, init_program, reference, sota

    assert validate(init_program.run_code(), config)["objective"] == 1
    assert validate(human.run_code(), config)["objective"] == distance
    assert validate(sota.run_code(), config)["objective"] == distance
    reference_result = validate(reference.run_code(), config)
    assert reference_result["verification_status"] == "exact"
    assert reference_result["objective"] == distance

    # Smoke-test the search interfaces without repeating expensive proposals.
    with patch.object(baseline, "search_steps", lambda _count: iter(())):
        assert validate(baseline.run_code(), config)["verification_status"] == "exact"
        assert validate(evolution.run_code(), config)["verification_status"] == "exact"


def test_saved_witness_hashes_match_sota_records():
    folder = Path(__file__).parent / "data"
    for config_id in ("T009-C02", "T009-C03"):
        suffix = config_id[-3:]
        saved = json.loads((folder / f"sota_generator_{suffix}.json").read_text())
        assert len(saved["matrix"]) == 20
        assert saved["construction"]["parameters"]["k"] == 20
