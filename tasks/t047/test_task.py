"""Exact tests for T047 integer difference bases."""

import hashlib
import json
import math
import os
from pathlib import Path

import pytest

from mathbench.evaluate import _run
from tasks.t047.baseline import run_code as baseline_run
from tasks.t047.check import validate
from tasks.t047.evolution import run_code as evolution_run
from tasks.t047.human import run_code as human_run
from tasks.t047.init_program import run_code as seed_run
from tasks.t047.reference import run_code as reference_run


TASK_DIR = Path(__file__).parent
CONFIG = {
    "id": "T047-C01",
    "parameters": {
        "N": 6166,
        "ambient_group": "integers_under_subtraction",
        "required_differences": "positive_integers_1_through_N",
    },
    "direction": "minimize",
    "human_reference": 158,
}
REFERENCE_PATH = TASK_DIR / "data" / "reference" / "singer_q31_leech_product_n6166_128.json"
REFERENCE_SHA256 = "e7af998f30472857a1403e637b595e7d69dbde02dc851060c03bbdf1fe0e248c"


def _independent_differences(basis):
    return {right - left for index, left in enumerate(sorted(basis)) for right in sorted(basis)[index + 1 :]}


def test_public_128_reconstruction_and_independent_all_distance_scan():
    assert hashlib.sha256(REFERENCE_PATH.read_bytes()).hexdigest() == REFERENCE_SHA256
    solution = reference_run()
    result = validate(solution, CONFIG, strict=True)
    assert result["objective"] == 128
    assert len(set(solution["basis"])) == 128
    differences = _independent_differences(solution["basis"])
    assert all(distance in differences for distance in range(1, 6167))
    assert solution["construction"]["modulus"] == 993
    assert solution["construction"]["cyclic_multiplier"] == 172


def test_wichmann_human_baseline_and_classical_parameters():
    solution = human_run()
    result = validate(solution, CONFIG, strict=True)
    assert result["objective"] == 158
    assert solution["basis"][0] == 0
    assert solution["basis"][-1] == 6548
    assert len(solution["basis"]) == 158
    assert _independent_differences(solution["basis"]).issuperset(range(1, 6167))


def test_simple_initial_seed_is_valid_but_not_a_comparison_input():
    solution = seed_run()
    assert len(solution["basis"]) == 6167
    assert validate(solution, CONFIG)["objective"] == 6167
    assert validate({"basis": list(range(6168))}, CONFIG)["objective"] == 6168


@pytest.mark.parametrize(
    "solution",
    [
        {"basis": [0]},
        {"basis": []},
        {"basis": [0, 2]},
        {"basis": [0, 6166, 6168]},
        {"basis": [0, 1, 1]},
        {"basis": [False, 1]},
        {"basis": [0, 1.0]},
        {"basis": [0, math.nan]},
        {"basis": [0, math.inf]},
        {"basis": "0,1"},
    ],
)
def test_checker_rejects_invalid_or_out_of_contract_basis(solution):
    with pytest.raises(ValueError):
        validate(solution, CONFIG)


def test_claimed_score_changes_do_not_change_validation():
    basis = reference_run()["basis"]
    expected = validate({"basis": basis}, CONFIG)
    for key, value in (("claimed_objective", -10**9), ("objective", 0), ("score", 1e300)):
        forged = {"basis": basis, key: value}
        assert validate(forged, CONFIG) == expected


def test_wrong_config_is_rejected():
    wrong = {**CONFIG, "parameters": {**CONFIG["parameters"], "N": 6167}}
    with pytest.raises(ValueError):
        validate({"basis": [0, 1]}, wrong)


def test_all_five_program_entries_and_seeded_search_metadata(monkeypatch):
    assert validate(evolution_run(), CONFIG)["objective"] <= 6167
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T047-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "17")
    candidate = baseline_run()
    result = validate(candidate, CONFIG, strict=True)
    assert result["verification_status"] == "exact"
    metadata = candidate["search_metadata"]
    assert metadata["seed"] == 17
    assert metadata["comparison_data_read"] is False
    assert metadata["restart_limit"] == 6
    assert metadata["completed_restarts"] >= 0


def test_program_entries_reject_an_unknown_configuration(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T047-UNKNOWN")
    for program in (seed_run, baseline_run, human_run, reference_run, evolution_run):
        with pytest.raises(ValueError, match="unsupported configuration"):
            program()


def test_runner_reports_candidate_error_and_timeout(tmp_path):
    error_program = tmp_path / "error_program.py"
    error_program.write_text("raise RuntimeError('expected failure')\n", encoding="utf-8")
    timeout_program = tmp_path / "timeout_program.py"
    timeout_program.write_text("import time\ntime.sleep(5)\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="expected failure"):
        _run([os.sys.executable, str(error_program)], dict(os.environ), timeout=3)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([os.sys.executable, str(timeout_program)], dict(os.environ), timeout=0.1)


def test_saved_witness_json_is_strict_and_matches_reference_program():
    stored = json.loads(REFERENCE_PATH.read_text(encoding="utf-8"))
    assert stored == reference_run()
    assert len(stored["basis"]) == 128
