"""Exact checker, task programs, and runner tests for T091-C01."""
import ast
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t091.check import PARAMETERS, validate
from tasks.t091.human import run_code as human_run
from tasks.t091.init_program import run_code as init_run
from tasks.t091.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {"id": "T091-C01", "parameters": PARAMETERS, "direction": "minimize", "human_reference": 4096}


def test_human_and_reference_bch_witness_recompute_exactly():
    witness = human_run()
    saved = json.loads((TASK_DIR / "data/human/bch_dual_oa4096.json").read_text())
    assert witness == reference_run() == saved
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == result["objective_value"] == 4096
    assert result["verification_status"] == "exact"
    assert result["details"]["balanced_parity_checks"] == 637392


def test_random_greedy_seed_is_valid_and_distinct_from_the_bch_comparator():
    witness = init_run()
    assert len(witness["rows"]) == 16384
    assert len(set(witness["rows"])) == 16384
    assert validate(witness, CONFIG)["objective"] == 16384


def test_repeated_rows_are_allowed_when_all_projections_remain_uniform():
    witness = reference_run()
    doubled = {"rows": [row for row in witness["rows"] for _ in range(2)]}
    assert len(set(doubled["rows"])) == 4096
    assert validate(doubled, CONFIG)["objective"] == 8192


def test_single_bit_damage_breaks_strength_four():
    witness = copy.deepcopy(reference_run())
    witness["rows"][0] ^= 1
    with pytest.raises(ValueError, match="unbalanced parity"):
        validate(witness, CONFIG)


def test_duplicate_columns_break_orthogonality():
    witness = copy.deepcopy(reference_run())
    witness["rows"] = [(row & ~2) | ((row & 1) << 1) for row in witness["rows"]]
    with pytest.raises(ValueError, match="unbalanced parity"):
        validate(witness, CONFIG)


@pytest.mark.parametrize("bad", [
    None, [], {}, {"rows": []}, {"rows": [0] * 2016}, {"rows": [0] * 2032},
    {"rows": [0] * 2048 + [0]},
    {"rows": [0] * 2032 + [True] * (4096 - 2032)},
    {"rows": [0] * 4095 + [1.0]},
    {"rows": [0] * 4095 + [-1]},
    {"rows": [0] * 4095 + [1 << 63]},
])
def test_malformed_or_boundary_solutions_are_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


@pytest.mark.parametrize("bad_config", [None, [], {}, {"id": "T091-C02", "parameters": PARAMETERS}])
def test_missing_or_unknown_configuration_is_rejected(bad_config):
    with pytest.raises(ValueError, match="configuration"):
        validate({"rows": [0] * 4096}, bad_config)


def test_configuration_parameters_are_exact_and_type_checked():
    for params in ({**PARAMETERS, "columns": 62}, {**PARAMETERS, "strength": True}):
        with pytest.raises(ValueError, match="configuration"):
            validate({"rows": [0] * 4096}, {**CONFIG, "parameters": params})


def test_claimed_score_fields_do_not_change_recomputed_result():
    witness = reference_run()
    expected = validate(witness, CONFIG)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", float("inf"))):
        altered = copy.deepcopy(witness)
        altered[key] = value
        assert validate(altered, CONFIG) == expected


def test_all_five_run_code_entries_return_valid_arrays(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T091-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    from tasks.t091.baseline import run_code as baseline_run
    from tasks.t091.evolution import run_code as evolution_run
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    results = [validate(w, CONFIG, strict=True) for w in outputs]
    assert [r["objective"] for r in results] == [16384, 8192, 8192, 4096, 4096]
    assert outputs[1]["search_metadata"]["proposals_evaluated"] == 12
    assert outputs[2]["search_metadata"]["proposals_evaluated"] == 16
    assert outputs[1]["search_metadata"]["seed_dimension"] == 13
    assert outputs[1]["search_metadata"]["seed_rows"] == 8192
    assert not outputs[1]["search_metadata"]["comparison_data_read"]
    assert not outputs[2]["search_metadata"]["comparison_data_read"]


def test_search_is_reproducible_and_has_no_reference_imports(monkeypatch):
    from tasks.t091.baseline import run_code as baseline_run
    monkeypatch.setenv("MATHBENCH_SEED", "81")
    assert baseline_run() == baseline_run()
    for filename in ("init_program.py", "baseline.py", "evolution.py", "search_core.py"):
        tree = ast.parse((TASK_DIR / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert "human" not in (node.module or "") and "reference" not in (node.module or "")
            elif isinstance(node, ast.Import):
                assert all("human" not in x.name and "reference" not in x.name for x in node.names)


def test_cold_seed_runs_without_task_package_imports(tmp_path):
    source = (TASK_DIR / "init_program.py").read_text()
    imports = [n for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert len(imports) == 2 and all(isinstance(node, ast.Import) for node in imports)
    assert {alias.name for node in imports for alias in node.names} <= {"os", "random"}
    (tmp_path / "init_program.py").write_text(source)
    env = {"PATH": os.environ.get("PATH", ""), "MATHBENCH_CONFIG_ID": "T091-C01"}
    code = "import json,runpy;print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    result = subprocess.run([sys.executable, "-c", code], cwd=tmp_path, env=env,
                            check=True, capture_output=True, text=True, timeout=5)
    out = json.loads(result.stdout)
    assert len(out["rows"]) == 16384 and len(set(out["rows"])) == 16384


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T091 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T091 worker failure')"], env, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time;time.sleep(2)"], env, 0.1)


def test_evaluator_with_temporary_registry_patch(monkeypatch, tmp_path):
    import mathbench.evaluate as evaluate_module
    from tasks.t091.evaluator import evaluate
    monkeypatch.setattr(evaluate_module, "load_config", lambda task_id, config_id=None: CONFIG)
    monkeypatch.setattr(evaluate_module, "task_path", lambda task_id: TASK_DIR)
    result = evaluate(TASK_DIR / "reference.py", "T091-C01", strict=True, seed=0,
                      generation_timeout=20, verification_timeout=40, output_dir=tmp_path)
    assert result["validity"] == 1.0
    assert result["objective"] == 4096
    assert result["verification_status"] == "exact"
