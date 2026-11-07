"""Exact moment checker and task runner tests for T092-C01."""
import ast
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t092.check import EXPONENTS, PARAMETERS, validate
from tasks.t092.human import run_code as human_run
from tasks.t092.init_program import run_code as init_run
from tasks.t092.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {"id": "T092-C01", "parameters": PARAMETERS, "direction": "maximize", "human_reference": 1.5315529249613}


def test_human_and_reference_rebuild_highest_weight_harmonic_exactly():
    witness = human_run()
    saved = json.loads((TASK_DIR / "data/reference/highest_weight_degree20.json").read_text())
    assert witness == reference_run() == saved
    result = validate(witness, CONFIG, strict=True)
    assert result["verification_status"] == "certified"
    assert result["details"]["harmonic_laplacian_residual_terms"] == 0
    assert result["details"]["sphere_average_M2"] == "137438953472/1412926920405"
    assert result["details"]["sphere_average_M4"] == "37778931862957161709568/725673658950019191115935"
    assert result["details"]["objective_interval"][0] == result["objective_value"]
    assert float(__import__("fractions").Fraction(result["objective_value"])) >= CONFIG["human_reference"]


def test_zonal_initial_harmonic_is_a_legal_simple_seed():
    witness = init_run()
    result = validate(witness, CONFIG)
    assert len(witness["coefficients"]) == 231
    assert result["verification_status"] == "certified"
    assert result["details"]["harmonic_laplacian_residual_terms"] == 0


@pytest.mark.parametrize("bad", [
    None, [], {}, {"coefficients": []},
    {"coefficients": [0] * 230}, {"coefficients": [0] * 232},
    {"coefficients": [0] * 231},
    {"coefficients": [True] + [0] * 230},
    {"coefficients": [float("nan")] + [0] * 230},
    {"coefficients": [float("inf")] + [0] * 230},
    {"coefficients": ["1/0"] + [0] * 230},
])
def test_malformed_zero_or_nonfinite_inputs_are_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)


def test_nonharmonic_polynomial_is_rejected_exactly():
    broken = copy.deepcopy(human_run())
    broken["coefficients"][EXPONENTS.index((20, 0, 0))] += 1
    with pytest.raises(ValueError, match="not harmonic"):
        validate(broken, CONFIG)


@pytest.mark.parametrize("bad_config", [
    None, [], {}, {"id": "T092-C02", "parameters": PARAMETERS},
    {**CONFIG, "direction": "minimize"}, {**CONFIG, "direction": None},
])
def test_missing_or_unknown_config_is_rejected(bad_config):
    with pytest.raises(ValueError, match="configuration"):
        validate(init_run(), bad_config)


def test_parameters_are_matched_exactly_and_type_checked():
    for params in ({**PARAMETERS, "degree": 19}, {**PARAMETERS, "degree": True}):
        with pytest.raises(ValueError, match="configuration"):
            validate(init_run(), {**CONFIG, "parameters": params})


def test_claimed_score_is_ignored_and_scale_invariance_is_exact():
    witness = human_run()
    expected = validate(witness, CONFIG)
    altered = copy.deepcopy(witness)
    altered.update(objective=-1, score=float("nan"), claimed_score=float("inf"))
    assert validate(altered, CONFIG) == expected
    scaled = {"coefficients": [2 * c for c in witness["coefficients"]]}
    scaled_result = validate(scaled, CONFIG)
    assert scaled_result["objective"] == expected["objective"]
    assert scaled_result["details"]["objective_interval"] == expected["details"]["objective_interval"]


def test_coefficients_have_no_fixed_decimal_digit_cap():
    zeros = "0" * 5000
    huge = []
    for value in human_run()["coefficients"]:
        if value == 0:
            huge.append("0")
        else:
            huge.append(("-" if value < 0 else "") + str(abs(value)) + zeros)
    result = validate({"coefficients": huge}, CONFIG)
    assert result["objective"] == validate(human_run(), CONFIG)["objective"]


def test_all_five_run_code_entries_produce_exactly_checkable_harmonics(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T092-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    from tasks.t092.baseline import run_code as baseline_run
    from tasks.t092.evolution import run_code as evolution_run
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    results = [validate(candidate, CONFIG, strict=True) for candidate in outputs]
    assert all(result["verification_status"] == "certified" for result in results)
    assert results[3] == results[4]
    assert outputs[1]["search_metadata"]["proposals_evaluated"] == 16
    assert outputs[2]["search_metadata"]["proposals_evaluated"] == 24
    assert not outputs[1]["search_metadata"]["comparison_data_read"]


def test_search_is_reproducible_and_search_files_do_not_read_comparators(monkeypatch):
    from tasks.t092.baseline import run_code as baseline_run
    monkeypatch.setenv("MATHBENCH_SEED", "712")
    assert baseline_run() == baseline_run()
    for filename in ("init_program.py", "baseline.py", "evolution.py", "search_core.py"):
        tree = ast.parse((TASK_DIR / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert "human" not in (node.module or "") and "reference" not in (node.module or "")
            elif isinstance(node, ast.Import):
                assert all("human" not in x.name and "reference" not in x.name for x in node.names)


def test_cold_initializer_runs_without_task_package_imports(tmp_path):
    source = (TASK_DIR / "init_program.py").read_text()
    imports = [n for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert all((isinstance(n, ast.Import) and all(a.name in {"os", "fractions"} for a in n.names))
               or (isinstance(n, ast.ImportFrom) and n.module == "fractions") for n in imports)
    (tmp_path / "init_program.py").write_text(source)
    env = {"PATH": os.environ.get("PATH", ""), "MATHBENCH_CONFIG_ID": "T092-C01"}
    code = "import json,runpy;print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    result = subprocess.run([sys.executable, "-c", code], cwd=tmp_path, env=env,
                            check=True, capture_output=True, text=True, timeout=5)
    assert len(json.loads(result.stdout)["coefficients"]) == 231


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T092 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T092 worker failure')"], env, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time;time.sleep(2)"], env, 0.1)


def test_evaluator_with_temporary_registry_patch(monkeypatch, tmp_path):
    import mathbench.evaluate as evaluate_module
    from tasks.t092.evaluator import evaluate
    monkeypatch.setattr(evaluate_module, "load_config", lambda task_id, config_id=None: CONFIG)
    monkeypatch.setattr(evaluate_module, "task_path", lambda task_id: TASK_DIR)
    result = evaluate(TASK_DIR / "reference.py", "T092-C01", strict=True, seed=0,
                      generation_timeout=20, verification_timeout=40, output_dir=tmp_path)
    assert result["validity"] == 1.0
    assert result["verification_status"] == "certified"
    assert result["objective"] == validate(reference_run(), CONFIG)["objective"]
