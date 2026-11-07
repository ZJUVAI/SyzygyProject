"""Tests for the exact T034 checker and construction entry points."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t034.baseline import run_code as baseline_run
from tasks.t034.check import validate
from tasks.t034.evolution import run_code as evolution_run
from tasks.t034.human import run_code as human_run
from tasks.t034.init_program import run_code as seed_run
from tasks.t034.reference import run_code as reference_run


TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T034-C01",
    "parameters": {
        "colors": 2,
        "progression_length": 7,
        "domain": "consecutive_prefix_of_positive_integers",
        "common_difference": "positive_integer",
    },
    "direction": "maximize",
    "human_reference": 3703,
}


def _independent_ap_count(colors):
    """Independent direct loop over every valid (start, step) pair."""
    n = len(colors)
    checked = 0
    for start in range(n):
        for step in range(1, (n - 1 - start) // 6 + 1):
            checked += 1
            terms = [start + j * step for j in range(7)]
            assert len({colors[position] for position in terms}) > 1
    return checked


def test_human_formula_is_exact_3703_and_matches_independent_enumeration():
    witness = human_run()
    assert witness == reference_run()
    result = validate(witness, CONFIG, strict=True)
    assert result["objective"] == 3703
    assert result["verification_status"] == "exact"
    assert result["details"]["progressions_checked"] == _independent_ap_count(witness["colors"])
    assert result["details"]["progressions_checked"] > 1_000_000


def test_simple_seed_is_self_contained_and_valid():
    seed = seed_run()
    assert seed == {"n": 6, "colors": [0, 0, 0, 0, 0, 0]}
    assert validate(seed, CONFIG)["objective"] == 6


def test_checker_rejects_bad_input_and_a_monochromatic_progression():
    bad = [None, {}, {"n": 7, "colors": [0] * 6}, {"n": 7, "colors": [0] * 7},
           {"n": 7, "colors": [0, 0, 0, 0, 0, 0, True]},
           {"n": 7, "colors": [0, 0, 0, 0, 0, 0, 2]},
           {"n": 7, "colors": [0, 0, 0, 0, 0, 0, 1.0]},
           {"n": 7, "colors": [0, 0, 0, 0, 0, 0, float("nan")]},
           {"n": 7, "colors": [0, 0, 0, 0, 0, 0, float("inf")]},
           {"n": True, "colors": [0]}, {"n": 0, "colors": []}]
    for solution in bad:
        with pytest.raises(ValueError):
            validate(solution, CONFIG)
    with pytest.raises(ValueError, match="configuration id"):
        validate(seed_run(), {**CONFIG, "id": "T034-C02"})
    with pytest.raises(ValueError, match="parameters"):
        validate(seed_run(), {**CONFIG, "parameters": {**CONFIG["parameters"], "colors": 3}})


def test_checker_rejects_step_one_and_nonunit_step_violations():
    with pytest.raises(ValueError, match="arithmetic progression"):
        validate({"n": 7, "colors": [1] * 7}, CONFIG)
    # Positions 1, 3, 5, 7, 9, 11, 13 (one-based) form a step-2 progression.
    colors = [0, 1] * 7
    for position in range(0, 13, 2):
        colors[position] = 0
    with pytest.raises(ValueError, match="arithmetic progression"):
        validate({"n": len(colors), "colors": colors}, CONFIG)


def test_repeated_color_labels_are_valid_and_claimed_score_is_ignored():
    witness = reference_run()
    original = validate(witness, CONFIG)
    assert original["objective"] == 3703
    for claim in (-1, 0, 10**100, "3703", float("nan"), float("inf")):
        candidate = {**witness, "claimed_objective": claim, "score": claim}
        assert validate(candidate, CONFIG)["objective"] == original["objective"]
    assert validate({"n": 8, "colors": [0, 0, 0, 0, 0, 0, 1, 0]}, CONFIG)["objective"] == 8


def test_baseline_and_evolution_entry_are_reproducible(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "19")
    one = baseline_run()
    two = baseline_run()
    assert one == two
    checked = validate(one, CONFIG)
    assert checked["objective"] == one["claimed_objective"]
    assert one["search_metadata"]["seed"] == 19
    assert one["search_metadata"]["reference_data_read"] is False
    assert validate(evolution_run(), CONFIG)["verification_status"] == "exact"


def test_search_deadline_zero_returns_a_valid_seed(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEARCH_SECONDS", "0")
    result = baseline_run()
    assert result["n"] == 6
    assert validate(result, CONFIG)["objective"] == 6


def test_source_note_integrity_and_endpoint_exception():
    notes = TASK_DIR / "data" / "source" / "source_notes.md"
    hashes = json.loads((TASK_DIR / "data" / "source_hashes.json").read_text())
    assert hashlib.sha256(notes.read_bytes()).hexdigest() == hashes["source_notes"]["sha256"]
    witness_file = TASK_DIR / "data" / "reconstructed_3703_coloring.json"
    assert hashlib.sha256(witness_file.read_bytes()).hexdigest() == hashes["reconstructed_witness"]["sha256"]
    assert json.loads(witness_file.read_text()) == reference_run()
    colors = reference_run()["colors"]
    assert colors[0] == 0
    assert colors[-1] == 1
    assert all(colors[i] == 0 for i in range(0, 6 * 617, 617))


def test_generation_runner_reports_candidate_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
