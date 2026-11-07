"""Tests for the T076 task-local programs and exact checker."""

import copy
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest

from tasks.t076 import baseline, check, evolution, human, init_program, reference


ROOT = Path(__file__).resolve().parents[2]
TASK = Path(__file__).resolve().parent
CONFIG = json.loads((TASK / "task.json").read_text())["configurations"][0]
CONFIGS = {item["id"]: item for item in json.loads((TASK / "task.json").read_text())["configurations"]}


def test_all_entries_return_valid_results_and_reference_assets_are_frozen():
    outputs = [
        init_program.run_code(),
        baseline.run_code(),
        human.run_code(),
        reference.run_code(),
    ]
    values = [check.validate(item, CONFIG)["objective"] for item in outputs]
    assert values[0] == 1 << 14
    assert values[1] >= 1
    assert values[2] == 8807
    assert values[3] == 8635
    assert baseline.run_code()["search_metadata"]["reference_data_read"] is False
    assert hashlib.sha256((TASK / "data/reference/sharp_8635_transcribed.json").read_bytes()).hexdigest() == (
        "e5b1c66298ad4643ecc22e6d589c764a4aba20c0b18ce0656def98a18d7b0fa0"
    )


def test_ignored_claims_cannot_change_any_validation_field():
    valid = human.run_code()
    expected = check.validate(valid, CONFIG)
    for key in ("objective", "score", "claimed_score"):
        forged = copy.deepcopy(valid)
        forged[key] = "999999999999999999999999"
        assert check.validate(forged, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


@pytest.mark.parametrize(
    "elements",
    [
        [1] * 15,
        [0] + list(range(2, 16)),
        [-1] + list(range(2, 16)),
        [True] + list(range(2, 16)),
        [1.0] + list(range(2, 16)),
        [float("nan")] + list(range(2, 16)),
        list(range(1, 15)),
        [1, 2, 3] + [1 << bit for bit in range(3, 15)],
    ],
)
def test_invalid_constructions_are_rejected(elements):
    with pytest.raises(ValueError):
        check.validate({"elements": elements}, CONFIG)


def test_exact_large_decimal_inputs_have_no_artificial_integer_cap():
    base = 10**5000
    result = check.validate(
        {"elements": [str(base * (1 << bit)) for bit in range(15)]}, CONFIG
    )
    assert result["objective"] == base * (1 << 14)
    assert result["verification_status"] == "exact"


def test_config_is_fixed_and_seeded_search_is_repeatable(monkeypatch):
    with pytest.raises(ValueError):
        check.validate(init_program.run_code(), {**CONFIG, "id": "T076-C02"})
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T076-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    monkeypatch.setattr(baseline, "CAP_START", 8_000)
    monkeypatch.setattr(baseline, "CAP_STOP", 8_000)
    first = baseline.run_code()
    second = baseline.run_code()
    assert first == second
    assert first["search_metadata"]["cap_trials_completed"] == 1


def test_evolution_entry_invokes_its_search(monkeypatch):
    expected = {"elements": [1, 2, 4], "search_metadata": {"seed": 9}}
    monkeypatch.setattr(evolution, "_run_search", lambda: expected)
    assert evolution.run_code() is expected


def test_runner_reports_program_errors_and_timeouts_without_registry_changes():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional failure')"], env, 5)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
    assert time.monotonic() - start < 3


@pytest.mark.parametrize(("config_id", "human_value", "reference_value", "subset_count"), [
    ("T076-C02", 17305, 17072, 1 << 16),
    ("T076-C03", 34301, 33531, 1 << 17),
])
def test_expanded_configuration_witnesses_and_programs(monkeypatch, config_id, human_value, reference_value, subset_count):
    config = CONFIGS[config_id]
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", config_id)
    h = human.run_code()
    r = reference.run_code()
    assert check.validate(h, config)["objective"] == human_value
    checked_reference = check.validate(r, config)
    assert checked_reference["objective"] == reference_value
    assert checked_reference["details"]["subset_sums_verified"] == subset_count
    assert check.validate(init_program.run_code(), config)["verification_status"] == "exact"
    assert check.validate(baseline.run_code(), config)["verification_status"] == "exact"
    assert check.validate(evolution.run_code(), config)["verification_status"] == "exact"


@pytest.mark.parametrize("config_id", ["T076-C02", "T076-C03"])
def test_expanded_config_rejects_parameter_mismatch_and_ignores_claims(monkeypatch, config_id):
    config = CONFIGS[config_id]
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", config_id)
    witness = human.run_code()
    before = check.validate(witness, config)
    forged = {**witness, "objective": -999, "claimed_score": -999, "score": -999}
    assert check.validate(forged, config) == before
    mismatch = copy.deepcopy(config)
    mismatch["parameters"]["element_count"] -= 1
    with pytest.raises(ValueError, match="parameters do not match"):
        check.validate(witness, mismatch)


def test_expanded_witness_hashes_and_records_match():
    records = json.loads((TASK / "records.json").read_text())
    sota = json.loads((TASK / "sota.json").read_text())
    expected_public = {"T076-C02": 17072, "T076-C03": 33531}
    for cid in ("T076-C02", "T076-C03"):
        entry = records["configurations"][cid]
        for label in ("best_human", "best_public"):
            witness = TASK / entry[label]["witness_file"]
            assert hashlib.sha256(witness.read_bytes()).hexdigest() == entry[label]["witness_sha256"]
        se = sota["configurations"][cid]
        assert se["acceptance_status"] == "accepted_by_sol"
        assert se["best_human"]["witness_sha256"] == entry["best_human"]["witness_sha256"]
        assert se["best_public"]["witness_sha256"] == entry["best_public"]["witness_sha256"]
        assert se["best_reproduced"]["witness_sha256"] == entry["best_public"]["witness_sha256"]
        assert se["public_value"] == se["reproduced_value"] == expected_public[cid]
        assert se["matches_public_best"] is True
        assert entry["best_public"]["value"] == expected_public[cid]
        assert entry["previously_selected_public_candidate"]["status"].startswith("valid but weaker")
