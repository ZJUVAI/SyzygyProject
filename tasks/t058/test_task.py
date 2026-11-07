import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t058.baseline import run_code as baseline_run
from tasks.t058.check import CONFIG_ID, PARAMETERS, validate
from tasks.t058.evolution import run_code as evolution_run
from tasks.t058.human import build_schedule, run_code as human_run
from tasks.t058.init_program import run_code as init_run
from tasks.t058.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _check(rounds):
    return validate({"rounds": rounds}, CONFIG)


def _round_with_invalid_last_player(last):
    groups = [list(range(5))]
    groups.extend([list(range(5 * i, 5 * i + 5)) for i in range(1, 6)])
    groups.append([30, 31, 32, 33, last])
    return [groups]


def test_all_five_program_entries(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("T058_SEARCH_RESTARTS", "1")
    monkeypatch.setenv("T058_ATTEMPTS_PER_ROUND", "20")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for output in outputs:
        assert isinstance(output, dict)
        assert _check(output["rounds"])["objective"] == len(output["rounds"])
    assert _check(init_run()["rounds"])["objective"] == 1
    assert _check(human_run()["rounds"])["objective"] == 7
    assert _check(reference_run()["rounds"])["objective"] == 7


def test_reference_file_hash_and_exact_reconstruction():
    witness = TASK / "data/reference/rtd_5_7.json"
    assert hashlib.sha256(witness.read_bytes()).hexdigest() == json.loads(
        (TASK / "sota.json").read_text()
    )["configurations"][CONFIG_ID]["witness_sha256"]
    saved = json.loads(witness.read_text())
    assert saved["rounds"] == build_schedule()
    result = _check(saved["rounds"])
    assert result["objective"] == 7
    assert result["details"]["distinct_pairs_used"] == 490


def test_valid_alternate_one_round_construction():
    rounds = [[[5 * group + offset for offset in range(5)] for group in range(7)]]
    assert _check(rounds)["objective"] == 1


@pytest.mark.parametrize(
    "rounds",
    [
        [],
        [[ [0, 1, 2, 3, 4] ]],  # not seven groups
        [[list(range(5)) for _ in range(7)]],  # same players in every group
        _round_with_invalid_last_player(99),
        _round_with_invalid_last_player(True),
        _round_with_invalid_last_player(34.0),
        _round_with_invalid_last_player(float("nan")),
    ],
)
def test_invalid_rounds_rejected(rounds):
    with pytest.raises(ValueError):
        _check(rounds)


def test_repeated_pair_rejected():
    rounds = build_schedule()
    rounds[1] = [group[:] for group in rounds[0]]
    with pytest.raises(ValueError, match="meet more than once"):
        _check(rounds)


def test_upper_bound_enforced():
    rounds = build_schedule() + [build_schedule()[0]] * 2
    with pytest.raises(ValueError, match="upper bound"):
        _check(rounds)


def test_claimed_scores_do_not_affect_validation():
    rounds = build_schedule()
    expected = validate({"rounds": rounds}, CONFIG)
    for key, value in (("objective", -100), ("score", float("nan")), ("claimed_score", "8")):
        assert validate({"rounds": rounds, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_fixed_baseline_is_deterministic_and_search_does_not_read_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_SEED", "12")
    monkeypatch.setenv("T058_SEARCH_RESTARTS", "3")
    monkeypatch.setenv("T058_ATTEMPTS_PER_ROUND", "50")
    one = baseline_run()
    two = baseline_run()
    assert one == two
    assert one["search"]["reference_data_read"] is False
    _check(one["rounds"])


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional task failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional task failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
