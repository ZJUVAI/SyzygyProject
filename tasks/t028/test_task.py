import hashlib
import json
import os
from pathlib import Path
import re
import sys

import pytest

from tasks.t028.baseline import run_code as baseline_run
from tasks.t028.check import load_processing_times, makespan, validate
from tasks.t028.evolution import run_code as evolution_run
from tasks.t028.human import run_code as human_run
from tasks.t028.init_program import run_code as seed_run
from tasks.t028.reference import run_code as reference_run


TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T028-C01",
    "parameters": {
        "instance": "Ta051",
        "jobs": 50,
        "machines": 20,
        "schedule_type": "permutation",
        "processing_times_sha256": "57e114d970f7af11c64a3280068ef2ee1cfc037afd312e30d0d176900df564de",
    },
    "direction": "minimize",
    "human_reference": 3846,
}


def test_official_instance_snapshot_and_extracted_matrix_match():
    source = TASK_DIR / "data" / "source" / "tai50_20_official.txt"
    raw = source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == (
        "cc139745dece17a2538e74ad2eaed232cc97321293f6b121883a6e3c69c8f8ba"
    )
    text = raw.decode("ascii")
    header = re.search(r"(?m)^\s*50\s+20\s+1539989115\s+3875\s+3480\s*$", text)
    assert header
    marker = text.find("processing times :", header.end())
    raw_values = [int(value) for value in re.findall(
        r"\d+", text[marker + len("processing times :"):]
    )][:1000]
    expected = tuple(tuple(raw_values[i * 50:(i + 1) * 50]) for i in range(20))
    assert load_processing_times() == expected
    assert hashlib.sha256((TASK_DIR / "data" / "ta051.json").read_bytes()).hexdigest() == (
        CONFIG["parameters"]["processing_times_sha256"]
    )


def test_human_witness_replays_exactly_and_declared_score_is_ignored():
    witness = human_run()
    assert witness == reference_run()
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 3846
    assert result["verification_status"] == "exact"
    assert result["details"]["all_operations_recomputed"] is True
    assert result["details"]["claimed_objective_ignored"] is True
    assert validate({**witness, "claimed_objective": -10**9}, CONFIG)["objective"] == 3846


def test_identity_seed_is_a_valid_full_permutation():
    candidate = seed_run()
    assert candidate == {"permutation": list(range(1, 51))}
    assert validate(candidate, CONFIG)["objective"] == makespan(list(range(1, 51)))


def test_invalid_permutation_forms_are_rejected():
    valid = list(range(1, 51))
    cases = [
        (valid[:-1], "exactly 50"),
        (valid[:-1] + [49], "each job"),
        ([0] + valid[1:], "1..50"),
        ([51] + valid[1:], "1..50"),
        ([True] + valid[1:], "integers"),
        ([1.0] + valid[1:], "integers"),
        ([float("nan")] + valid[1:], "integers"),
        ([float("inf")] + valid[1:], "integers"),
        (["1"] + valid[1:], "integers"),
    ]
    for permutation, message in cases:
        with pytest.raises(ValueError, match=message):
            validate({"permutation": permutation}, CONFIG)


def test_wrong_shape_config_and_nonpermutation_payload_are_rejected():
    with pytest.raises(ValueError, match="permutation"):
        validate({"schedule": [[1, 2], [2, 1]]}, CONFIG)
    with pytest.raises(ValueError, match="configuration"):
        validate({"permutation": list(range(1, 51))}, {
            **CONFIG,
            "parameters": {**CONFIG["parameters"], "schedule_type": "nonpermutation"},
        })
    with pytest.raises(ValueError, match="configuration id"):
        validate({"permutation": list(range(1, 51))}, {**CONFIG, "id": "T028-C02"})
    with pytest.raises(ValueError, match="configuration"):
        validate({"permutation": list(range(1, 51))}, {
            **CONFIG,
            "parameters": {**CONFIG["parameters"], "processing_times_sha256": "candidate-controlled"},
        })


def test_checker_ignores_arbitrary_claimed_scores_and_recomputes():
    permutation = list(range(1, 51))
    true_value = validate({"permutation": permutation}, CONFIG)["objective"]
    for claimed in (-1, 0, 10**99, "3846", float("nan"), float("inf")):
        assert validate({"permutation": permutation, "objective": claimed}, CONFIG)["objective"] == true_value


def test_neh_swap_baseline_is_seeded_and_reports_budget_without_reference_data(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "31")
    first = baseline_run()
    second = baseline_run()
    assert first == second
    assert validate(first, CONFIG)["objective"] == first["claimed_objective"]
    metadata = first["search_metadata"]
    assert metadata["seed"] == 31
    assert metadata["iterations"] <= metadata["iteration_limit"]
    assert metadata["budget"]["iteration_limit"] == 2_000
    assert metadata["reference_data_read"] is False


def test_genetic_search_is_seeded_and_reports_budget_without_reference_data(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "19")
    first = evolution_run()
    second = evolution_run()
    assert first == second
    assert validate(first, CONFIG)["objective"] == first["claimed_objective"]
    metadata = first["search_metadata"]
    assert metadata["seed"] == 19
    assert metadata["generations"] <= metadata["generation_limit"]
    assert metadata["budget"]["population_size"] == 24
    assert metadata["reference_data_read"] is False


def test_generation_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
