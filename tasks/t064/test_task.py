"""Exact geometry tests for the fixed ortho40 triangulation task."""
import ast
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t064.baseline import run_code as baseline_run
from tasks.t064.check import CONFIG_ID, INSTANCE_UID, _faces, _fraction, validate
from tasks.t064.evolution import run_code as evolution_run
from tasks.t064.human import run_code as human_run
from tasks.t064.init_program import run_code as seed_run
from tasks.t064.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": CONFIG_ID,
    "parameters": {"instance_uid": INSTANCE_UID, "coordinate_domain": "rational"},
    "direction": "minimize",
    "human_reference": 129,
}


def test_fixed_source_hash_and_exact_reference_witness():
    instance_path = TASK_DIR / "data/source/ortho40.instance.json"
    witness_path = TASK_DIR / "data/reference/ortho40_solution.json"
    assert hashlib.sha256(instance_path.read_bytes()).hexdigest() == (
        "f379e17cc7b4370d092ed37dcb6293dcb01c71d4f4c8e6cc4418c39ce178cad7"
    )
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == (
        "56bb1631924d9d254a399df25cb2ef0a1d9d18f228395dbefca98940b9151877"
    )
    result = validate(reference_run(), CONFIG, strict=True)
    assert result["objective"] == 19
    assert result["verification_status"] == "exact"
    assert result["details"]["total_vertices"] == 59
    assert result["details"]["edges"] == 121
    assert result["details"]["bounded_triangles"] == 63
    assert result["details"]["polygon_area2"] == "2711189126024"
    assert result["details"]["triangle_area2_sum"] == "2711189126024"


def test_reconstructed_human_grid_baseline_replays():
    generated = human_run()
    saved = json.loads((TASK_DIR / "data/human/ortho40_grid.json").read_text())
    assert generated == saved
    result = validate(generated, CONFIG)
    assert result["objective"] == 129
    assert result["verification_status"] == "exact"


def test_all_five_program_entries_return_valid_meshes(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    for run in (seed_run, baseline_run, human_run, reference_run, evolution_run):
        assert validate(run(), CONFIG)["verification_status"] == "exact"


def test_exported_seed_runs_with_only_public_input(tmp_path):
    shutil.copy(TASK_DIR / "init_program.py", tmp_path / "init_program.py")
    target = tmp_path / "data/source"
    target.mkdir(parents=True)
    shutil.copy(TASK_DIR / "data/source/ortho40.instance.json", target / "ortho40.instance.json")
    environment = {
        "PATH": os.environ.get("PATH", ""),
        "MATHBENCH_CONFIG_ID": CONFIG_ID,
        "MATHBENCH_SEED": "0",
    }
    code = "import json, runpy; print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    completed = subprocess.run(
        [sys.executable, "-c", code], cwd=tmp_path, env=environment,
        check=True, capture_output=True, text=True, timeout=20,
    )
    result = validate(json.loads(completed.stdout), CONFIG)
    assert result["objective"] == 129


def test_search_entries_are_seeded_fixed_count_and_do_not_import_comparisons(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "23")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first = baseline_run()
    assert first == baseline_run()
    assert first["search_metadata"]["iterations"] == 3
    assert first["search_metadata"]["reference_data_read"] is False
    evolved = evolution_run()
    assert evolved == evolution_run()
    assert evolved["search_metadata"]["iterations"] == 20
    assert evolved["search_metadata"]["seed"] == 23
    assert evolved["search_metadata"]["reference_data_read"] is False
    for filename in ("init_program.py", "baseline.py", "evolution.py"):
        tree = ast.parse((TASK_DIR / filename).read_text(encoding="utf-8"))
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                modules.append(node.module or "")
            elif isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
        assert not any("t064.human" in name or "t064.reference" in name for name in modules)


def test_explicit_zero_second_budget_returns_valid_mesh(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    result = evolution_run()
    assert result["search_metadata"]["iterations"] == 0
    assert result["search_metadata"]["budget"]["mode"] == "wall_clock_cutoff"
    assert validate(result, CONFIG)["verification_status"] == "exact"


def test_claimed_objectives_do_not_change_exact_validation():
    candidate = reference_run()
    expected = validate(candidate, CONFIG)
    changed = {
        **candidate,
        "objective": -1,
        "score": float("nan"),
        "claimed_score": float("inf"),
        "claimed_objective": True,
    }
    assert validate(changed, CONFIG) == expected


@pytest.mark.parametrize("mutation", ["duplicate_coordinate", "duplicate_edge", "missing_edge", "crossing_edge", "bad_index", "outside_point", "bool_index"])
def test_damaged_meshes_are_rejected(mutation):
    candidate = reference_run()
    if mutation == "duplicate_coordinate":
        candidate["steiner_points_x"][0] = "0"
        candidate["steiner_points_y"][0] = "0"
    elif mutation == "duplicate_edge":
        candidate["edges"].append(candidate["edges"][0][:])
    elif mutation == "missing_edge":
        candidate["edges"].pop()
    elif mutation == "crossing_edge":
        candidate["edges"][0] = [0, 2]
    elif mutation == "bad_index":
        candidate["edges"][0] = [0, 10000]
    elif mutation == "outside_point":
        candidate["steiner_points_x"][0] = "10000000"
        candidate["steiner_points_y"][0] = "10000000"
    elif mutation == "bool_index":
        candidate["edges"][0][0] = True
    with pytest.raises(ValueError):
        validate(candidate, CONFIG)


@pytest.mark.parametrize("bad", [True, float("nan"), float("inf"), "NaN", "1/0", "", "x"])
def test_bad_coordinates_are_rejected(bad):
    candidate = reference_run()
    candidate["steiner_points_x"][0] = bad
    with pytest.raises(ValueError):
        validate(candidate, CONFIG)


def test_arbitrary_length_rational_coordinate_is_not_truncated():
    value = "1/" + "2" * 5000
    parsed = _fraction(value)
    assert parsed.denominator == int("2" * 5000)


def test_finite_float_is_checked_as_its_exact_binary_rational():
    candidate = reference_run()
    candidate["steiner_points_x"][0] = 720358.5
    assert validate(candidate, CONFIG)["objective"] == 19


def test_nonobtuse_condition_is_exactly_checked_at_each_triangle_corner():
    points = ((0, 0), (4, 0), (1, 1))
    edges = ((0, 1), (1, 2), (0, 2))
    with pytest.raises(ValueError, match="obtuse"):
        _faces(points, edges, 3)


def test_wrong_configuration_or_instance_is_rejected():
    with pytest.raises(ValueError, match="configuration"):
        validate(reference_run(), {**CONFIG, "parameters": {"instance_uid": "other"}})
    candidate = reference_run()
    candidate["instance_uid"] = "other"
    with pytest.raises(ValueError, match="instance_uid"):
        validate(candidate, CONFIG)


def test_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
