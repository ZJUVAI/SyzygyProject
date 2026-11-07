import json
from pathlib import Path

import pytest

from tasks.t001.check import validate
from tasks.t001.init_program import run_code as run_seed
from tasks.t001.human import run_human
from tasks.t001.reference import run_code as run_reference
from tasks.t001.baseline import run_code as run_baseline


CONFIGS = {
    "T001-C01": {"id": "T001-C01", "parameters": {"n": 26, "container": "unit square"}},
    "T001-C02": {"id": "T001-C02", "parameters": {"n": 32, "container": "unit square"}},
    "T001-C03": {"id": "T001-C03", "parameters": {"n": 50, "container": "unit square"}},
}
EXPECTED = {
    "T001-C01": "96362339/1000000000",
    "T001-C02": "10982269511/125000000000",
    "T001-C03": "14275420753/200000000000",
}


@pytest.mark.parametrize("cid", CONFIGS)
def test_human_and_reference_are_exact(cid, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    for candidate in (run_human(), run_reference()):
        result = validate(candidate, CONFIGS[cid], strict=True)
        assert result["verification_status"] == "exact"
        assert result["objective"] == EXPECTED[cid]


@pytest.mark.parametrize("cid", CONFIGS)
def test_seed_feasible_and_claim_ignored(cid, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    candidate = run_seed()
    expected = validate(candidate, CONFIGS[cid], strict=True)
    for claim in (-10, {"invalid": True}):
        candidate["objective"] = claim
        assert validate(candidate, CONFIGS[cid], strict=True) == expected


@pytest.mark.parametrize("cid", ["T001-C02", "T001-C03"])
def test_classical_baseline_returns_exact_feasible(cid, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0.05")
    result = validate(run_baseline(), CONFIGS[cid], strict=True)
    assert result["verification_status"] == "exact"


@pytest.mark.parametrize("cid", CONFIGS)
def test_invalid_objects_rejected(cid, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    n = CONFIGS[cid]["parameters"]["n"]
    for candidate in ({"radius": True, "centers": []},
                      {"radius": "NaN", "centers": []},
                      {"radius": "0.1", "centers": [["0.5", "0.5"]] * n}):
        with pytest.raises(ValueError):
            validate(candidate, CONFIGS[cid], strict=True)


@pytest.mark.parametrize("cid", CONFIGS)
def test_corrupt_boundary_overlap_and_nonfinite_rejected(cid, monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    candidate = run_seed()
    candidate["centers"][0][0] = "0.01"
    with pytest.raises(ValueError):
        validate(candidate, CONFIGS[cid])
    candidate = run_seed()
    candidate["centers"][1] = candidate["centers"][0]
    with pytest.raises(ValueError):
        validate(candidate, CONFIGS[cid])
    candidate = run_seed()
    candidate["centers"][0][0] = True
    with pytest.raises(ValueError):
        validate(candidate, CONFIGS[cid])


def test_expansion_metadata_matches_sol_accepted_configuration():
    root = Path(__file__).parent
    staged = json.loads((root / "configuration_expansion.json").read_text())
    live = json.loads((root / "task.json").read_text())
    assert staged["acceptance_status"] == "accepted_by_sol"
    assert [c["id"] for c in staged["configurations"]] == ["T001-C02", "T001-C03"]
    live_ids = [c["id"] for c in live["configurations"]]
    assert live_ids[0] == "T001-C01"
    assert {"T001-C02", "T001-C03"} <= set(live_ids)
    assert live["acceptance_status"] == "accepted_by_sol"
    for config in staged["configurations"]:
        released = next(c for c in live["configurations"] if c["id"] == config["id"])
        assert released["parameters"] == config["parameters"]
        assert released["human_reference"] == config["human_reference"]
