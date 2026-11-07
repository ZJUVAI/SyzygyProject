import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest
from tasks.t011.check import validate
from tasks.t011.init_program import run_code as run_seed
from tasks.t011.baseline import run_code as run_baseline
from tasks.t011.human import run_human
from tasks.t011.reference import run_code as run_reference

ROOT = Path(__file__).parent
CONFIGS = {
    "T011-C01": ({"q": 7, "power": 5}, 367, 367),
    "T011-C02": ({"q": 7, "power": 4}, 100, 100),
    "T011-C03": ({"q": 7, "power": 6}, 1101, 1120),
}

@pytest.mark.parametrize("cid", CONFIGS)
def test_seed_and_exact_objective(monkeypatch, cid):
    params, _, _ = CONFIGS[cid]
    seed_count = 3 ** params["power"]
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    sol = run_seed()
    config = {"id": cid, "parameters": params}
    result = validate(sol, config)
    for fake in (-1, 999999, {"fabricated": True}, ["not", "a", "score"], None):
        forged = dict(sol, objective=fake, score=fake)
        assert validate(forged, config) == result
    assert result["objective"] == seed_count
    assert result["details"]["claimed_objective_ignored"]
    assert result["details"]["all_pairs_checked"]

@pytest.mark.parametrize("cid", CONFIGS)
def test_human_and_reference_replay(monkeypatch, cid):
    params, human_count, record_count = CONFIGS[cid]
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    config = {"id": cid, "parameters": params}
    assert validate(run_human(), config, strict=True)["objective"] == human_count
    assert validate(run_reference(), config, strict=True)["objective"] == record_count

@pytest.mark.parametrize("cid", CONFIGS)
def test_baseline_valid(monkeypatch, cid):
    params, _, _ = CONFIGS[cid]
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0.05")
    assert validate(run_baseline(), {"id": cid, "parameters": params})["verification_status"] == "exact"

@pytest.mark.parametrize("cid", CONFIGS)
def test_damaged_witness_rejected_and_claim_ignored(monkeypatch, cid):
    params, _, _ = CONFIGS[cid]
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    sol = run_seed(); sol["objective"] = 999999
    sol["words"].append(sol["words"][0])
    with pytest.raises(ValueError): validate(sol, {"id": cid, "parameters": params})

@pytest.mark.parametrize("cid", CONFIGS)
def test_init_program_cold_export(tmp_path, cid):
    # Copy only the candidate source: no package, task metadata, or witnesses.
    shutil.copy(ROOT / "init_program.py", tmp_path / "candidate.py")
    script = f"import runpy,json; m=runpy.run_path({str(tmp_path / 'candidate.py')!r}); print(json.dumps(m['run_code']()))"
    env = dict(os.environ, MATHBENCH_CONFIG_ID=cid)
    out = subprocess.check_output([os.sys.executable, "-I", "-c", script], cwd=tmp_path, env=env, text=True)
    candidate = json.loads(out)
    assert len(candidate["words"]) == 3 ** CONFIGS[cid][0]["power"]
    assert validate(candidate, {"id": cid, "parameters": CONFIGS[cid][0]})["verification_status"] == "exact"

def test_wrong_configuration_parameters_rejected():
    with pytest.raises(ValueError): validate({"words": []}, {"id": "T011-C02", "parameters": {"q": 7, "power": 5}})
