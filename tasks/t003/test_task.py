from fractions import Fraction
import json
from pathlib import Path

import pytest

from tasks.t003.check import validate

ROOT = Path(__file__).parent

def cfg(n):
    return {"id": "T003-C02", "parameters": {"n": n}}

def witness(n):
    return json.loads((ROOT / "data" / f"human{n}.json").read_text())

def test_human_witness_exact():
    result = validate(witness(32), cfg(32), strict=True)
    assert result["verification_status"] == "certified"
    assert result["objective"] == "10982269511/3906250000"

def test_boundary_tangent_grid_is_valid():
    circles = [{"x": f"{2*c+1}/12", "y": f"{2*r+1}/12", "r": "1/12"}
               for r in range(6) for c in range(6)][:32]
    assert validate({"circles": circles}, cfg(32))["objective"] == str(Fraction(32, 12))

@pytest.mark.parametrize("n", [32])
def test_reject_wrong_size_and_wall_crossing(n):
    data = witness(n)
    with pytest.raises(ValueError):
        validate({"circles": data["circles"][:-1]}, cfg(n))
    data["circles"][0]["x"] = "1/100"
    with pytest.raises(ValueError):
        validate(data, cfg(n))

@pytest.mark.parametrize("n", [32])
def test_claimed_objective_is_ignored(n):
    data = witness(n)
    data["objective"] = "not even a number"
    result = validate(data, cfg(n), strict=True)
    assert result["details"]["claimed_objective_ignored"] is True
    assert result["objective"] != "999"

def test_reject_overlap_and_invalid_numbers():
    data = witness(32)
    data["circles"][1] = dict(data["circles"][0])
    with pytest.raises(ValueError):
        validate(data, cfg(32))
    data = witness(32)
    data["circles"][0]["r"] = True
    with pytest.raises(ValueError):
        validate(data, cfg(32))

@pytest.mark.parametrize("n", [32])
def test_evolution_is_deterministic_and_exact(n, monkeypatch):
    from tasks.t003.evolution import run_code
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T003-C02")
    monkeypatch.setenv("MATHBENCH_SEED", "19")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_GENERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_POPULATION", "4")
    first = run_code()
    second = run_code()
    assert first == second
    result = validate(first, cfg(n), strict=True)
    assert result["verification_status"] == "certified"
    assert first["search"]["evaluations"] >= 4
    assert Fraction(result["objective"]) >= (Fraction(n, 12) if n <= 36 else Fraction(5, 2))


def test_evolution_analytic_jacobian_matches_finite_difference(monkeypatch):
    import numpy as np
    import scipy.optimize
    from types import SimpleNamespace
    from tasks.t003 import evolution

    captured = {}
    def fake_minimize(fun, x0, jac, method, bounds, constraints, options, callback=None):
        captured.update(fun=fun, objective_jac=jac, x0=x0,
                        constraint=constraints["fun"], constraint_jac=constraints["jac"])
        return SimpleNamespace(x=x0)
    monkeypatch.setattr(scipy.optimize, "minimize", fake_minimize)
    points = [(120_000, 180_000), (610_000, 270_000), (360_000, 790_000)]
    evolution._polish(points, [20_000, 30_000, 25_000])
    x = captured["x0"] + np.linspace(0.00013, 0.00037, len(captured["x0"]))
    analytic = captured["constraint_jac"](x)
    eps = 1e-7
    numeric = np.column_stack([
        (captured["constraint"](x + eps*np.eye(len(x))[k]) -
         captured["constraint"](x - eps*np.eye(len(x))[k])) / (2*eps)
        for k in range(len(x))
    ])
    assert np.allclose(analytic, numeric, rtol=1e-6, atol=1e-7)
    objective_numeric = np.array([
        (captured["fun"](x + eps*np.eye(len(x))[k]) -
         captured["fun"](x - eps*np.eye(len(x))[k])) / (2*eps)
        for k in range(len(x))
    ])
    assert np.allclose(captured["objective_jac"](x), objective_numeric, atol=1e-8)


def test_evolution_repair_handles_near_wall_and_close_centers():
    from tasks.t003.evolution import _D, _repair
    points = [((2*c + 1) * _D // 12, (2*r + 1) * _D // 12)
              for r in range(6) for c in range(6)][:32]
    points[0] = (500, 500_000)
    points[1] = (1_500, 500_200)
    repaired = _repair(points, [40_000] * 32)
    assert repaired is not None
    assert validate({"circles": repaired[0]}, cfg(32), strict=True)["verification_status"] == "certified"


def test_basin_hopping_accepts_downhill_without_replacing_global_incumbent():
    import random
    from fractions import Fraction
    from tasks.t003.evolution import _accept

    rng = random.Random(7)
    assert _accept(Fraction(3), Fraction(3), 0.01, rng)
    # A small downhill step can move a chain; the caller stores the global best separately.
    assert _accept(Fraction(3), Fraction(299, 100), 0.01, rng)
    assert not _accept(Fraction(3), Fraction(2), 0.01, rng)
    assert not _accept(Fraction(3), Fraction(2), 0, rng)


def test_evolution_reports_bounded_solver_calls_and_keeps_exact_seed(monkeypatch):
    from fractions import Fraction
    import tasks.t003.evolution as evolution

    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T003-C02")
    monkeypatch.setenv("MATHBENCH_SEED", "31")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_GENERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_POPULATION", "4")
    monkeypatch.setattr(evolution, "_RESTART_AFTER", 0)
    result = evolution.run_code()
    search = result["search"]
    assert search["solver_calls"] == 2
    assert search["candidate_slots_per_generation"] == 4
    assert search["solver_calls"] <= search["generations"]
    assert search["restarts"] == 2
    assert search["restart_evaluations"] == 2
    assert search["evaluations"] == 4 + 8 + 2
    assert len(search["history"]) == search["generations"] + 1
    assert Fraction(search["history"][0]["objective"]) == Fraction(8, 3)
    assert Fraction(search["history"][-1]["objective"]) >= Fraction(8, 3)


def test_reject_removed_configurations():
    for config_id in ("T003-C01", "T003-C03"):
        with pytest.raises(ValueError):
            validate(witness(32), {"id": config_id})

def test_reject_config_parameter_mismatch():
    with pytest.raises(ValueError):
        validate(witness(32), {"id":"T003-C02", "parameters":{"n":26,"container":"unit square","radii":"variable"}})

def test_claimed_score_is_never_parsed():
    data=witness(32)
    data["objective"]={"arbitrary":"untrusted"}
    result=validate(data,cfg(32),strict=True)
    assert result["details"]["claimed_objective_ignored"] is True
    assert result["objective"]=="10982269511/3906250000"
