"""Exact tests for T075's K4^- free three-uniform hypergraphs."""
import ast
import copy
import json
import os
import subprocess
import sys
from math import comb
from itertools import combinations
from pathlib import Path

import pytest

from tasks.t075.baseline import run_code as baseline_run
from tasks.t075.check import PARAMETERS, validate
from tasks.t075.evolution import run_code as evolution_run
from tasks.t075.human import run_code as human_run
from tasks.t075.init_program import run_code as init_run
from tasks.t075.reference import run_code as reference_run

TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T075-C01",
    "parameters": PARAMETERS,
    "direction": "maximize",
    "human_reference": 2220,
}


def test_h6_reference_is_rebuilt_and_exactly_verified():
    human = human_run()
    saved_human = json.loads((TASK_DIR / "data/human/h6_iterated_blowup_n36.json").read_text())
    reference = reference_run()
    assert human == saved_human == reference
    result = validate(human, CONFIG, strict=True)
    assert result["objective"] == 2220
    assert result["details"]["four_vertex_sets_checked"] == 58905
    assert result["details"]["maximum_triples_on_any_four_set"] == 2


def test_h6_link_graphs_are_five_cycles():
    template = json.loads((TASK_DIR / "data/source/h6_template.json").read_text())
    edges = [tuple(e) for e in template["edges_zero_based"]]
    for vertex in range(6):
        link = {}
        for edge in edges:
            if vertex in edge:
                other = tuple(x for x in edge if x != vertex)
                link.setdefault(other[0], set()).add(other[1])
                link.setdefault(other[1], set()).add(other[0])
        assert len(link) == 5
        assert all(len(neighbors) == 2 for neighbors in link.values())
        seen = set()
        pending = [next(iter(link))]
        while pending:
            current = pending.pop()
            if current not in seen:
                seen.add(current)
                pending.extend(link[current] - seen)
        assert len(seen) == 5


def test_saved_own_search_result_recomputes_objective():
    saved = json.loads((TASK_DIR / "best/T075-C01/solution.json").read_text())
    saved_result = json.loads((TASK_DIR / "best/T075-C01/result.json").read_text())
    provenance = json.loads((TASK_DIR / "best/T075-C01/provenance.json").read_text())
    result = validate(saved, CONFIG, strict=True)
    expected = provenance["generation_record"]["objective"]
    assert expected == saved_result["objective"]
    assert result["objective"] == expected
    assert saved["search_metadata"]["best_edge_count"] == expected
    assert provenance["program"] == "evolution.py"


def test_empty_hypergraph_is_valid_and_bounds_are_recomputed():
    result = validate({"edges": []}, CONFIG, strict=True)
    assert result["objective"] == 0
    assert result["details"]["double_counting_upper_bound"] == 3570
    assert result["details"]["four_vertex_sets_checked"] == 58905


def test_direct_double_counting_bound_and_human_count():
    witness = human_run()
    assert len(witness["edges"]) == 2220
    assert 33 * 3570 == 2 * comb(36, 4)
    assert 3570 == comb(36, 3) // 2


def test_three_edges_on_four_vertices_are_rejected():
    witness = human_run()
    edges = {tuple(e) for e in witness["edges"]}
    for quad in combinations(range(36), 4):
        triples = list(combinations(quad, 3))
        if sum(t in edges for t in triples) == 2:
            missing = next(t for t in triples if t not in edges)
            bad = copy.deepcopy(witness)
            bad["edges"].append(list(missing))
            with pytest.raises(ValueError, match="K4"):
                validate(bad, CONFIG)
            return
    raise AssertionError("reference construction had no four-set with occupancy two")


@pytest.mark.parametrize("bad_edge", [
    None, True, 1.0, float("nan"), float("inf"), [], [0, 1], [0, 1, 36],
    [-1, 1, 2], [0, 0, 2], [0, 1, False], [0, 1, 2.0],
])
def test_malformed_edges_are_rejected(bad_edge):
    with pytest.raises(ValueError):
        validate({"edges": [bad_edge]}, CONFIG)


