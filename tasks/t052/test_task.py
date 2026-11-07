"""Task-local correctness and runner-control tests for T052."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t052.check import PARAMETERS, validate

ROOT = Path(__file__).resolve().parent
CONFIG = {"parameters": PARAMETERS}


def _distance(left, right):
    return sum(a != b for a, b in zip(left, right))


def test_human_and_reference_reconstruct_exact_pgl_code():
    from tasks.t052.human import run_code as human_run
    from tasks.t052.reference import run_code as reference_run

    human = human_run()
    reference = reference_run()
    human_result = validate(human, CONFIG, strict=True)
    reference_result = validate(reference, CONFIG, strict=True)
    assert human_result["objective"] == 1320
    assert reference_result["objective"] == 1320
    assert human_result["details"]["pairs_checked"] == 1320 * 1319 // 2 == 870540
    assert human_result["details"]["minimum_distance_observed"] == 10
    assert {tuple(row) for row in human["codewords"]} == {tuple(row) for row in reference["codewords"]}

    path = ROOT / "data/reference/pgl_2_11_n12_d9.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == "f33140d3e4278b1ad4adcc43dbd0823c1e453ff6c97d47e6fb91e17ecb02fb06"
    saved = json.loads(path.read_text())
    assert saved["codeword_count"] == 1320
    assert saved["minimum_hamming_distance"] == 10


def test_independent_score_and_claimed_score_is_ignored():
    from tasks.t052.reference import run_code

    solution = run_code()
    rows = solution["codewords"]
    independently_counted = 0
    minimum = 12
    for i, left in enumerate(rows):
        for right in rows[i + 1:]:
            distance = _distance(left, right)
            independently_counted += 1
            minimum = min(minimum, distance)
    assert independently_counted == 870540
    assert minimum == 10
    checked = validate(solution, CONFIG, strict=True)
    assert checked["objective"] == 1320
    assert validate({**solution, "objective": -1}, CONFIG) == checked
    assert validate({**solution, "score": float("nan")}, CONFIG) == checked
    assert validate({**solution, "claimed_score": {"forged": True}}, CONFIG) == checked


def test_checker_rejects_bad_rows_duplicates_and_distance_8():
    from tasks.t052.init_program import run_code

    valid = run_code()
    assert validate(valid, CONFIG)["objective"] == 12
    with pytest.raises(ValueError, match="nonempty"):
        validate({"codewords": []}, CONFIG)
    with pytest.raises(ValueError, match="exactly 12"):
        validate({"codewords": [[0, 1]]}, CONFIG)
    with pytest.raises(ValueError, match="integers"):
        validate({"codewords": [[False] + list(range(1, 12))]}, CONFIG)
    with pytest.raises(ValueError, match="integers"):
        validate({"codewords": [[0.0] + list(range(1, 12))]}, CONFIG)
    with pytest.raises(ValueError, match="integers"):
        validate({"codewords": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, float("nan")]]}, CONFIG)
    with pytest.raises(ValueError, match="not a permutation"):
        validate({"codewords": [[0] * 12]}, CONFIG)
    with pytest.raises(ValueError, match="distinct"):
        validate({"codewords": [valid["codewords"][0], valid["codewords"][0]]}, CONFIG)

    identity = list(range(12))
    distance_eight = identity[:]
    for i in range(0, 8, 2):
        distance_eight[i], distance_eight[i + 1] = distance_eight[i + 1], distance_eight[i]
    assert _distance(identity, distance_eight) == 8
    with pytest.raises(ValueError, match="below 9"):
        validate({"codewords": [identity, distance_eight]}, CONFIG)
    with pytest.raises(ValueError, match="unsupported"):
        validate(valid, {"parameters": {**PARAMETERS, "length": 11}})


def test_all_five_program_entries_return_valid_codes(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T052-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.setenv("MATHBENCH_SEARCH_ITERATIONS", "1")
    monkeypatch.setenv("T052_CANDIDATES_PER_RESTART", "25")
    monkeypatch.setenv("T052_CANDIDATES_PER_GENERATION", "25")
    from tasks.t052.init_program import run_code as init_run
    from tasks.t052.baseline import run_code as baseline_run
    from tasks.t052.human import run_code as human_run
    from tasks.t052.reference import run_code as reference_run
    from tasks.t052.evolution import run_code as evolution_run

    for run in (init_run, baseline_run, human_run, reference_run, evolution_run):
        result = run()
        assert validate(result, CONFIG, strict=True)["verification_status"] == "exact"


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T052 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T052 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
