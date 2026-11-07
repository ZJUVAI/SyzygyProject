import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t030.baseline import run_code as baseline_run
from tasks.t030.check import load_graph, validate
from tasks.t030.evolution import run_code as evolution_run
from tasks.t030.human import run_code as human_run
from tasks.t030.init_program import run_code as seed_run
from tasks.t030.reference import run_code as reference_run


TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T030-C01",
    "parameters": {
        "instance": "DSJC1000.5",
        "vertices": 1000,
        "edges": 249826,
        "input_sha256": "51550de59559742f72c2da8e3963edab39124cd8f334eb63cae10d9bb3f132bd",
    },
    "direction": "minimize",
    "human_reference": 86,
}


def test_frozen_dimacs_text_matches_trusted_graph_json():
    source_path = TASK_DIR / "data" / "source" / "DSJC1000.5.col"
    raw = source_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (
        "17b395030fbab1e2a6564396c3a161dbb3248423953e6b462377a018b8f4bb6c"
    )
    n = m = None
    edges = []
    for line in raw.decode("ascii").splitlines():
        fields = line.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            assert fields[1] == "edge"
            n, m = map(int, fields[2:4])
        elif fields[0] == "e":
            edges.append([int(fields[1]) - 1, int(fields[2]) - 1])
    assert (n, m, len(edges)) == (1000, 249826, 249826)
    payload = json.loads((TASK_DIR / "data" / "instance.json").read_text())
    assert payload == {"instance": "DSJC1000.5", "vertices": n, "edges": edges}
    assert hashlib.sha256((TASK_DIR / "data" / "instance.json").read_bytes()).hexdigest() == (
        CONFIG["parameters"]["input_sha256"]
    )


def test_human_witness_exactly_replays_and_claimed_score_is_ignored():
    witness = human_run()
    assert witness["claimed_objective"] == 86
    assert hashlib.sha256((TASK_DIR / "data" / "human_witness.json").read_bytes()).hexdigest() == (
        "de1106b17304b59fb18809d285e91ad78f8414a892e2e5ea1e7fedbfaa630007"
    )
    source_witness = TASK_DIR / "data" / "source" / "DSJC1000.5.sol"
    source_raw = source_witness.read_bytes()
    assert hashlib.sha256(source_raw).hexdigest() == (
        "4d77396da94d8a3427557fad4ff6dbc3ecc490670260bae22c3d646ab88248f0"
    )
    source_colors = [None] * 1000
    for line in source_raw.decode("ascii").splitlines():
        fields = line.split()
        if len(fields) == 4 and fields[0] == "vertex":
            source_colors[int(fields[1])] = int(fields[3])
    assert witness["colors"] == source_colors
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 86
    assert result["verification_status"] == "exact"
    assert result["details"]["edges_checked"] == 249826
    assert result["details"]["claimed_objective_ignored"] is True
    assert result["details"]["claimed_score_ignored"] is True
    for claimed in (-999, 0, 10**100, "86", float("nan"), float("inf")):
        for key in ("claimed_objective", "claimed_score", "objective"):
            assert validate({**witness, key: claimed}, CONFIG)["objective"] == 86


def test_public_82_certificate_is_replayed_and_older_83_certificate_is_archived():
    source82 = TASK_DIR / "data" / "source" / "DSJC1000.5_K82_col.txt"
    raw82 = source82.read_bytes()
    assert hashlib.sha256(raw82).hexdigest() == (
        "0e73778bb2934ee8a828b59cbd3b5deaaadc88716d5010af67ec7cdaec2c5109"
    )
    colors82 = [int(value) for value in raw82.decode("ascii").split()]
    assert reference_run() == {"colors": colors82, "claimed_objective": 82}
    result82 = validate({"colors": colors82}, CONFIG, strict=True)
    assert result82["objective"] == 82
    assert result82["details"]["claimed_score_ignored"] is True
    saved82 = json.loads((TASK_DIR / "data" / "DSJC1000.5_K82_verification.json").read_text())
    assert saved82["distinct_colors_recomputed"] == result82["objective"]
    assert saved82["conflicting_edges"] == 0

    source83 = TASK_DIR / "data" / "source" / "DSJC1000.5_K83.txt"
    raw83 = source83.read_bytes()
    assert hashlib.sha256(raw83).hexdigest() == (
        "1b7deb4d7e6d376a76eb027f645262ee8ca35e57bec0f87ce547800de5b2aca7"
    )
    colors83 = [int(value) for value in raw83.decode("ascii").splitlines()[1].split()]
    assert validate({"colors": colors83}, CONFIG)["objective"] == 83


def test_self_contained_cold_seed_is_valid():
    candidate = seed_run()
    assert candidate == {"colors": list(range(1000))}
    result = validate(candidate, CONFIG)
    assert result["objective"] == 1000
    assert result["verification_status"] == "exact"


def test_malformed_or_improper_colorings_are_rejected():
    valid = human_run()["colors"]
    cases = [
        (valid[:-1], "1000 vertices"),
        (valid[:2], "1000 vertices"),
        ([True] + valid[1:], "integers"),
        ([1.0] + valid[1:], "integers"),
        ([float("nan")] + valid[1:], "integers"),
        ([float("inf")] + valid[1:], "integers"),
        (["1"] + valid[1:], "integers"),
        ([0] * 1000, "edge 0"),
    ]
    for colors, message in cases:
        with pytest.raises(ValueError, match=message):
            validate({"colors": colors}, CONFIG)
    with pytest.raises(ValueError, match="colors"):
        validate({"assignment": valid}, CONFIG)
    with pytest.raises(ValueError, match="configuration"):
        validate({"colors": valid}, {
            **CONFIG,
            "parameters": {**CONFIG["parameters"], "input_sha256": "candidate-controlled"},
        })
    with pytest.raises(ValueError, match="configuration id"):
        validate({"colors": valid}, {**CONFIG, "id": "T030-C02"})


def test_exact_checker_recounts_distinct_colors_and_checks_every_edge():
    adjacency, edges = load_graph()
    assert len(adjacency) == 1000
    assert sum(map(len, adjacency)) == 2 * 249826
    colors = list(range(1000))
    # Renumber labels without changing the construction; the objective remains 1000.
    renamed = [color + 10000 for color in colors]
    result = validate({"colors": renamed, "objective": -1}, CONFIG)
    assert result["objective"] == 1000
    assert all(renamed[u] != renamed[v] for u, v in edges)


def test_dsatur_baseline_and_evolution_entry_are_seeded_and_valid(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "31")
    first = baseline_run()
    second = baseline_run()
    assert first == second
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    seed_zero_result = baseline_run()
    saved_result = json.loads((TASK_DIR / "best" / "seed0_dsatur_result.json").read_text())
    saved_verification = json.loads((TASK_DIR / "best" / "seed0_dsatur_verification.json").read_text())
    assert seed_zero_result == saved_result
    assert validate(saved_result, CONFIG) == saved_verification
    assert validate(first, CONFIG)["objective"] == first["claimed_objective"]
    metadata = first["search_metadata"]
    assert metadata["seed"] == 31
    assert metadata["iterations"] <= metadata["iteration_limit"]
    assert metadata["reference_data_read"] is False
    evolved = evolution_run()
    assert len(evolved["colors"]) == 1000
    assert validate(evolved, CONFIG)["verification_status"] == "exact"


def test_generation_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
