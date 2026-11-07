import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t071.baseline import run_code as baseline_run
from tasks.t071.check import CONFIG_ID, N, PARAMETERS, deletion_outputs, validate
from tasks.t071.evolution import run_code as evolution_run
from tasks.t071.human import build_vt0, run_code as human_run
from tasks.t071.init_program import run_code as init_run
from tasks.t071.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _validate(solution):
    return validate(solution, CONFIG)


def test_all_five_entries_and_exact_vt_witness(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for solution in outputs:
        checked = _validate(solution)
        assert checked["verification_status"] == "exact"
        assert checked["objective"] == len(solution["codewords"])
        assert checked["details"]["pairwise_disjoint_deletion_outputs"] is True
    assert _validate(human_run())["objective"] == 3856
    assert human_run() == reference_run()
    assert outputs[1] == outputs[2]
    assert outputs[1]["search_metadata"]["reference_data_read"] is False


def test_reference_hash_and_vt_checksum_formula():
    metadata = json.loads((TASK / "sota.json").read_text())
    record = metadata["configurations"][CONFIG_ID]
    reference_path = TASK / record["witness"]
    human_path = TASK / "data/human/vt16_3856.json"
    for path in (reference_path, human_path):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["witness_sha256"]
    words = json.loads(reference_path.read_text())["codewords"]
    assert len(words) == len(set(words)) == 3856
    formula_words = build_vt0()["codewords"]
    assert words == formula_words
    for word in words:
        checksum = sum((N - bit) * ((word >> bit) & 1) for bit in range(N))
        assert checksum % 17 == 0


def test_deletion_outputs_are_exact_and_repeated_bits_are_deduplicated():
    assert deletion_outputs(0) == {0}
    assert deletion_outputs((1 << N) - 1) == {(1 << (N - 1)) - 1}
    assert len(deletion_outputs(0b0000000011111111)) == 2
    assert _validate({"codewords": [0, (1 << N) - 1]})["objective"] == 2
    with pytest.raises(ValueError, match="shares a deletion output"):
        _validate({"codewords": [0, 1]})


@pytest.mark.parametrize(
    "solution",
    [
        {"codewords": [0, 0]},
        {"codewords": [0, 1]},
        {"codewords": [-1]},
        {"codewords": [65536]},
        {"codewords": [True]},
        {"codewords": [1.0]},
        {"codewords": [float("nan")]},
        {"codewords": ["0000000000000000"]},
        {},
    ],
)
def test_invalid_or_uncorrectable_candidates_rejected(solution):
    with pytest.raises(ValueError):
        _validate(solution)


def test_claimed_scores_do_not_change_check_result():
    solution = reference_run()
    expected = _validate(solution)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "false")):
        assert validate({**solution, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_random_greedy_baseline_is_seeded(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "37")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    assert baseline_run() == baseline_run()


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T071 failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T071 failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
