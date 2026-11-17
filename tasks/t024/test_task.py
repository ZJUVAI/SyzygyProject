"""Exact T024 checker and program tests."""
import hashlib, json
import os, sys
from pathlib import Path
import pytest
from tasks.t024.check import validate
from tasks.t024.init_program import run_code as seed
from tasks.t024.baseline import run_code as baseline
from tasks.t024.evolution import run_code as evolution
from tasks.t024.human import run_code as human
from tasks.t024.reference import run_code as reference
from mathbench.evaluate import _run

CONFIG = {"id": "T024-C01", "parameters": {"grid_size": 100}, "direction": "maximize", "human_reference": 16}

def independent_triple_audit(points):
    ps = [tuple(p) for p in points]
    for i, a in enumerate(ps):
        for j in range(i+1, len(ps)):
            b = ps[j]
            for c in ps[j+1:]:
                ds = sorted(((a[0]-b[0])**2+(a[1]-b[1])**2,
                             (a[0]-c[0])**2+(a[1]-c[1])**2,
                             (b[0]-c[0])**2+(b[1]-c[1])**2))
                if ds[0] == ds[1] or ds[1] == ds[2]: return False
    return True

def test_alphaevolve_reference_witness():
    path = Path(__file__).parent / "data/reference/alphaevolve_n100_164.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "d9aedb326481ea234afc32b8925b365c32bac2e2b2284f71262a04f7d2eb8aba"
    result = validate(reference(), CONFIG, strict=True)
    assert result["objective"] == 164
    assert result["verification_status"] == "exact"
    assert independent_triple_audit(reference()["points"])

def test_classical_human_method_formula_and_boundary():
    candidate = human(); xs = [p[0] for p in candidate["points"]]
    path = Path(__file__).parent / "data/reference/odlyzko_stanley_n100_16.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "1a723d3c6556edfbbd4a949b3b7e3772d339676f6bcb8c7f08fe01df5b1a71c7"
    assert json.loads(path.read_text(encoding="utf-8")) == candidate
    assert len(xs) == 16 and max(xs) == 41 and all(y == 0 for _, y in candidate["points"])
    assert validate(candidate, CONFIG, strict=True)["objective"] == 16
    assert independent_triple_audit(candidate["points"])

def test_seed_search_entries_are_valid_and_search_improves_seed():
    assert validate(seed(), CONFIG)["objective"] == 2
    searched = baseline()
    assert validate(searched, CONFIG)["objective"] == len(searched["points"])
    assert len(searched["points"]) > 2
    assert validate(evolution(), CONFIG)["objective"] > 2

@pytest.mark.parametrize("bad", [
    {"points": [[0,0],[1,0],[2,0]]}, # collinear midpoint
    {"points": [[0,0],[1,0],[0,1]]}, # right isosceles
    {"points": [[0,0],[0,0]]},
    {"points": [[100,0]]},
    {"points": [[True,0]]},
    {"points": [[1.0,0]]},
])
def test_invalid_constructions_rejected(bad):
    with pytest.raises(ValueError): validate(bad, CONFIG)

def test_claimed_objective_fields_do_not_change_validation():
    original = reference()
    expected = validate(original, CONFIG)
    for key in ("objective", "score", "claimed_score", "claimed_objective"):
        changed = dict(original); changed[key] = -10**9
        assert validate(changed, CONFIG) == expected

def test_empty_single_and_two_point_boundary():
    assert validate({"points": []}, CONFIG)["objective"] == 0
    assert validate({"points": [[99,99]]}, CONFIG)["objective"] == 1
    assert validate({"points": [[0,0],[99,99]]}, CONFIG)["objective"] == 2

def test_runner_success_error_and_timeout_controls():
    _run([sys.executable, "-c", "pass"], dict(os.environ), 2)
    with pytest.raises(RuntimeError):
        _run([sys.executable, "-c", "raise RuntimeError('expected')"], dict(os.environ), 2)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], dict(os.environ), 0.1)
