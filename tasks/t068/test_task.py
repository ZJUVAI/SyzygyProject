import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t068.baseline import run_code as baseline_run
from tasks.t068.check import CONFIG_ID, PARAMETERS, validate
from tasks.t068.evolution import run_code as evolution_run
from tasks.t068.human import build_human_code, run_code as human_run
from tasks.t068.init_program import run_code as init_run
from tasks.t068.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _validate(solution):
    return validate(solution, CONFIG)


def test_all_five_entries_and_reproduced_public_count(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for solution in outputs:
        checked = _validate(solution)
        assert checked["verification_status"] == "exact"
        assert checked["details"]["covered_word_count"] == 1024
        assert checked["objective"] == len(solution["codewords"])
    assert _validate(human_run())["objective"] == 128
    assert _validate(reference_run())["objective"] == 120


def test_frozen_public_list_matches_n10_source_and_hash():
    path = TASK / "data/reference/oeis_a000983_n10.json"
    raw = path.read_bytes()
    metadata = json.loads((TASK / "sota.json").read_text())
    record = metadata["configurations"][CONFIG_ID]
    assert hashlib.sha256(raw).hexdigest() == record["witness_sha256"]
    source_path = TASK / "data/source/oeis_a000983.txt"
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == record["source_file_sha256"]
    words = json.loads(raw)["codewords"]
    assert len(words) == 120
    assert all(len(word) == 10 and set(word) <= {"0", "1"} for word in words)
    assert _validate({"codewords": [int(word, 2) for word in words]})["objective"] == 120

    source = source_path.read_text()
    n10_section = source.split("a(10)<=120", 1)[1].split("a(11)<=192", 1)[0]
    assert words == __import__("re").findall(r"\b[01]{10}\b", n10_section)


def test_hamming_product_has_128_words_and_full_cover():
    solution = build_human_code()
    words = solution["codewords"]
    assert len(words) == len(set(words)) == 128
    assert _validate(solution)["objective"] == 128


@pytest.mark.parametrize(
    "solution",
    [
        {"codewords": [0, 0]},
        {"codewords": [0]},
        {"codewords": [-1]},
        {"codewords": [1024]},
        {"codewords": [True]},
        {"codewords": [1.0]},
        {"codewords": [float("nan")]},
        {"codewords": ["0000000000"]},
        {},
    ],
)
def test_invalid_or_noncovering_candidate_rejected(solution):
    with pytest.raises(ValueError):
        _validate(solution)


def test_claimed_scores_do_not_change_validation():
    solution = reference_run()
    expected = _validate(solution)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "fake")):
        assert validate({**solution, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_search_is_seeded_and_does_not_read_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "37")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first, second = baseline_run(), baseline_run()
    assert first == second
    assert first["search_metadata"]["reference_data_read"] is False
    _validate(first)


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T068 failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T068 failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
