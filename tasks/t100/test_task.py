import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t100.baseline import run_code as baseline_run
from tasks.t100.check import CONFIG_ID, PARAMETERS, validate
from tasks.t100.evaluator import evaluate as task_evaluate
from tasks.t100.evolution import run_code as evolution_run
from tasks.t100.human import build_human_graph, run_code as human_run
from tasks.t100.init_program import run_code as init_run
from tasks.t100.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {
    "id": CONFIG_ID,
    "parameters": PARAMETERS,
    "direction": "minimize",
    "human_reference": 1817,
}


def _validate(graph, config=CONFIG):
    return validate(graph, config)


def _trace_cubes(graph):
    adjacency = [0] * 50
    for left, right in graph["edges"]:
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    trace = 0
    for left in range(50):
        for right in range(50):
            if adjacency[left] & (1 << right):
                trace += (adjacency[left] & adjacency[right]).bit_count()
    assert trace % 6 == 0
    return trace // 6


def test_all_five_program_entries(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    monkeypatch.setenv("T100_SEARCH_STEPS", "1")
    monkeypatch.setenv("T100_EVOLVE_STEPS", "1")
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for graph in outputs:
        result = _validate(graph)
        assert result["verification_status"] == "exact"
        assert result["objective"] == _trace_cubes(graph)
        assert result["details"]["edge_count"] == 700
    assert _validate(human_run())["objective"] == 1817
    assert _validate(reference_run())["objective"] == 1817


def test_public_witness_and_reconstruction_are_pinned():
    witness = TASK / "data/reference/hstar_50_700.json"
    metadata = json.loads((TASK / "sota.json").read_text(encoding="utf-8"))
    entry = metadata["configurations"][CONFIG_ID]
    assert hashlib.sha256(witness.read_bytes()).hexdigest() == entry["witness_sha256"]
    saved = json.loads(witness.read_text(encoding="utf-8"))
    assert saved == build_human_graph()
    assert _validate(saved)["objective"] == 1817
    assert len(saved["edges"]) == 700


@pytest.mark.parametrize(
    "config",
    [
        {**CONFIG, "id": "T100-C02"},
        {**CONFIG, "parameters": {**PARAMETERS, "edges": 700.0}},
        {**CONFIG, "parameters": {**PARAMETERS, "vertices": True}},
        {**CONFIG, "parameters": {**PARAMETERS, "extra": 1}},
        {**CONFIG, "direction": "maximize"},
        {**CONFIG, "direction": True},
        {**CONFIG, "human_reference": 1817.0},
        {**CONFIG, "human_reference": True},
        {**CONFIG, "extra": 1},
        {"id": CONFIG_ID, "parameters": PARAMETERS},
    ],
)
def test_config_is_frozen_with_strict_types(config):
    with pytest.raises(ValueError):
        _validate(build_human_graph(), config)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda graph: graph.update(vertices=49),
        lambda graph: graph.update(vertices=True),
        lambda graph: graph.update(edges=graph["edges"][:-1]),
        lambda graph: graph["edges"].__setitem__(0, [0, 0]),
        lambda graph: graph["edges"].__setitem__(0, [False, 1]),
        lambda graph: graph["edges"].__setitem__(0, [0.0, 1]),
        lambda graph: graph["edges"].__setitem__(0, [0, 50]),
        lambda graph: graph["edges"].__setitem__(0, [float("nan"), 1]),
        lambda graph: graph["edges"].__setitem__(0, graph["edges"][1]),
    ],
)
def test_invalid_graphs_are_rejected(mutate):
    graph = build_human_graph()
    mutate(graph)
    with pytest.raises(ValueError):
        _validate(graph)


def test_claimed_scores_and_objective_are_whole_result_invariant():
    graph = build_human_graph()
    expected = _validate(graph)
    for key, value in (
        ("objective", -1),
        ("score", float("nan")),
        ("claimed_score", "999999999"),
    ):
        assert _validate({**graph, key: value}) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_search_determinism_and_reference_isolation(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "33")
    monkeypatch.setenv("T100_SEARCH_STEPS", "3")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first, second = baseline_run(), baseline_run()
    assert first == second
    assert first["search"]["comparison_data_read"] is False
    _validate(first)


def test_runner_error_and_timeout_without_task_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T100 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T100 worker failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)


def test_public_evaluate_with_full_config_and_temporary_registry(monkeypatch):
    import mathbench.evaluate as shared_runner

    task_config = json.loads((TASK / "task.json").read_text(encoding="utf-8"))["configurations"][0]
    monkeypatch.setattr(shared_runner, "load_config", lambda task_id, config_id=None: task_config)
    monkeypatch.setattr(shared_runner, "task_path", lambda task_id: TASK)
    result = task_evaluate(
        TASK / "reference.py",
        CONFIG_ID,
        strict=True,
        generation_timeout=10,
        verification_timeout=10,
    )
    assert result["validity"] == 1.0
    assert result["objective"] == 1817
    assert result["objective_value"] == 1817
    assert result["combined_score"] == 1.0
    assert result["verification_status"] == "exact"
