import math
import pytest
from tasks.t004.check import validate
from tasks.t004.human import run_code

def config(cid,n):
    return {"id":cid,"parameters":{"n":n,"space":"S2","objective":"minimum pairwise angular separation in radians"}}

@pytest.mark.parametrize("cid,n,pairs",[("T004-C01",16,120),("T004-C02",17,136),("T004-C03",19,171)])
def test_public_witness_strict_lower_bound_and_interval(cid,n,pairs,monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID",cid)
    result=validate(run_code(),config(cid,n),strict=True)
    assert result["verification_status"] == "certified"
    lo,hi=result["details"]["angle_interval"]
    assert 0 < lo <= hi <= math.pi
    assert result["objective"] == lo
    assert result["details"]["pairs_checked"] == pairs

def test_claimed_score_does_not_change_recomputed_score(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID","T004-C02")
    sol=run_code(); a=validate(sol,config("T004-C02",17),strict=True)
    sol["objective"]="1/2"; b=validate(sol,config("T004-C02",17),strict=True)
    assert a["objective"] == b["objective"]
    assert b["details"]["claimed_objective_mismatch"]

def test_rejects_damaged_duplicate_and_wrong_size(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID","T004-C03")
    sol=run_code(); c=config("T004-C03",19)
    sol["points"][0]=[0,0,0]
    with pytest.raises(ValueError): validate(sol,c,strict=True)
    sol=run_code(); sol["points"][1]=sol["points"][0]
    with pytest.raises(ValueError): validate(sol,c,strict=True)
    sol=run_code(); sol["points"].pop()
    with pytest.raises(ValueError): validate(sol,c,strict=True)

def test_rejects_bool_nonfinite_and_configuration_mismatch(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID","T004-C02")
    sol=run_code(); sol["points"][0][0]=True
    with pytest.raises(ValueError): validate(sol,config("T004-C02",17),strict=True)
    sol=run_code(); sol["points"][0][0]=float("nan")
    with pytest.raises(ValueError): validate(sol,config("T004-C02",17),strict=True)
    with pytest.raises(ValueError): validate(run_code(),config("T004-C02",18),strict=True)
