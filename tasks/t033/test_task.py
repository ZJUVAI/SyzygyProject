import json
from pathlib import Path

import pytest

from tasks.t033.check import validate
from tasks.t033.human import run_code as human_run
from tasks.t033.reference import run_code as reference_run


TASK = json.loads((Path(__file__).parent / "task.json").read_text())
CONFIG = TASK["configurations"][0]
GRAPH = json.loads((Path(__file__).parent / "data" / "instance.json").read_text())
N = GRAPH["n"]


def test_all_same_side_is_valid_and_exact():
    result = validate({"labels": [0] * N}, CONFIG)
    assert result["objective"] == 0
    assert result["verification_status"] == "exact"


def test_one_vertex_cut_equals_its_degree():
    labels = [0] * N
    labels[0] = 1
    result = validate({"labels": labels}, CONFIG)
    degree = sum(weight for u, v, weight in GRAPH["edges"] if u == 0 or v == 0)
    assert result["objective"] == degree


def test_pinned_graph_has_expected_edges_without_duplicates():
    edges = GRAPH["edges"]
    pairs = [(min(u, v), max(u, v)) for u, v, _ in edges]
    assert (GRAPH["n"], len(edges)) == (10000, 9999)
    assert all(u != v and w == 1 for u, v, w in edges)
    assert len(set(pairs)) == len(edges)


def test_human_baseline_witness_replays(monkeypatch):
    monkeypatch.delenv("MATHBENCH_SEED", raising=False)
    solution = human_run()
    assert validate(solution, CONFIG)["objective"] == 8616
    metadata = solution["search_metadata"]
    assert metadata == {
        "algorithm": "steepest_improving_single_vertex_flip",
        "seed": 0,
        "restarts": 4,
        "max_flips_per_restart": 10000,
        "flips_per_restart": [2163, 2226, 2227, 2158],
        "total_flips": 8774,
        "budget": "fixed iteration cap; stop early at 1-flip local optimum",
    }


def test_fixed_reference_replays_and_claim_is_ignored():
    solution = reference_run()
    result = validate(solution, CONFIG)
    assert result["objective"] == 8616
    solution["claimed_score"] = 10**9
    assert validate(solution, CONFIG)["objective"] == 8616


@pytest.mark.parametrize("labels", [
    [0] * (N - 1),
    [0] * (N - 1) + [True],
    [0] * (N - 1) + [2],
    [0] * (N - 1) + [0.0],
    [0] * (N - 1) + [float("nan")],
    [0] * (N - 1) + [float("inf")],
    [0] * (N - 1) + ["1"],
])
def test_invalid_label_vectors_are_rejected(labels):
    with pytest.raises(ValueError):
        validate({"labels": labels}, CONFIG)


def test_candidate_duplicate_edges_are_ignored():
    labels = [0] * N
    labels[0] = 1
    candidate = {"labels": labels, "edges": [[0, 1, 1], [0, 1, 1]],
                 "claimed_score": 999}
    expected = validate({"labels": labels}, CONFIG)["objective"]
    assert validate(candidate, CONFIG)["objective"] == expected


def test_configuration_must_match_pinned_graph():
    changed = dict(CONFIG)
    changed["parameters"] = dict(CONFIG["parameters"], n=N + 1)
    with pytest.raises(ValueError):
        validate({"labels": [0] * N}, changed)
