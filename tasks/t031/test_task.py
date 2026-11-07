"""Tests for the T031 exact checker and construction entry points."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t031.baseline import run_code as baseline_run
from tasks.t031.check import validate
from tasks.t031.evolution import run_code as evolution_run
from tasks.t031.human import run_code as human_run
from tasks.t031.init_program import run_code as seed_run
from tasks.t031.reference import run_code as reference_run


TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T031-C01",
    "parameters": {
        "symbols": ["1", "2", "3", "4", "5", "6", "7"],
        "permutations_required": 5040,
        "containment": "contiguous_substring",
    },
    "direction": "minimize",
    "human_reference": 5913,
}


def test_public_attachment_hash_and_exact_5905_witness():
    path = TASK_DIR / "data" / "reference" / "public_5905_attachment.txt"
    raw = path.read_bytes()
    assert len(raw) == 5907
    assert hashlib.sha256(raw).hexdigest() == (
        "f0208fb0e8ea98b015799b8f0dfaadc58d5909bad4a089603f2c9c4768536f67"
    )
    witness = reference_run()
    assert len(witness["word"]) == 5905
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 5905
    assert result["verification_status"] == "exact"
    assert result["details"]["distinct_permutations_found"] == 5040
    assert result["details"]["windows_checked"] == 5899


def test_reconstructed_human_method_witness_and_score():
    witness = human_run()
    assert len(witness["word"]) == 5913
    assert witness["word"] == (TASK_DIR / "data" / "reference" / "human_ashlock_tillotson_5913.txt").read_text()
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 5913
    assert result["details"]["distinct_permutations_found"] == 5040


def test_self_contained_seed_is_valid_and_has_35280_symbols():
    candidate = seed_run()
    assert set(candidate) == {"word"}
    assert len(candidate["word"]) == 5040 * 7
    result = validate(candidate, CONFIG)
    assert result["objective"] == 35280
    assert result["verification_status"] == "exact"


def test_checker_uses_contiguous_windows_and_ignores_claimed_scores():
    witness = reference_run()
    base = validate(witness, CONFIG)
    for claimed in (-999, 0, 10**100, "5905", float("nan"), float("inf")):
        candidate = {**witness, "claimed_objective": claimed, "score": claimed}
        assert validate(candidate, CONFIG)["objective"] == base["objective"]
    # All required symbols occur repeatedly, but subsequence-only coverage is insufficient.
    repeated = {"word": "1234567" * 100}
    with pytest.raises(ValueError, match="missing"):
        validate(repeated, CONFIG)
    # Repeating the complete valid witness is permitted by the "at least once" rule.
    duplicated = {"word": witness["word"] + witness["word"]}
    assert validate(duplicated, CONFIG)["objective"] == 11810


def test_bad_data_and_configuration_are_rejected():
    for solution in (None, {}, {"word": 123}, {"word": ""}, {"word": "1234568"}, {"word": "12345x7"}):
        with pytest.raises(ValueError):
            validate(solution, CONFIG)
    with pytest.raises(ValueError, match="configuration id"):
        validate(reference_run(), {**CONFIG, "id": "T031-C02"})
    with pytest.raises(ValueError, match="parameters"):
        validate(reference_run(), {**CONFIG, "parameters": {**CONFIG["parameters"], "permutations_required": 1}})


def test_traditional_greedy_baseline_and_evolution_are_reproducible(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "73")
    first = baseline_run()
    second = baseline_run()
    assert first == second
    checked = validate(first, CONFIG)
    assert checked["objective"] == first["claimed_objective"]
    assert first["search_metadata"]["seed"] == 73
    assert first["search_metadata"]["iterations"] <= first["search_metadata"]["iteration_limit"]
    assert first["search_metadata"]["reference_data_read"] is False
    evolved = evolution_run()
    assert validate(evolved, CONFIG)["verification_status"] == "exact"


def test_generation_runner_reports_candidate_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 300)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
