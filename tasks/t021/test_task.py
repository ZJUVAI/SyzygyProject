from copy import deepcopy
import math

import pytest

from tasks.t021.check import validate
from tasks.t021.baseline import run_code as run_baseline
from tasks.t021.human import run_code


CONFIG = {
    "id": "T021-C01",
    "parameters": {
        "n": 32,
        "space": "unit sphere S2",
        "potential": "sum over unordered pairs 1 / Euclidean distance",
        "objective_unit": "Coulomb energy in unit-charge, unit-radius units",
    },
}


def test_human_witness_is_certified_and_covers_all_pairs():
    result = validate(run_code(), CONFIG, strict=True)
    lo, hi = map(lambda s: __import__("fractions").Fraction(s), result["details"]["objective_interval"])
    assert result["verification_status"] == "certified"
    assert lo < hi
    assert result["objective"] == str(hi)
    assert result["details"]["pairs_checked"] == 32 * 31 // 2
    assert float(lo) > 412.2612
    assert float(hi) < 412.2614


def test_baseline_uses_reproducible_fixed_default_search(monkeypatch):
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.delenv("MATHBENCH_SEED", raising=False)
    first = run_baseline()
    second = run_baseline()
    assert first == second
    assert first["search_metadata"] == {
        "algorithm": "seeded coordinate perturbation with simulated-annealing acceptance and best-witness retention",
        "seed": 0,
        "actual_iterations": 600,
        "iteration_budget": 600,
        "requested_seconds": None,
    }


def test_claimed_score_is_ignored():
    solution = run_code()
    first = validate(solution, CONFIG, strict=True)
    solution["objective"] = "this is not a number"
    second = validate(solution, CONFIG, strict=True)
    assert second["objective"] == first["objective"]
    assert second["details"] == first["details"]
    assert second["details"]["claimed_score_ignored"]


def test_certifies_extremely_close_distinct_points():
    solution = run_code()
    solution["points"][1] = [
        str(__import__("fractions").Fraction(solution["points"][0][0]) + __import__("fractions").Fraction(1, 10**30)),
        solution["points"][0][1],
    ]
    result = validate(solution, CONFIG, strict=True)
    assert result["verification_status"] == "certified"
    assert result["details"]["pairs_checked"] == 496


def test_rejects_duplicate_wrong_size_and_bad_pair():
    solution = run_code()
    solution["points"][1] = solution["points"][0]
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)
    solution = run_code()
    solution["points"].pop()
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)
    solution = run_code()
    solution["points"][0] = [1]
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)


def test_rejects_bool_and_nonfinite_parameter():
    for bad in (True, math.nan, math.inf, -math.inf, "not-a-rational", "1/0"):
        solution = run_code()
        solution["points"][0] = [bad, "0"]
        with pytest.raises(ValueError):
            validate(solution, CONFIG, strict=True)


def test_rejects_wrong_configuration():
    bad = deepcopy(CONFIG)
    bad["parameters"]["n"] = 31
    with pytest.raises(ValueError):
        validate(run_code(), bad, strict=True)

@pytest.mark.parametrize("config_id,n,expected", [("T021-C02",40,660.6752788),("T021-C03",50,1055.1823147)])
def test_added_ccd_records_are_exactly_recomputed(monkeypatch, config_id, n, expected):
    import json
    from pathlib import Path
    from tasks.t021 import human, reference, init_program
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", config_id)
    cfg={"id":config_id,"parameters":{"n":n,"space":"unit sphere S2","potential":"sum over unordered pairs 1 / Euclidean distance","objective_unit":"Coulomb energy in unit-charge, unit-radius units"}}
    witness=human.run_code()
    assert witness==reference.run_code()
    result=validate(witness,cfg,strict=True)
    assert result["verification_status"]=="certified"
    assert result["details"]["point_count"]==n
    from fractions import Fraction
    lo,hi=map(Fraction,result["details"]["objective_interval"])
    assert float(lo) > expected-1e-5 and float(hi) < expected+1e-5
    seed=init_program.run_code()
    assert len(seed["points"])==n
    broken={"points":witness["points"][:-1]}
    with pytest.raises(ValueError): validate(broken,cfg)
    forged={**witness,"objective":"0","claimed_score":"0"}
    assert validate(forged,cfg)==result


@pytest.mark.parametrize("config_id,n", [("T021-C01",32),("T021-C02",40),("T021-C03",50)])
def test_init_program_is_cold_export(tmp_path, config_id, n):
    import os, shutil, subprocess, sys
    source=__import__("pathlib").Path(__file__).with_name("init_program.py")
    exported=tmp_path/"init_program.py"; shutil.copy(source,exported)
    code=("import importlib.util,json; "
          f"s=importlib.util.spec_from_file_location('candidate',{str(exported)!r}); "
          "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
          "print(json.dumps(m.run_code()))")
    env={k:v for k,v in os.environ.items() if k!="PYTHONPATH"}; env["MATHBENCH_CONFIG_ID"]=config_id
    output=subprocess.run([sys.executable,"-I","-c",code],cwd=tmp_path,env=env,text=True,capture_output=True,check=True)
    assert len(__import__("json").loads(output.stdout)["points"])==n

@pytest.mark.parametrize("config_id,n", [("T021-C02",40),("T021-C03",50)])
def test_classical_search_is_configuration_aware(monkeypatch, config_id, n):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", config_id)
    candidate=run_baseline()
    assert len(candidate["points"])==n
    cfg={"id":config_id,"parameters":{"n":n,"space":"unit sphere S2","potential":"sum over unordered pairs 1 / Euclidean distance","objective_unit":"Coulomb energy in unit-charge, unit-radius units"}}
    assert validate(candidate,cfg)["details"]["pairs_checked"]==n*(n-1)//2
