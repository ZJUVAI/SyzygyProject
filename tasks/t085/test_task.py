"""Exact checker and runner tests for T085-C01."""
import ast
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t085.check import PARAMETERS, validate
from tasks.t085.human import run_code as human_run
from tasks.t085.init_program import run_code as init_run
from tasks.t085.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {"id": "T085-C01", "parameters": PARAMETERS, "direction": "maximize", "human_reference": 3.5}


def test_human_and_reference_patch_exactly_cover_radius_seven_halves():
    witness = human_run()
    saved = json.loads((TASK_DIR / "data/human/kershner_triangular_patch21.json").read_text())
    assert witness == saved == reference_run()
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == "7/2"
    assert result["verification_status"] == "exact"
    assert result["details"]["critical_points_checked"] == 1463


def test_seed_boundary_and_repeated_centers_are_valid():
    seed = init_run()
    assert len(seed["centers"]) == 21 and len({tuple(c) for c in seed["centers"]}) == 1
    assert validate(seed, CONFIG, strict=True)["objective"] == "1"


def test_noncovering_radius_is_rejected_by_full_domain_certificate():
    broken = copy.deepcopy(reference_run())
    broken["radius"] = "4"
    with pytest.raises(ValueError, match="full target disk"):
        validate(broken, CONFIG)


def test_moving_an_essential_center_breaks_coverage():
    broken = copy.deepcopy(reference_run())
    broken["centers"][0] = ["100", "100"]
    with pytest.raises(ValueError, match="full target disk"):
        validate(broken, CONFIG)


@pytest.mark.parametrize("bad", [
    None, [], {"radius": "1", "centers": []},
    {"radius": "nan", "centers": init_run()["centers"]},
    {"radius": float("inf"), "centers": init_run()["centers"]},
    {"radius": True, "centers": init_run()["centers"]},
])
def test_malformed_solution_is_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


@pytest.mark.parametrize("bad_center", [None, [], [1], [True, 0], [float("nan"), 0], ["0", "1/0"]])
def test_malformed_centers_are_rejected(bad_center):
    witness = init_run()
    witness["centers"][0] = bad_center
    with pytest.raises(ValueError):
        validate(witness, CONFIG)


def test_rational_parser_has_no_decimal_digit_cap():
    witness = init_run()
    witness["centers"][0][0] = "0/" + "9" * 5000
    assert validate(witness, CONFIG)["objective"] == "1"


@pytest.mark.parametrize("bad_config", [None, [], {}, {"id": "T085-C02", "parameters": PARAMETERS}])
def test_unknown_or_missing_config_is_rejected(bad_config):
    with pytest.raises(ValueError, match="configuration"):
        validate(init_run(), bad_config)


def test_wrong_parameters_are_rejected_including_bool_aliases():
    for params in ({**PARAMETERS, "circle_count": 20}, {**PARAMETERS, "covering_circle_radius": True}):
        with pytest.raises(ValueError, match="configuration"):
            validate(init_run(), {**CONFIG, "parameters": params})


def test_claimed_scores_never_change_validation_result():
    witness = human_run()
    expected = validate(witness, CONFIG)
    for key, value in (("objective", -5), ("score", float("nan")), ("claimed_score", float("inf"))):
        assert validate({**witness, key: value}, CONFIG) == expected


def test_all_five_run_code_entries_return_valid_objects(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T085-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    from tasks.t085.baseline import run_code as baseline_run
    from tasks.t085.evolution import run_code as evolution_run
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    results = [validate(value, CONFIG, strict=True) for value in outputs]
    assert results[0]["objective"] == results[1]["objective"] == results[2]["objective"] == "1"
    assert results[3]["objective"] == results[4]["objective"] == "7/2"
    assert outputs[1]["search_metadata"]["candidate_count"] == 12
    assert outputs[2]["search_metadata"]["candidate_count"] == 20
    assert not outputs[1]["search_metadata"]["comparison_data_read"]
    assert not outputs[2]["search_metadata"]["comparison_data_read"]


def test_search_is_reproducible_and_honors_zero_time_cutoff(monkeypatch):
    from tasks.t085.baseline import run_code as baseline_run
    monkeypatch.setenv("MATHBENCH_SEED", "7")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    assert baseline_run() == baseline_run()
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    assert baseline_run()["search_metadata"]["candidate_count"] == 0


def test_search_and_initializer_do_not_import_comparison_assets():
    for filename in ("init_program.py", "baseline.py", "evolution.py", "search_core.py"):
        tree = ast.parse((TASK_DIR / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert "human" not in (node.module or "") and "reference" not in (node.module or "")
            elif isinstance(node, ast.Import):
                assert all("human" not in x.name and "reference" not in x.name for x in node.names)


def test_cold_initializer_runs_without_task_package(tmp_path):
    source = (TASK_DIR / "init_program.py").read_text()
    imports = [n for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert len(imports) == 1 and isinstance(imports[0], ast.Import)
    (tmp_path / "init_program.py").write_text(source)
    env = {"PATH": os.environ.get("PATH", ""), "MATHBENCH_CONFIG_ID": "T085-C01"}
    cmd = "import json,runpy;print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    result = subprocess.run([sys.executable, "-c", cmd], cwd=tmp_path, env=env,
                            check=True, capture_output=True, text=True, timeout=5)
    assert json.loads(result.stdout) == init_run()


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T085 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T085 worker failure')"], env, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time;time.sleep(2)"], env, 0.1)


def test_evaluator_with_temporary_registry_patch(monkeypatch, tmp_path):
    import mathbench.evaluate as evaluate_module
    from tasks.t085.evaluator import evaluate
    monkeypatch.setattr(evaluate_module, "load_config", lambda task_id, config_id=None: CONFIG)
    monkeypatch.setattr(evaluate_module, "task_path", lambda task_id: TASK_DIR)
    result = evaluate(TASK_DIR / "reference.py", "T085-C01", strict=True, seed=0,
                      generation_timeout=20, verification_timeout=20, output_dir=tmp_path)
    assert result["validity"] == 1.0
    assert result["objective"] == "7/2"
    assert result["verification_status"] == "exact"
