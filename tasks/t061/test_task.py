import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t061.baseline import run_code as baseline_run
from tasks.t061.check import CONFIG_ID, PARAMETERS, _path_endpoint_pairs, validate
from tasks.t061.evolution import run_code as evolution_run
from tasks.t061.human import build_human_graph, run_code as human_run
from tasks.t061.init_program import run_code as init_run
from tasks.t061.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _validate(graph):
    return validate(graph, CONFIG)


def test_all_five_program_entries(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("T061_SEARCH_TRIALS", "1")
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for graph in outputs:
        result = _validate(graph)
        assert result["verification_status"] == "exact"
        assert result["objective"] == len(graph["edges"])
    assert _validate(human_run())["objective"] == 133
    assert _validate(reference_run())["objective"] == 133


def test_human_reference_file_and_source_hash():
    witness = TASK / "data/reference/c6_sat_100_133.json"
    metadata = json.loads((TASK / "sota.json").read_text())
    config_record = metadata["configurations"][CONFIG_ID]
    assert hashlib.sha256(witness.read_bytes()).hexdigest() == config_record["witness_sha256"]
    saved = json.loads(witness.read_text())
    assert saved == build_human_graph()
    verified = _validate(saved)
    assert verified["objective"] == 133
    assert verified["details"]["missing_pairs_checked"] == 4817
    assert verified["details"]["simple_5_path_endpoint_pairs"] == 4817


def test_repeated_vertex_walk_does_not_count_as_simple_five_path():
    adjacency = [0] * 100
    for left, right in ((0, 1), (1, 2), (2, 3)):
        adjacency[left] |= 1 << right
        adjacency[right] |= 1 << left
    repeated_walk = [0, 1, 2, 1, 2, 3]
    assert len(repeated_walk) == 6
    assert len(set(repeated_walk)) < len(repeated_walk)
    assert (0, 3) not in _path_endpoint_pairs(adjacency)


@pytest.mark.parametrize(
    "graph",
    [
        {"vertices": 99, "edges": []},
        {"vertices": True, "edges": []},
        {"vertices": 100, "edges": [[0, 0]]},
        {"vertices": 100, "edges": [[0, 100]]},
        {"vertices": 100, "edges": [[False, 1]]},
        {"vertices": 100, "edges": [[0.0, 1]]},
        {"vertices": 100, "edges": [[0, float("nan")]]},
        {"vertices": 100, "edges": [[0]]},
        {"vertices": 100, "edges": [[0, 1], [1, 0]]},
    ],
)
def test_invalid_graph_input_rejected(graph):
    with pytest.raises(ValueError):
        _validate(graph)


def test_cycle_with_six_distinct_vertices_rejected():
    cycle = [[i, (i + 1) % 6] for i in range(6)]
    with pytest.raises(ValueError, match="simple cycle of length 6"):
        _validate({"vertices": 100, "edges": cycle})


def test_non_saturated_graph_rejected():
    # The isolated graph has no simple 5-edge paths for its missing pairs.
    with pytest.raises(ValueError, match="not C6-saturated"):
        _validate({"vertices": 100, "edges": []})


def test_claimed_scores_do_not_change_validation():
    graph = build_human_graph()
    expected = _validate(graph)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "0")):
        assert validate({**graph, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_search_is_seeded_and_does_not_read_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "5")
    monkeypatch.setenv("T061_SEARCH_TRIALS", "1")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first, second = baseline_run(), baseline_run()
    assert first == second
    assert first["search"]["reference_data_read"] is False
    _validate(first)


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional graph task failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional graph task failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
