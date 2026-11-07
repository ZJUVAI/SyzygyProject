"""Exact tests for T097-C01."""
import ast
import copy
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t097.check import INSTANCE_PATH, PARAMETERS, validate
from tasks.t097.human import run_code as human_run
from tasks.t097.init_program import run_code as init_run
from tasks.t097.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {"id": "T097-C01", "parameters": PARAMETERS, "direction": "minimize", "human_reference": 15}


def _human_saved():
    return json.loads((TASK_DIR / "data/human/socg_fixed92_15.json").read_text())


def test_human_and_reference_rebuild_the_same_public_15_piece_cover():
    human = human_run()
    reference = reference_run()
    saved = json.loads((TASK_DIR / "data/human/socg_fixed92_15.json").read_text())
    assert human["polygons"] == reference["polygons"] == saved["polygons"]
    result = validate(reference, CONFIG, strict=True)
    assert result["objective"] == result["objective_value"] == 15
    assert result["verification_status"] == "certified"
    assert result["details"]["algebraic_field_degree"] == 1
    assert result["details"]["verified_open_arrangement_cells"] > 0


def test_irrational_algebraic_coordinates_are_supported_without_domain_restriction():
    solution = _human_saved()
    solution["algebraic_field"] = {
        "minimal_polynomial": ["-2", "0", "1"],
        "isolating_interval": ["1", "2"],
    }
    # Insert the exact point (96 + 104*sqrt(2), 704), which lies on a cover edge.
    solution["polygons"][0].insert(1, [["96", "104"], ["704"]])
    result = validate(solution, CONFIG)
    assert result["objective"] == 15
    assert result["details"]["algebraic_field_degree"] == 2


def test_higher_degree_algebraic_field_and_large_coefficients_are_supported():
    solution = _human_saved()
    solution["algebraic_field"] = {
        "minimal_polynomial": ["-2", "0", "0", "0", "0", "1"],
        "isolating_interval": ["1", "2"],
    }
    solution["polygons"][0].insert(1, [["96", "20"], ["704"]])
    result = validate(solution, CONFIG)
    assert result["objective"] == 15
    assert result["details"]["algebraic_field_degree"] == 5

    rational_solution = _human_saved()
    rational_solution["polygons"][0][0][0] = ["96", "7" * 5000]
    assert validate(rational_solution, CONFIG)["objective"] == 15


def test_initial_triangulation_is_a_valid_complete_cover():
    result = validate(init_run(), CONFIG, strict=True)
    assert result["objective"] == 90
    assert result["verification_status"] == "certified"


@pytest.mark.parametrize("bad", [None, [], 1, {"polygons": []}, {"polygons": [None]}])
def test_malformed_solution_shapes_are_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


@pytest.mark.parametrize("bad_field", [
    None,
    {"minimal_polynomial": ["-1", "0", "1"], "isolating_interval": ["0", "2"]},
    {"minimal_polynomial": ["-2", "0", "1"], "isolating_interval": ["2", "3"]},
    {"minimal_polynomial": ["0", "1"], "isolating_interval": ["0", "1"]},
    {"minimal_polynomial": ["0", True], "isolating_interval": ["-1", "1"]},
])
def test_nonminimal_or_invalid_algebraic_fields_are_rejected(bad_field):
    solution = _human_saved()
    solution["algebraic_field"] = bad_field
    with pytest.raises(ValueError):
        validate(solution, CONFIG)


@pytest.mark.parametrize("coordinate", [True, float("nan"), float("inf"), 1.25, ["1/0"], []])
def test_boolean_nonfinite_float_and_bad_rational_coordinates_are_rejected(coordinate):
    solution = _human_saved()
    solution["polygons"][0][0][0] = coordinate if isinstance(coordinate, list) else [coordinate]
    with pytest.raises(ValueError):
        validate(solution, CONFIG)


def test_nonconvex_or_degenerate_piece_is_rejected():
    solution = _human_saved()
    solution["polygons"][0] = [
        [["0"], ["0"]], [["2"], ["0"]], [["1"], ["1"]], [["2"], ["2"]], [["0"], ["2"]],
    ]
    with pytest.raises(ValueError, match="not convex"):
        validate(solution, CONFIG)
    degenerate = _human_saved()
    degenerate["polygons"][0] = [[["0"], ["0"]], [["1"], ["0"]], [["2"], ["0"]]]
    with pytest.raises(ValueError, match="positive area"):
        validate(degenerate, CONFIG)


