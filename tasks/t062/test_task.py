import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t062.baseline import run_code as baseline_run
from tasks.t062.check import CONFIG_ID, N, PARAMETERS, validate
from tasks.t062.evolution import run_code as evolution_run
from tasks.t062.human import build_human_set, run_code as human_run
from tasks.t062.init_program import run_code as init_run
from tasks.t062.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _validate(solution):
    return validate(solution, CONFIG)


def test_all_five_entries_and_exact_reference_value(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("T062_SEARCH_TRIALS", "0")
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for solution in outputs:
        result = _validate(solution)
        assert result["verification_status"] == "exact"
        assert result["objective"] == len(solution["elements"])
    assert _validate(human_run())["objective"] == 2460
    assert _validate(reference_run())["objective"] == 2460


def test_human_formula_and_frozen_file_match():
    saved_path = TASK / "data/reference/lewko205_n42025.json"
    saved_bytes = saved_path.read_bytes()
    metadata = json.loads((TASK / "sota.json").read_text())
    record = metadata["configurations"][CONFIG_ID]
    assert hashlib.sha256(saved_bytes).hexdigest() == record["witness_sha256"]
    saved = json.loads(saved_bytes)
    assert saved == build_human_set()
    result = _validate(saved)
    assert result["objective"] == 2460
    assert min(saved["elements"]) == 8
    assert max(saved["elements"]) == 42020
    assert result["details"]["positive_square_translations_checked"] > 0


@pytest.mark.parametrize(
    "solution",
    [
        {"elements": [1, 1]},
        {"elements": [1, 2]},  # difference 1
        {"elements": [1, 5]},  # difference 4
        {"elements": [0]},
        {"elements": [N + 1]},
        {"elements": [True]},
        {"elements": [1.0]},
        {"elements": [float("nan")]},
        {"elements": None},
        {},
    ],
)
def test_invalid_or_forbidden_input_rejected(solution):
    with pytest.raises(ValueError):
        _validate(solution)


def test_claimed_scores_do_not_change_validation():
    solution = build_human_set()
    expected = _validate(solution)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "fake")):
        assert validate({**solution, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_search_is_seeded_and_does_not_read_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "18")
    monkeypatch.setenv("T062_SEARCH_TRIALS", "1")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first, second = baseline_run(), baseline_run()
    assert first == second
    assert first["search"]["reference_data_read"] is False
    _validate(first)


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T062 failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T062 failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
