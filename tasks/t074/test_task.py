"""Exact tests for T074-C01."""

import hashlib
import json
import os
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sys

import pytest

from tasks.t074.check import PARAMETERS, validate
from tasks.t074.construction import reconstruct_rational_points


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T074-C01", "parameters": PARAMETERS}
SOURCE_SHA256 = "c5eaf80a1b3f270b949fe891eb9777541f0330c6d33a33e7b3d1eaa267c03b27"
WITNESS_SHA256 = "6e7f78156eac11badf81609e08f0c4600e98e31c42000867585e9d6d9cda11b4"


def _cross(a, b, c):
    return (b[0]-a[0]) * (c[1]-a[1]) - (b[1]-a[1]) * (c[0]-a[0])


def _independent_geometry(points):
    # The known hull order is checked with a separate shoelace calculation.
    hull = [points[i] for i in (0, 1, 10, 8, 9, 6, 4, 5, 2)]
    hull_twice_area = abs(sum(
        hull[i][0] * hull[(i+1) % len(hull)][1]
        - hull[(i+1) % len(hull)][0] * hull[i][1]
        for i in range(len(hull))
    ))
    twice_areas = [abs(_cross(*triple)) for triple in combinations(points, 3)]
    return min(twice_areas), hull_twice_area, len(twice_areas)


def _parse_points(solution):
    return [tuple(Fraction(value) for value in point) for point in solution["points"]]


def test_source_and_rationalized_witness_are_pinned_and_linked():
    source_path = ROOT / "data/source/tejstead_convex_n12.json"
    witness_path = ROOT / "data/reference/cantrell_n12_rationalized.json"
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == SOURCE_SHA256
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == WITNESS_SHA256
    reconstructed = reconstruct_rational_points(source_path)
    saved = json.loads(witness_path.read_text(encoding="utf-8"))
    assert reconstructed == {"points": saved["points"]}
    assert saved["ratio"] == "2/51"


def test_exact_public_score_and_independent_area_recomputation():
    from tasks.t074.human import run_code as human_run
    from tasks.t074.reference import run_code as reference_run

    human = human_run()
    reference = reference_run()
    assert human == reference
    points = _parse_points(human)
    min_twice_area, hull_twice_area, triangle_count = _independent_geometry(points)
    assert triangle_count == 220
    assert min_twice_area == Fraction(1, 2)
    assert hull_twice_area == Fraction(51, 4)
    result = validate(human, CONFIG, strict=True)
    assert result["objective"] == "2/51"
    assert result["details"]["minimum_triangle_area"] == "1/4"
    assert result["details"]["convex_hull_area"] == "51/8"
    assert result["details"]["hull_vertex_count"] == 9
    assert result["details"]["triangles_checked"] == 220


def test_all_five_entries_return_valid_solutions(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T074-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "5")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_BASELINE_ITERATIONS", "8")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_POPULATION", "2")
    from tasks.t074.init_program import run_code as initial
    from tasks.t074.baseline import run_code as baseline
    from tasks.t074.evolution import run_code as evolution
    from tasks.t074.human import run_code as human
    from tasks.t074.reference import run_code as reference

    results = [initial(), baseline(), evolution(), human(), reference()]
    scores = [Fraction(validate(item, CONFIG, strict=True)["objective"]) for item in results]
    assert len(results[0]["points"]) == 12
    assert scores[0] > 0 and scores[1] > 0 and scores[2] > 0
    assert scores[3:] == [Fraction(2, 51), Fraction(2, 51)]
    assert results[1]["search_metadata"]["iterations_run"] == 8
    assert results[2]["search_metadata"]["generations_run"] == 2


def test_checker_accepts_unbounded_rational_coordinates_and_is_affine_invariant():
    witness = json.loads((ROOT / "data/reference/cantrell_n12_rationalized.json").read_text())
    source_points = [tuple(Fraction(v) for v in point) for point in witness["points"]]
    scale = 10**300 + 33
    shift_x, shift_y = 10**450 + 1, -(10**430 + 9)
    transformed = {
        "points": [[str(scale * x + shift_x), str(scale * y + shift_y)] for x, y in source_points]
    }
    assert validate(transformed, CONFIG, strict=True)["objective"] == "2/51"


def test_checker_rejects_duplicates_collinear_points_bad_shapes_and_types():
    witness = json.loads((ROOT / "data/reference/cantrell_n12_rationalized.json").read_text())
    duplicate = [point[:] for point in witness["points"]]
    duplicate[-1] = duplicate[0][:]
    with pytest.raises(ValueError, match="distinct"):
        validate({"points": duplicate}, CONFIG)

    collinear = [[i, 2*i + 1] for i in range(12)]
    with pytest.raises(ValueError, match="collinear"):
        validate({"points": collinear}, CONFIG)

    with pytest.raises(ValueError, match="exactly 12"):
        validate({"points": witness["points"][:-1]}, CONFIG)
    with pytest.raises(ValueError, match="two coordinates"):
        validate({"points": [[0]] * 12}, CONFIG)

    for invalid in (True, float("nan"), float("inf"), "not a fraction", "1/0"):
        bad = [point[:] for point in witness["points"]]
        bad[0][0] = invalid
        with pytest.raises(ValueError):
            validate({"points": bad}, CONFIG)
    with pytest.raises(ValueError, match="configuration must fix"):
        validate({"points": witness["points"]}, {"id": "T074-C01", "parameters": {**PARAMETERS, "point_count": 11}})


def test_claimed_scores_do_not_change_recomputed_result():
    from tasks.t074.init_program import run_code

    candidate = run_code()
    expected = validate(candidate, CONFIG)
    for key, value in (("objective", "999"), ("score", float("nan")), ("claimed_score", {"fake": True})):
        assert validate({**candidate, key: value}, CONFIG) == expected


def test_records_keep_reported_record_and_optimality_status_distinct():
    sota = json.loads((ROOT / "sota.json").read_text())
    records = json.loads((ROOT / "records.json").read_text())
    entry = sota["configurations"]["T074-C01"]
    assert entry["public_value"] == entry["reproduced_value"] == "2/51"
    assert entry["highest_reported"]["value"] == "2/51"
    assert records["configurations"]["T074-C01"]["optimality_status"]["status"] == "open in the sources checked"


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T074 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T074 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
