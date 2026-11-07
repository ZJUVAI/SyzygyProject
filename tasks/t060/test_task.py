"""Task-local tests for exact M61 integer-complexity checking."""
import hashlib
import ast
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tasks.t060.baseline import run_code as baseline_run
from tasks.t060.check import TARGET, _selfridge_max, validate
from tasks.t060.evolution import run_code as evolution_run
from tasks.t060.human import run_code as human_run
from tasks.t060.init_program import run_code as seed_run
from tasks.t060.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T060-C01",
    "parameters": {"target": "2^61-1", "target_value": str(TARGET)},
    "direction": "minimize",
    "human_reference": 153,
}


def test_exact_selfridge_bound_uses_integer_arithmetic():
    assert _selfridge_max(115) == 1801135623563989452
    assert _selfridge_max(115) < TARGET < _selfridge_max(116)


def test_human_base3_expression_rebuilds_saved_witness():
    generated = human_run()
    saved = json.loads((TASK_DIR / "data/human/human_base3_expression.json").read_text())
    result = validate(generated, CONFIG, strict=True)
    assert generated == saved
    assert result["objective"] == 153
    assert result["verification_status"] == "exact"


def test_public_127_witness_exactly_replays_and_hash_matches():
    witness = reference_run()
    path = TASK_DIR / "data/reference/public_127_expression.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "946a56e064e60422f49c98aeeb0ceae0a99c22d5070318a7b84fcbca28699449"
    )
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 127
    assert result["details"]["expression_value"] == str(TARGET)


def test_all_five_program_entries_return_valid_expressions(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T060-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    for run in (seed_run, baseline_run, human_run, reference_run, evolution_run):
        assert validate(run(), CONFIG)["verification_status"] == "exact"


def test_binary_seed_is_self_contained_when_exported(tmp_path):
    seed_copy = tmp_path / "init_program.py"
    shutil.copy(TASK_DIR / "init_program.py", seed_copy)
    environment = {
        "PATH": os.environ.get("PATH", ""),
        "MATHBENCH_CONFIG_ID": "T060-C01",
        "MATHBENCH_SEED": "0",
    }
    code = "import json, runpy; print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    completed = subprocess.run(
        [sys.executable, "-c", code], cwd=tmp_path, env=environment,
        check=True, capture_output=True, text=True, timeout=10,
    )
    assert validate(json.loads(completed.stdout), CONFIG)["objective"] == 181


def test_baseline_and_evolution_are_seeded_and_report_actual_iterations(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "5")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first = baseline_run()
    assert first == baseline_run()
    assert first["search_metadata"]["iterations"] == 15
    assert first["search_metadata"]["reference_data_read"] is False
    evolved = evolution_run()
    assert evolved == evolution_run()
    assert evolved["search_metadata"]["seed"] == 5
    assert evolved["search_metadata"]["iterations"] == 1000
    assert evolved["search_metadata"]["reference_data_read"] is False
    assert evolved["search_metadata"]["budget"]["mode"] == "fixed_iteration_count"


def test_zero_second_budget_returns_valid_seed(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    result = evolution_run()
    assert result["search_metadata"]["iterations"] == 0
    assert validate(result, CONFIG)["verification_status"] == "exact"
    assert result["search_metadata"]["budget"]["mode"] == "wall_clock_cutoff"


def test_claimed_scores_are_ignored_even_when_nonfinite():
    candidate = reference_run()
    expected = validate(candidate, CONFIG)
    changed = {
        **candidate,
        "objective": float("nan"),
        "score": float("inf"),
        "claimed_score": -1,
        "claimed_objective": True,
        "metadata": [None, False],
    }
    assert validate(changed, CONFIG) == expected


@pytest.mark.parametrize("bad", [
    None, True, 1, 1.0, float("nan"), float("inf"), [], {},
    "", "2", "1-1", "1/1", "1^1", "x", "1+", "+1", "()",
    "1 1", "1\t+1", "1\n+1", "1(1)", "(1+1", "1+1)", "(1+)1", "1**1",
])
def test_invalid_expressions_are_rejected(bad):
    with pytest.raises(ValueError):
        validate({"expression": bad}, CONFIG)


def test_wrong_value_and_wrong_configuration_are_rejected():
    with pytest.raises(ValueError, match="does not evaluate"):
        validate({"expression": "1+1"}, CONFIG)
    with pytest.raises(ValueError, match="configuration"):
        validate(reference_run(), {**CONFIG, "parameters": {"target": "2^61-2"}})


def test_expression_tree_repetition_is_counted_as_separate_leaves():
    # The same text is repeated, but the expression is a tree and evaluates to 4.
    from tasks.t060.check import _parse

    assert _parse("(1+1)*(1+1)") == (4, 4)


def test_search_program_imports_do_not_reach_comparison_programs():
    for filename in ("baseline.py", "evolution.py", "init_program.py"):
        tree = ast.parse((TASK_DIR / filename).read_text(encoding="utf-8"))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
            elif isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
        assert not any("t060.human" in name or "t060.reference" in name for name in imported)


def test_expression_length_limit_and_deep_parentheses_are_safe():
    from tasks.t060.check import MAX_EXPRESSION_LENGTH, _parse

    with pytest.raises(ValueError, match="too long"):
        _parse("1" + " " * MAX_EXPRESSION_LENGTH)
    assert _parse("(" * 3000 + "1" + ")" * 3000) == (1, 1)


def test_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
