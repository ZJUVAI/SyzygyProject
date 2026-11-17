from fractions import Fraction
import pytest
try:
    from .check import validate
except ImportError:
    from check import validate

CFG={"id":"T084-C01","parameters":{"m":15},"direction":"maximize"}

def seed(): return {"pairs":[["1/4","1/4"] for _ in range(15)]}

def test_valid_seed_exact():
    out=validate(seed(),CFG)
    assert out["verification_status"]=="exact"
    assert out["details"]["routes"]==32768
    assert out["objective"] == "1/4"

def test_invalid_length():
    with pytest.raises(ValueError): validate({"pairs":[]},CFG)

def test_invalid_pair_constraint():
    s=seed(); s["pairs"][0]=["3/4","1/2"]
    with pytest.raises(ValueError): validate(s,CFG)

def test_reject_bool():
    s=seed(); s["pairs"][0]=[True,0]
    with pytest.raises(ValueError): validate(s,CFG)

def test_evolution_entrypoint_metadata(monkeypatch):
    try:
        from . import evolution
    except ImportError:
        import evolution
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    result=evolution.run_code()
    assert result["search_metadata"]["seed"]==17
    assert result["search_metadata"]["iterations"]==32
    assert result["search_metadata"]["reference_data_read"] is False
    assert len(result["pairs"])==15
    assert validate(result,CFG)["verification_status"]=="exact"
