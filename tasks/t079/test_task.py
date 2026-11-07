"""Exact tests for T079 finite-field Kakeya line systems."""

import ast
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t079.check import CANONICAL_DIRECTIONS, PARAMETERS, P, validate
from tasks.t079.human import run_code as human_run
from tasks.t079.init_program import run_code as init_run
from tasks.t079.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T079-C01",
    "parameters": PARAMETERS,
    "direction": "minimize",
    "human_reference": 8641,
}


def test_canonical_projective_directions_are_complete_and_unique():
    assert len(CANONICAL_DIRECTIONS) == (31**3 - 1) // (31 - 1) == 993
    assert len(set(CANONICAL_DIRECTIONS)) == 993
    assert all(d[-1] == 1 or d[-2] == 1 or d[-3] == 1 for d in CANONICAL_DIRECTIONS)


def test_traditional_human_construction_exactly_recomputes_8641():
    witness = human_run()
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 8641
    assert result["details"]["projective_directions_checked"] == 993
    assert result["details"]["line_points_generated"] == 31 * 993
    assert result["verification_status"] == "exact"


def test_published_station_formula_rebuilds_and_exactly_checks_8289():
    witness = reference_run()
    saved = json.loads((TASK_DIR / "data/reference/station_p31_8289.json").read_text())
    result = validate(witness, CONFIG, strict=True)
    assert witness == saved
    assert result["objective"] == 8289
    assert result["objective"] == (2 * 31**3 + 7 * 31**2 + 3) // 8
    assert result["details"]["projective_directions_checked"] == 993


def test_saved_human_witness_matches_human_program():
    saved = json.loads((TASK_DIR / "data/human/quadratic_residue_q31.json").read_text())
    assert saved == human_run()
    assert validate(saved, CONFIG)["objective"] == 8641


def test_all_lines_through_origin_is_valid_full_space_boundary():
    solution = init_run()
    result = validate(solution, CONFIG, strict=True)
    assert len(solution["lines"]) == 993
    assert result["objective"] == 31**3 == 29791


def test_missing_or_extra_line_records_are_rejected():
    witness = reference_run()
    for lines in (witness["lines"][:-1], witness["lines"] + [witness["lines"][0]]):
        with pytest.raises(ValueError, match="993"):
            validate({"lines": lines}, CONFIG)
    with pytest.raises(ValueError, match="list"):
        validate({"lines": None}, CONFIG)


def test_duplicate_projective_direction_is_rejected_even_if_origin_differs():
    witness = reference_run()
    broken = copy.deepcopy(witness)
    broken["lines"][-1]["direction"] = broken["lines"][0]["direction"]
    with pytest.raises(ValueError, match="duplicate projective direction"):
        validate(broken, CONFIG)


@pytest.mark.parametrize("bad_record", [
    None,
    [],
    {"direction": [0, 0, 0], "origin": [0, 0, 0]},
    {"direction": [0, 0, 2], "origin": [0, 0, 0]},
    {"direction": [0, 0, 1], "origin": [0, 0, 31]},
    {"direction": [0, 0, 1], "origin": [0, 0, False]},
    {"direction": [0, 0, 1.0], "origin": [0, 0, 0]},
    {"direction": [0, 0, float("nan")], "origin": [0, 0, 0]},
    {"direction": [0, 0, float("inf")], "origin": [0, 0, 0]},
    {"direction": [0, 0, 1], "origin": [0, 0]},
    {"direction": [0, 0, 1], "origin": [0, 0, 0], "score": 3},
])
def test_malformed_line_records_are_rejected(bad_record):
    witness = reference_run()
    witness["lines"][0] = bad_record
    with pytest.raises(ValueError):
        validate(witness, CONFIG)


@pytest.mark.parametrize("bad_config", [None, [], {}, {"id": "T079-C02", "parameters": PARAMETERS}])
def test_missing_and_unknown_configuration_is_rejected(bad_config):
    with pytest.raises(ValueError, match="configuration"):
        validate({"lines": reference_run()["lines"]}, bad_config)


def test_wrong_parameters_are_rejected():
    bad = {**CONFIG, "parameters": {**PARAMETERS, "field_order": 29}}
    with pytest.raises(ValueError, match="parameters"):
        validate({"lines": reference_run()["lines"]}, bad)


def test_claimed_scores_never_change_validation_result():
    witness = reference_run()
    expected = validate(witness, CONFIG)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", float("inf"))):
        candidate = {**witness, key: value}
        assert validate(candidate, CONFIG) == expected


def test_all_five_programs_return_exactly_valid_objects(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T079-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "4")
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    from tasks.t079.baseline import run_code as baseline_run
    from tasks.t079.evolution import run_code as evolution_run

    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    results = [validate(value, CONFIG, strict=True) for value in outputs]
    assert all(result["verification_status"] == "exact" for result in results)
    assert results[0]["objective"] == 29791
    assert results[1]["objective"] == results[2]["objective"] == 29791
    assert results[3]["objective"] == 8641
    assert results[4]["objective"] == 8289


def test_search_is_seeded_bounded_and_never_reads_comparisons(monkeypatch):
    from tasks.t079.baseline import run_code as baseline_run
    from tasks.t079.evolution import run_code as evolution_run

    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T079-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    baseline = baseline_run()
    assert baseline == baseline_run()
    assert baseline["search_metadata"]["candidate_anchors_evaluated"] == 993 * 8
    assert baseline["search_metadata"]["comparison_data_read"] is False
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    evolution = evolution_run()
    assert evolution["search_metadata"]["completed_sweeps"] == 0
    assert evolution["search_metadata"]["candidate_anchors_evaluated"] == 0
    assert evolution["search_metadata"]["comparison_data_read"] is False


def test_cold_initializer_is_self_contained_in_a_clean_export(tmp_path):
    source = (TASK_DIR / "init_program.py").read_text()
    tree = ast.parse(source)
    imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]
    assert len(imports) == 1 and isinstance(imports[0], ast.Import)
    assert [alias.name for alias in imports[0].names] == ["os"]
    module = tmp_path / "init_program.py"
    module.write_text(source)
    env = {
        "PATH": os.environ.get("PATH", ""),
        "MATHBENCH_CONFIG_ID": "T079-C01",
        "MATHBENCH_SEED": "0",
    }
    command = "import json, runpy; print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    completed = subprocess.run([sys.executable, "-c", command], cwd=tmp_path, env=env,
                               check=True, capture_output=True, text=True, timeout=5)
    assert json.loads(completed.stdout) == init_run()


def test_search_programs_do_not_import_human_or_reference():
    for filename in ("baseline.py", "evolution.py", "search_core.py", "init_program.py"):
        tree = ast.parse((TASK_DIR / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert "human" not in (node.module or "") and "reference" not in (node.module or "")
            elif isinstance(node, ast.Import):
                assert all("human" not in item.name and "reference" not in item.name for item in node.names)


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T079 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T079 worker failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)


def test_evaluator_with_temporary_registry_patch(monkeypatch, tmp_path):
    import mathbench.evaluate as evaluate_module
    from tasks.t079.evaluator import evaluate

    monkeypatch.setattr(evaluate_module, "load_config", lambda task_id, config_id=None: CONFIG)
    monkeypatch.setattr(evaluate_module, "task_path", lambda task_id: TASK_DIR)
    result = evaluate(TASK_DIR / "reference.py", "T079-C01", strict=True, seed=0,
                      generation_timeout=20, verification_timeout=20, output_dir=tmp_path)
    assert result["validity"] == 1.0
    assert result["objective"] == 8289
    assert result["verification_status"] == "exact"
