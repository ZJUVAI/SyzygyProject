import pytest

from tasks.t009.check import validate


def test_c01_references_keep_their_verified_objective_and_shape(monkeypatch):
    from tasks.t009 import reference
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T009-C01")
    matrix=reference.run_code()["generator_matrix"]
    assert len(matrix)==15 and all(len(row)==68 for row in matrix)
    assert all(type(bit) is int and bit in (0,1) for row in matrix for bit in row)
    result=validate({"generator_matrix":matrix},_config("T009-C01",68,15))
    assert result["objective"]==19


def _config(config_id, n, k=15):
    return {"id": config_id, "parameters": {"n": n, "k": k, "q": 2}}


def test_programs_reject_removed_configurations(monkeypatch):
    from tasks.t009 import baseline, evolution, human, init_program, reference, sota
    for config_id in ("T009-C99",):
        monkeypatch.setenv("MATHBENCH_CONFIG_ID", config_id)
        for module in (baseline, evolution, human, init_program, reference, sota):
            with pytest.raises(ValueError, match="unsupported"):
                module.run_code()
