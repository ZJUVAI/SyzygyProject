"""Exact tests for T067-C01."""

import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t067.check import PARAMETERS, validate


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T067-C01", "parameters": PARAMETERS}
WITNESS_SHA256 = "e278101d7c5496d890e87330df664e874225020ded21750515954e8b8a42219d"
SOURCE_SHA256 = "bc5261c3f1b9229985dcd4a95388bf15b42f9d657aa1fa55fd017121d255216a"


def _word(positions):
    return "".join("1" if i in positions else "0" for i in range(17))


def _independent_pair_check(words):
    ints = [int(word, 2) for word in words]
    count = 0
    minimum = 17
    for i, word in enumerate(ints):
        for other in ints[:i]:
            distance = (word ^ other).bit_count()
            assert distance >= 4
            minimum = min(minimum, distance)
            count += 1
    return count, minimum


def test_published_human_and_reference_witness_exactly_replay():
    from tasks.t067.human import run_code as human_run
    from tasks.t067.reference import run_code as reference_run

    witness_path = ROOT / "data/reference/a17_4_5_444.json"
    source_path = ROOT / "data/source/milshtein_a17_4_5_444.txt"
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == WITNESS_SHA256
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == SOURCE_SHA256
    human = human_run()
    assert reference_run() == human
    result = validate(human, CONFIG, strict=True)
    pairs, minimum = _independent_pair_check(human["codewords"])
    assert result["objective"] == len(human["codewords"]) == 444
    assert result["details"]["unordered_pairs_checked"] == pairs == 98_346
    assert result["details"]["minimum_pairwise_distance"] == minimum == 4


def test_all_five_entries_return_valid_candidates(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T067-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "7")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    monkeypatch.setenv("MATHBENCH_RESTARTS", "2")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_POPULATION", "2")
    from tasks.t067.init_program import run_code as initial
    from tasks.t067.baseline import run_code as baseline
    from tasks.t067.evolution import run_code as evolution
    from tasks.t067.human import run_code as human
    from tasks.t067.reference import run_code as reference

    results = [initial(), baseline(), evolution(), human(), reference()]
    values = [validate(result, CONFIG, strict=True)["objective"] for result in results]
    assert values[0] == 1
    assert values[1] >= 1
    assert values[2] >= 1
    assert values[3:] == [444, 444]
    assert results[1]["search_metadata"]["restarts_run"] == 2
    assert results[2]["search_metadata"]["generations_run"] == 2


def test_checker_accepts_pair_at_exact_minimum_distance_and_empty_boundary():
    a = _word({0, 1, 2, 3, 4})
    b = _word({0, 1, 2, 5, 6})
    result = validate({"codewords": [a, b]}, CONFIG)
    assert result["objective"] == 2
    assert result["details"]["minimum_pairwise_distance"] == 4
    assert validate({"codewords": []}, CONFIG)["objective"] == 0


def test_checker_rejects_bad_word_constraints_and_duplicates():
    with pytest.raises(ValueError, match="17-character"):
        validate({"codewords": ["101"]}, CONFIG)
    with pytest.raises(ValueError, match="weight 5"):
        validate({"codewords": ["0" * 17]}, CONFIG)
    duplicate = _word({0, 1, 2, 3, 4})
    with pytest.raises(ValueError, match="distinct"):
        validate({"codewords": [duplicate, duplicate]}, CONFIG)
    near = _word({0, 1, 2, 3, 5})
    far = _word({0, 1, 2, 3, 4})
    with pytest.raises(ValueError, match="distance at least 4"):
        validate({"codewords": [near, far]}, CONFIG)
    with pytest.raises(ValueError, match="configuration must fix"):
        validate({"codewords": []}, {"id": "T067-C01", "parameters": {**PARAMETERS, "length": 18}})


def test_checker_rejects_non_string_numeric_and_malformed_inputs():
    for invalid in (True, 3, 1.0, float("nan"), float("inf"), None, [0, 1]):
        with pytest.raises(ValueError):
            validate({"codewords": [invalid]}, CONFIG)
    with pytest.raises(ValueError, match="solution must be an object"):
        validate([_word({0, 1, 2, 3, 4})], CONFIG)
    with pytest.raises(ValueError, match="codewords must be"):
        validate({"codewords": "10101"}, CONFIG)


def test_claimed_scores_do_not_change_recomputed_result():
    from tasks.t067.init_program import run_code

    valid = run_code()
    result = validate(valid, CONFIG)
    for key, value in (("objective", 999), ("score", float("nan")),
                       ("claimed_score", {"forged": True})):
        assert validate({**valid, key: value}, CONFIG) == result


def test_sota_record_separates_verified_444_from_optimality_claim():
    metadata = json.loads((ROOT / "sota.json").read_text())
    record = json.loads((ROOT / "records.json").read_text())
    item = metadata["configurations"]["T067-C01"]
    assert item["public_value"] == item["reproduced_value"] == 444
    assert item["best_human"]["value"] == 444
    assert item["best_public"]["value"] == 444
    assert item["optimality_status"]["status"].startswith("open")
    assert record["configurations"]["T067-C01"]["frozen_human_baseline"]["value"] == 444


def test_runner_error_and_timeout_controls():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T067 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T067 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
