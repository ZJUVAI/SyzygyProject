"""Tests for the T042 checker, witnesses, and callable programs."""

import hashlib
import json
import math
import os
import sys
from pathlib import Path

import pytest

from tasks.t042.baseline import run_code as baseline_run
from tasks.t042.check import validate
from tasks.t042.evolution import run_code as evolution_run
from tasks.t042.human import run_code as human_run
from tasks.t042.init_program import run_code as seed_run
from tasks.t042.reference import run_code as reference_run


CONFIG = {
    "id": "T042-C01",
    "parameters": {
        "N": 212,
        "universe": "integers_1_through_N",
        "forbidden_pattern": "nontrivial_three_term_arithmetic_progression",
    },
    "direction": "maximize",
    "human_reference": 32,
}


def _independent_ap_audit(elements):
    values = set(elements)
    for a in values:
        for b in values:
            c = 2 * b - a
            if a < b < c and c in values:
                return False
    return True


def test_public_43_witness_is_exact_and_matches_source_record():
    source_file = Path(__file__).parent / "data" / "reference" / "ergezer_n212_k43_witness.json"
    assert hashlib.sha256(source_file.read_bytes()).hexdigest() == (
        "41377c0db2e50f2d7753434ac472e82d831d093013562a477fffb068f117eb28"
    )
    candidate = reference_run()
    result = validate(candidate, CONFIG, strict=True)
    assert len(candidate["elements"]) == 43
    assert result["objective"] == 43
    assert result["verification_status"] == "exact"
    assert _independent_ap_audit(candidate["elements"])


def test_classical_human_formula_has_32_elements_and_is_valid():
    candidate = human_run()
    source_file = Path(__file__).parent / "data" / "reference" / "odlyzko_stanley_n212_32.json"
    assert hashlib.sha256(source_file.read_bytes()).hexdigest() == (
        "9c4230152b0e0f1e8a98a35d78944fd190b9d94b0c14ba4a458b640c8fdaf24b"
    )
    assert candidate == json.loads(source_file.read_text(encoding="utf-8"))
    assert len(candidate["elements"]) == 32
    assert min(candidate["elements"]) == 1
    assert max(candidate["elements"]) == 122
    assert validate(candidate, CONFIG, strict=True)["objective"] == 32
    assert _independent_ap_audit(candidate["elements"])


def test_simple_seed_and_edge_sets_are_valid():
    assert validate(seed_run(), CONFIG)["objective"] == 1
    assert validate({"elements": [212]}, CONFIG)["objective"] == 1
    assert validate({"elements": []}, CONFIG)["objective"] == 0


def test_checker_rejects_progressions_bad_types_duplicates_and_bad_range():
    invalid = [
        {"elements": [1, 2, 3]},
        {"elements": [1, 1]},
        {"elements": [0]},
        {"elements": [213]},
        {"elements": [True]},
        {"elements": [1.0]},
        {"elements": [math.nan]},
        {"elements": [math.inf]},
        {"elements": "1,2,3"},
        None,
    ]
    for candidate in invalid:
        with pytest.raises(ValueError):
            validate(candidate, CONFIG)


def test_claimed_score_is_ignored_and_configuration_is_fixed():
    witness = reference_run()
    for forged in (-1, 0, 10**100, "43", math.nan, math.inf, True):
        result = validate({**witness, "claimed_objective": forged, "score": forged}, CONFIG)
        assert result["objective"] == 43
        assert result["details"]["claimed_score_ignored"] is True
    with pytest.raises(ValueError, match="configuration id"):
        validate(witness, {**CONFIG, "id": "T042-C02"})
    with pytest.raises(ValueError, match="parameters"):
        validate(witness, {**CONFIG, "parameters": {**CONFIG["parameters"], "N": 211}})


def test_all_five_program_entries_return_valid_constructions(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T042-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "212")
    programs = (seed_run, baseline_run, evolution_run, human_run, reference_run)
    for program in programs:
        output = program()
        assert validate(output, CONFIG)["verification_status"] == "exact"
    search = baseline_run()
    assert search["search_metadata"]["seed"] == 212
    assert search["search_metadata"]["comparison_data_read"] is False
    assert search["search_metadata"]["restarts"] <= 48


def test_shared_runner_surfaces_candidate_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
