"""Tests for T044 graph validation and program entry points."""

import hashlib
import math
import os
import sys
from collections import deque
from pathlib import Path

import pytest

from tasks.t044.baseline import run_code as baseline_run
from tasks.t044.check import validate
from tasks.t044.evolution import run_code as evolution_run
from tasks.t044.human import run_code as human_run
from tasks.t044.init_program import run_code as seed_run
from tasks.t044.reference import run_code as reference_run


TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T044-C01",
    "parameters": {
        "maximum_degree": 3,
        "diameter_at_most": 5,
        "graph": "simple_undirected_connected",
    },
    "direction": "maximize",
    "human_reference": 70,
}


def _independent_graph_audit(candidate):
    n = candidate["n"]
    adjacency = [set() for _ in range(n)]
    for left, right in candidate["edges"]:
        adjacency[left].add(right)
        adjacency[right].add(left)
    assert max(map(len, adjacency)) == 3
    diameter = 0
    for source in range(n):
        distances = {source: 0}
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor not in distances:
                    distances[neighbor] = distances[vertex] + 1
                    queue.append(neighbor)
        assert len(distances) == n
        diameter = max(diameter, max(distances.values()))
    return len({tuple(sorted(edge)) for edge in candidate["edges"]}), diameter


@pytest.mark.parametrize(
    ("filename", "program", "sha256"),
    [
        (
            "afy_70_adjlist_nx.txt",
            human_run,
            "9d2bca25876fb72ca81727a7dbd3d91d7d9c84e2233d6a055742146b0d98cafb",
        ),
        (
            "coxeter_70_adjlist_nx.txt",
            reference_run,
            "2b62872f9ac8ca2f8bed3f6495033aa7e7acd97d16e1427a3532c638100dbde5",
        ),
    ],
)
def test_two_public_order_70_witnesses_are_exact(filename, program, sha256):
    source = TASK_DIR / "data" / "reference" / filename
    assert hashlib.sha256(source.read_bytes()).hexdigest() == sha256
    candidate = program()
    result = validate(candidate, CONFIG, strict=True)
    assert result["objective"] == 70
    assert result["details"]["edge_count"] == 105
    assert result["details"]["maximum_degree"] == 3
    assert result["details"]["diameter"] == 5
    assert _independent_graph_audit(candidate) == (105, 5)


def test_simple_seed_and_small_boundary_graphs_are_valid():
    assert validate(seed_run(), CONFIG)["objective"] == 1
    assert validate({"n": 2, "edges": [[0, 1]]}, CONFIG)["objective"] == 2
    assert validate({"n": 6, "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5]]}, CONFIG)["objective"] == 6


def test_checker_rejects_bad_edges_degree_connectivity_and_diameter():
    invalid = [
        {"n": 2, "edges": [[0, 0]]},
        {"n": 2, "edges": [[0, 1], [1, 0]]},
        {"n": 2, "edges": [[0, 2]]},
        {"n": 5, "edges": [[0, 1], [0, 2], [0, 3], [0, 4]]},
        {"n": 3, "edges": [[0, 1]]},
        {"n": 7, "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]},
        {"n": True, "edges": []},
        {"n": 1.0, "edges": []},
        {"n": math.nan, "edges": []},
        {"n": 95, "edges": []},
        {"n": 2, "edges": [[False, 1]]},
        {"n": 2, "edges": [[0.0, 1]]},
        {"n": 1, "edges": [[0]]},
        None,
    ]
    for candidate in invalid:
        with pytest.raises(ValueError):
            validate(candidate, CONFIG)


def test_claimed_scores_are_ignored_and_configuration_is_fixed():
    candidate = human_run()
    original = validate(candidate, CONFIG)
    for forged in (-1, 0, 10**100, "70", math.nan, math.inf, True):
        changed = {**candidate, "claimed_objective": forged, "score": forged}
        assert validate(changed, CONFIG) == original
    with pytest.raises(ValueError, match="configuration id"):
        validate(candidate, {**CONFIG, "id": "T044-C02"})
    with pytest.raises(ValueError, match="parameters"):
        validate(candidate, {**CONFIG, "parameters": {**CONFIG["parameters"], "diameter_at_most": 4}})


def test_all_five_programs_return_valid_data_and_seeded_baseline_replays(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T044-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "36")
    for program in (seed_run, baseline_run, evolution_run, human_run, reference_run):
        assert validate(program(), CONFIG)["verification_status"] == "exact"
    first = baseline_run()
    second = baseline_run()
    assert first == second
    assert first["search_metadata"]["comparison_data_read"] is False
    assert first["search_metadata"]["attempts"] <= first["search_metadata"]["attempt_limit"]


def test_shared_runner_surfaces_candidate_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