def test_missing_coverage_and_outside_pieces_are_rejected():
    missing = _human_saved()
    missing["polygons"].pop()
    with pytest.raises(ValueError, match="do not cover exactly"):
        validate(missing, CONFIG)
    outside = _human_saved()
    outside["polygons"].append([
        [["0"], ["0"]], [["1"], ["0"]], [["1"], ["1"]], [["0"], ["1"]],
    ])
    with pytest.raises(ValueError, match="do not cover exactly"):
        validate(outside, CONFIG)


def test_duplicate_piece_is_valid_but_increases_the_exact_objective():
    solution = _human_saved()
    solution["polygons"].append(copy.deepcopy(solution["polygons"][0]))
    assert validate(solution, CONFIG)["objective"] == 16


@pytest.mark.parametrize("bad_config", [
    None, [], {}, {**CONFIG, "id": "T097-C02"}, {**CONFIG, "direction": "maximize"},
    {**CONFIG, "direction": None}, {**CONFIG, "parameters": {**PARAMETERS, "boundary_vertices": 93}},
    {**CONFIG, "parameters": {**PARAMETERS, "holes": False}},
])
def test_unknown_or_mismatched_configuration_is_rejected(bad_config):
    with pytest.raises(ValueError, match="configuration"):
        validate(_human_saved(), bad_config)


def test_input_checksum_is_verified(monkeypatch, tmp_path):
    corrupt = tmp_path / "input.json"
    corrupt.write_text("{}")
    monkeypatch.setattr("tasks.t097.check.INSTANCE_PATH", corrupt)
    with pytest.raises(ValueError, match="checksum"):
        validate(_human_saved(), CONFIG)


def test_claimed_scores_are_ignored_and_full_result_is_unchanged():
    solution = human_run()
    expected = validate(solution, CONFIG, strict=True)
    altered = copy.deepcopy(solution)
    altered.update(objective=-1000, objective_value=float("nan"), score=float("inf"), claimed_score="wrong")
    assert validate(altered, CONFIG, strict=True) == expected


def test_all_five_run_code_entries_return_valid_deterministic_solutions(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T097-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    from tasks.t097.baseline import run_code as baseline_run
    from tasks.t097.evolution import run_code as evolution_run

    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    results = [validate(candidate, CONFIG, strict=True) for candidate in outputs]
    assert [r["objective"] for r in results] == [90, 26, 26, 15, 15]
    assert all(r["verification_status"] == "certified" for r in results)
    assert outputs[3]["polygons"] == outputs[4]["polygons"]
    assert outputs[1] == baseline_run()
    assert outputs[2] == evolution_run()


def test_search_and_initializer_do_not_import_comparison_assets():
    for filename in ("init_program.py", "baseline.py", "evolution.py", "search_core.py"):
        tree = ast.parse((TASK_DIR / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert "human" not in (node.module or "") and "reference" not in (node.module or "")
            elif isinstance(node, ast.Import):
                assert all("human" not in item.name and "reference" not in item.name for item in node.names)


def test_cold_initializer_runs_from_only_its_file_and_public_input(tmp_path):
    source = (TASK_DIR / "init_program.py").read_text()
    imports = [node for node in ast.walk(ast.parse(source)) if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert all((isinstance(node, ast.Import) and all(item.name in {"json", "os"} for item in node.names))
               or (isinstance(node, ast.ImportFrom) and node.module == "pathlib") for node in imports)
    data = tmp_path / "data/source"
    data.mkdir(parents=True)
    shutil.copy(INSTANCE_PATH, data / INSTANCE_PATH.name)
    (tmp_path / "init_program.py").write_text(source)
    env = {"PATH": os.environ.get("PATH", ""), "MATHBENCH_CONFIG_ID": "T097-C01"}
    code = "import json,runpy; print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    result = subprocess.run([sys.executable, "-c", code], cwd=tmp_path, env=env,
                            check=True, capture_output=True, text=True, timeout=10)
    assert len(json.loads(result.stdout)["polygons"]) == 90


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T097 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T097 worker failure')"], env, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)


def test_evaluator_with_temporary_registry_patch(monkeypatch, tmp_path):
    import mathbench.evaluate as evaluate_module
    from tasks.t097.evaluator import evaluate
    monkeypatch.setattr(evaluate_module, "load_config", lambda task_id, config_id=None: CONFIG)
    monkeypatch.setattr(evaluate_module, "task_path", lambda task_id: TASK_DIR)
    result = evaluate(TASK_DIR / "reference.py", "T097-C01", strict=True, seed=0,
                      generation_timeout=30, verification_timeout=60, output_dir=tmp_path)
    assert result["validity"] == 1.0
    assert result["verification_status"] == "certified"
    assert result["objective"] == 15
