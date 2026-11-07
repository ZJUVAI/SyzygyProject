"""Exact checker, program, and runner tests for T083-C01."""
import ast
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t083.check import PARAMETERS, Q, validate
from tasks.t083.human import run_code as human_run
from tasks.t083.init_program import run_code as init_run
from tasks.t083.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {"id": "T083-C01", "parameters": PARAMETERS, "direction": "minimize", "human_reference": 1.577350269189626}


def test_ordered_field_sign_and_arithmetic_are_exact():
    assert Q(0, 1).sign() > 0
    assert Q(1, -1).sign() < 0
    assert Q(2, -1).sign() > 0
    assert Q(0, 1) * Q(0, 1) == 3
    assert (Q.parse(["1", "1/3"]) - Q.parse("1577350269189625/1000000000000000")).sign() > 0


def test_human_and_reference_recompute_exact_side():
    for witness in (human_run(), reference_run(), json.loads((TASK_DIR / "data/reference/friedman4_reconstructed.json").read_text())):
        result = validate(witness, CONFIG, strict=True)
        assert result["objective"] == "[1,1/3]"
        assert result["verification_status"] == "certified"
        low, high = map(lambda s: Q.parse(s), result["details"]["objective_interval"])
        assert low <= Q.parse(["1", "1/3"]) <= high
        assert Q.parse(result["objective_value"]) == high
        assert result["details"]["triangle_pairs_checked"] == 6


def test_source_reconstruction_matches_fixed_program_and_score():
    archived = json.loads((TASK_DIR / "data/source/friedman4_reconstructed_source.json").read_text())
    assert archived["container_side"] == "sqrt(3)/3 + 1"
    assert len(archived["triangles"]) == 4
    assert validate(reference_run(), CONFIG)["objective"] == "[1,1/3]"


def test_simple_seed_is_valid():
    result = validate(init_run(), CONFIG, strict=True)
    assert result["objective"] == "[2,0]"


def test_exact_rationals_have_no_decimal_digit_cap():
    witness = init_run()
    witness["triangles"][0]["anchor"][0] = ["0/" + "9" * 5000, "0"]
    assert validate(witness, CONFIG)["objective"] == "[2,0]"


@pytest.mark.parametrize("bad", [
    None, [], {"side": ["2", "0"], "triangles": []},
    {"side": [float("nan"), "0"], "triangles": reference_run()["triangles"]},
    {"side": [True, "0"], "triangles": reference_run()["triangles"]},
])
def test_malformed_solution_is_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


@pytest.mark.parametrize("bad_config", [None, [], {}, {"id": "T083-C02", "parameters": PARAMETERS}])
def test_missing_and_unknown_configuration_is_rejected(bad_config):
    with pytest.raises(ValueError, match="configuration"):
        validate(reference_run(), bad_config)


def test_wrong_fixed_parameters_are_rejected():
    for parameters in ({**PARAMETERS, "triangle_count": 5}, {**PARAMETERS, "triangle_side": True}):
        bad = {**CONFIG, "parameters": parameters}
        with pytest.raises(ValueError, match="configuration"):
            validate(reference_run(), bad)


@pytest.mark.parametrize("bad_direction", [[True, 0], [1.0, 0.0], [2, 0], ["nan", "0"], [0, 0]])
def test_nonexact_or_nonunit_directions_are_rejected(bad_direction):
    broken = copy.deepcopy(reference_run())
    broken["triangles"][0]["direction"] = bad_direction
    with pytest.raises(ValueError):
        validate(broken, CONFIG)


def test_boundary_violation_is_rejected():
    broken = copy.deepcopy(reference_run())
    broken["triangles"][0]["anchor"][0] = ["-1", "0"]
    with pytest.raises(ValueError, match="outside"):
        validate(broken, CONFIG)


def test_overlapping_and_duplicate_triangle_are_rejected():
    witness = reference_run()
    duplicate = copy.deepcopy(witness)
    duplicate["triangles"][1] = copy.deepcopy(duplicate["triangles"][0])
    with pytest.raises(ValueError, match="overlap"):
        validate(duplicate, CONFIG)
    overlap = copy.deepcopy(witness)
    overlap["triangles"][0]["anchor"] = [["1/2", "0"], ["1", "0"]]
    with pytest.raises(ValueError, match="overlap"):
        validate(overlap, CONFIG)


def test_claimed_scores_do_not_change_full_validation_result():
    witness = reference_run()
    expected = validate(witness, CONFIG)
    for key, value in (("objective", -99), ("score", float("nan")), ("claimed_score", float("inf"))):
        altered = {**witness, key: value}
        assert validate(altered, CONFIG) == expected


def test_all_five_programs_return_valid_objects(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T083-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    from tasks.t083.baseline import run_code as baseline_run
    from tasks.t083.evolution import run_code as evolution_run

    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    results = [validate(item, CONFIG, strict=True) for item in outputs]
    assert [r["objective"] for r in results] == ["[2,0]", "[2,0]", "[2,0]", "[1,1/3]", "[1,1/3]"]
    assert outputs[1]["search_metadata"]["candidate_count"] == 80
    assert outputs[2]["search_metadata"]["candidate_count"] == 160
    assert outputs[1]["search_metadata"]["comparison_data_read"] is False
    assert outputs[2]["search_metadata"]["comparison_data_read"] is False


def test_searches_are_repeatable_and_honor_explicit_zero_cutoff(monkeypatch):
    from tasks.t083.baseline import run_code as baseline_run
    monkeypatch.setenv("MATHBENCH_SEED", "42")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    assert baseline_run() == baseline_run()
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    assert baseline_run()["search_metadata"]["candidate_count"] == 0


def test_search_and_seed_sources_do_not_import_comparison_assets():
    for filename in ("init_program.py", "baseline.py", "evolution.py", "search_core.py"):
        tree = ast.parse((TASK_DIR / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert "human" not in (node.module or "") and "reference" not in (node.module or "")
            elif isinstance(node, ast.Import):
                assert all("human" not in item.name and "reference" not in item.name for item in node.names)


def test_cold_initializer_runs_without_task_package(tmp_path):
    source = (TASK_DIR / "init_program.py").read_text()
    tree = ast.parse(source)
    imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert len(imports) == 1 and isinstance(imports[0], ast.Import)
    module = tmp_path / "init_program.py"
    module.write_text(source)
    env = {"PATH": os.environ.get("PATH", ""), "MATHBENCH_CONFIG_ID": "T083-C01"}
    cmd = "import json,runpy;print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    completed = subprocess.run([sys.executable, "-c", cmd], cwd=tmp_path, env=env,
                               check=True, text=True, capture_output=True, timeout=5)
    assert json.loads(completed.stdout) == init_run()


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T083 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T083 worker failure')"], env, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time;time.sleep(2)"], env, 0.1)


def test_evaluator_with_temporary_registry_patch(monkeypatch, tmp_path):
    import mathbench.evaluate as evaluate_module
    from tasks.t083.evaluator import evaluate
    monkeypatch.setattr(evaluate_module, "load_config", lambda task_id, config_id=None: CONFIG)
    monkeypatch.setattr(evaluate_module, "task_path", lambda task_id: TASK_DIR)
    result = evaluate(TASK_DIR / "reference.py", "T083-C01", strict=True, seed=0,
                      generation_timeout=20, verification_timeout=20, output_dir=tmp_path)
    assert result["validity"] == 1.0
    assert result["objective"] == "[1,1/3]"
    assert result["verification_status"] == "certified"
