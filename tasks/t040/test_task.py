from copy import deepcopy
from fractions import Fraction
import math
import os
import sys

import pytest

from tasks.t040.baseline import run_code as run_baseline
from tasks.t040.check import validate
from tasks.t040.evolution import run_code as run_evolution
from tasks.t040.human import run_code as run_human
from tasks.t040.reference import run_code as run_reference
from mathbench.evaluate import _run


CONFIG = {
    "id": "T040-C01",
    "parameters": {
        "n": 11,
        "space": "unit sphere S2 in R3",
        "objective": "Euclidean volume of the convex hull",
        "objective_unit": "unit-radius cubed",
    },
}


def test_reconstructed_human_and_reference_match_exactly():
    human = validate(run_human(), CONFIG, strict=True)
    reference = validate(run_reference(), CONFIG, strict=True)
    assert human["verification_status"] == reference["verification_status"] == "exact"
    assert human["objective"] == reference["objective"]
    assert human["details"]["unique_supporting_planes"] == 18
    assert human["details"]["triangles_after_face_triangulation"] == 18
    assert Fraction(human["objective"]) > Fraction(23546, 10000)
    assert Fraction(human["objective"]) < Fraction(23547, 10000)


def test_claimed_score_does_not_change_recomputed_objective():
    solution = run_reference()
    expected = validate(solution, CONFIG, strict=True)
    assert expected["details"]["claimed_objective_ignored"] is True
    for field, value in (("objective", "0"), ("score", -1), ("claimed_score", "not numeric")):
        changed = dict(solution)
        changed[field] = value
        assert validate(changed, CONFIG, strict=True) == expected


def test_seed_and_evolution_are_self_contained_and_bounded(monkeypatch):
    from tasks.t040 import init_program
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    seed = validate(init_program.run_code(), CONFIG, strict=True)
    assert Fraction(seed["objective"]) > 0
    assert run_evolution is run_baseline
    result = run_baseline()
    replay = run_baseline()
    assert result == replay
    assert Fraction(validate(result, CONFIG, strict=True)["objective"]) > 0
    assert result["search_metadata"]["seed"] == 0
    assert result["search_metadata"]["actual_iterations"] == 400
    assert result["search_metadata"]["iteration_budget"] == 400


def test_rejects_duplicate_wrong_size_and_non_sphere_point():
    solution = run_reference()
    solution["points"][1] = solution["points"][0]
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)
    solution = run_reference()
    solution["points"] = solution["points"][:-1]
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)
    solution = run_reference()
    solution["points"][0] = ["0", "0", "0"]
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)


@pytest.mark.parametrize("bad", [True, math.nan, math.inf, -math.inf, "nope", "1/0"])
def test_rejects_bad_coordinate_values(bad):
    solution = run_reference()
    solution["points"][0][0] = bad
    with pytest.raises(ValueError):
        validate(solution, CONFIG, strict=True)


def test_rejects_bad_config():
    bad = deepcopy(CONFIG)
    bad["parameters"]["n"] = 10
    with pytest.raises(ValueError):
        validate(run_reference(), bad, strict=True)


def test_chart_omits_south_pole_and_can_represent_north_pole():
    solution = run_human()
    solution["stereographic"][0] = ["0", "0"]
    result = validate(solution, CONFIG, strict=True)
    assert result["verification_status"] == "exact"
    assert result["details"]["input_representation"].endswith("south pole is omitted")


def test_worker_reports_program_error_and_timeout_without_registry():
    with pytest.raises(RuntimeError, match="Worker failed"):
        _run([sys.executable, "-c", "raise SystemExit(17)"], dict(os.environ), 2)
    with pytest.raises(TimeoutError, match="Wall time limit exceeded"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], dict(os.environ), 0.1)


def test_coplanar_quadrilateral_is_one_face_not_two_duplicate_facets():
    # Four rational points form a square in z=3/5. Seven other sphere points
    # lie below its plane. Each triple on the square defines the same exact
    # supporting plane, which must be counted once and triangulated twice.
    solution = {
        "points": [
            ["4/5", "0", "3/5"], ["0", "4/5", "3/5"],
            ["-4/5", "0", "3/5"], ["0", "-4/5", "3/5"],
            ["0", "0", "-1"], ["3/5", "0", "-4/5"],
            ["-3/5", "0", "-4/5"], ["0", "3/5", "-4/5"],
            ["0", "-3/5", "-4/5"], ["4/5", "0", "-3/5"],
            ["-4/5", "0", "-3/5"],
        ]
    }
    result = validate(solution, CONFIG, strict=True)
    assert result["verification_status"] == "exact"
    assert result["details"]["unique_supporting_planes"] < result["details"]["supporting_triples_found"]
    assert result["details"]["triangles_after_face_triangulation"] > result["details"]["unique_supporting_planes"]



@pytest.mark.parametrize(("cid", "n", "reported"), [
    ("T040-C02", 13, "2.612834152060"),
    ("T040-C03", 15, "2.804379381835"),
])
def test_expanded_sloane_configs(monkeypatch, cid, n, reported):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", cid)
    cfg = dict(CONFIG, id=cid, parameters=dict(CONFIG["parameters"], n=n))
    human = run_human()
    reference = run_reference()
    hresult = validate(human, cfg, strict=True)
    rresult = validate(reference, cfg, strict=True)
    assert hresult == rresult
    assert abs(float(Fraction(rresult["objective"])) - float(reported)) < 1e-10
    for forged in (dict(reference, objective="-999"), dict(reference, score={"fake": True})):
        assert validate(forged, cfg, strict=True) == rresult
    damaged = {**reference, "stereographic": reference["stereographic"][:-1]}
    with pytest.raises(ValueError):
        validate(damaged, cfg, strict=True)
    damaged = {**reference, "stereographic": reference["stereographic"] + [reference["stereographic"][0]]}
    with pytest.raises(ValueError):
        validate(damaged, cfg, strict=True)

@pytest.mark.parametrize(("cid", "n"), [("T040-C02", 13), ("T040-C03", 15)])
def test_expanded_cold_seed_single_file_isolated(monkeypatch, tmp_path, cid, n):
    import shutil
    import subprocess
    from pathlib import Path
    source = Path(__file__).with_name("init_program.py")
    shutil.copy(source, tmp_path / "candidate.py")
    env = dict(os.environ, MATHBENCH_CONFIG_ID=cid)
    script = f"import runpy,json; m=runpy.run_path({str(tmp_path / 'candidate.py')!r}); print(json.dumps(m['run_code']()))"
    output = subprocess.check_output([sys.executable, "-I", "-c", script], cwd=tmp_path, env=env, text=True)
    solution = __import__("json").loads(output)
    cfg = dict(CONFIG, id=cid, parameters=dict(CONFIG["parameters"], n=n))
    assert len(solution["stereographic"]) == n
    assert validate(solution, cfg, strict=True)["verification_status"] == "exact"