def test_unordered_duplicate_edges_are_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        validate({"edges": [[0, 1, 2], [2, 0, 1]]}, CONFIG)


def test_claimed_scores_do_not_change_the_full_result():
    candidate = reference_run()
    expected = validate(candidate, CONFIG)
    changed = {
        **candidate,
        "objective": float("nan"),
        "score": float("inf"),
        "claimed_score": -1,
    }
    assert validate(changed, CONFIG) == expected


@pytest.mark.parametrize("changes", [
    {"n": 35},
    {"uniformity": 2},
    {"forbidden_semantics": "induced"},
    {"constraint": "every 4-set spans at most 3 triples"},
    {"extra": 1},
])
def test_incorrect_configuration_parameters_are_rejected(changes):
    with pytest.raises(ValueError, match="unsupported"):
        validate({"edges": []}, {**CONFIG, "parameters": {**PARAMETERS, **changes}})


@pytest.mark.parametrize("bad_config", [None, [], "T075-C01", {}, {"id": "T075-C02", "parameters": PARAMETERS}])
def test_missing_nonobject_and_unknown_configurations_are_rejected(bad_config):
    with pytest.raises(ValueError, match="unsupported"):
        validate({"edges": []}, bad_config)


def test_all_five_program_entries_return_valid_hypergraphs(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T075-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    for run in (init_run, baseline_run, evolution_run, human_run, reference_run):
        assert validate(run(), CONFIG)["verification_status"] == "exact"


def test_search_is_seeded_and_reports_actual_trials(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T075-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "5")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    baseline = baseline_run()
    assert baseline == baseline_run()
    assert baseline["search_metadata"]["iterations"] == 5
    assert baseline["search_metadata"]["comparison_data_read"] is False
    evolution = evolution_run()
    assert evolution == evolution_run()
    assert evolution["search_metadata"]["iterations"] == 8
    assert evolution["search_metadata"]["comparison_data_read"] is False


def test_init_program_is_self_contained_and_simple(tmp_path):
    source = (TASK_DIR / "init_program.py").read_text()
    tree = ast.parse(source)
    imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    assert len(imports) == 1 and isinstance(imports[0], ast.Import)
    assert [alias.name for alias in imports[0].names] == ["os"]
    copied = tmp_path / "init_program.py"
    copied.write_text(source)
    env = {"PATH": os.environ.get("PATH", ""), "MATHBENCH_CONFIG_ID": "T075-C01", "MATHBENCH_SEED": "0"}
    command = "import json, runpy; print(json.dumps(runpy.run_path('init_program.py')['run_code']()))"
    completed = subprocess.run([sys.executable, "-c", command], cwd=tmp_path, env=env,
                               check=True, capture_output=True, text=True, timeout=5)
    assert json.loads(completed.stdout) == {"edges": []}


def test_search_code_does_not_import_human_or_reference_programs():
    for filename in ("baseline.py", "evolution.py", "greedy.py", "init_program.py"):
        tree = ast.parse((TASK_DIR / filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert "human" not in module and "reference" not in module
            elif isinstance(node, ast.Import):
                assert all("human" not in a.name and "reference" not in a.name for a in node.names)


def test_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)


def test_evaluator_uses_temporary_registry_patch(monkeypatch, tmp_path):
    import mathbench.evaluate as evaluate_module
    from tasks.t075.evaluator import evaluate

    monkeypatch.setattr(evaluate_module, "load_config", lambda task_id, config_id=None: CONFIG)
    monkeypatch.setattr(evaluate_module, "task_path", lambda task_id: TASK_DIR)
    result = evaluate(TASK_DIR / "reference.py", "T075-C01", strict=True, seed=0,
                      generation_timeout=20, verification_timeout=20, output_dir=tmp_path)
    assert result["validity"] == 1.0
    assert result["objective"] == 2220
    assert result["verification_status"] == "exact"
