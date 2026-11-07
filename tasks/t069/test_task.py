import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t069.baseline import run_code as baseline_run
from tasks.t069.check import (
    CONFIG_ID,
    INSTANCE_SHA256,
    PARAMETERS,
    TOUR_SHA256,
    edge_length,
    load_points,
    validate,
)
from tasks.t069.evolution import run_code as evolution_run
from tasks.t069.human import run_code as human_run
from tasks.t069.init_program import run_code as init_run
from tasks.t069.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _validate(solution):
    return validate(solution, CONFIG)


def test_five_entries_and_public_tour_recompute(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    solutions = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    objectives = []
    for solution in solutions:
        checked = _validate(solution)
        assert checked["verification_status"] == "exact"
        assert checked["details"]["unique_city_count"] == 100_000
        objectives.append(checked["objective"])
    assert objectives[3:] == [5_757_191, 5_757_191]
    assert solutions[1] == solutions[2]
    assert solutions[1]["search_metadata"]["reference_data_read"] is False


def test_pinned_inputs_and_witness_hashes():
    metadata = json.loads((TASK / "sota.json").read_text())
    record = metadata["configurations"][CONFIG_ID]
    instance = TASK / record["instance_file"]
    reference = TASK / record["witness"]
    human = TASK / "data/human/monalisa_5757191.tour"
    assert hashlib.sha256(instance.read_bytes()).hexdigest() == INSTANCE_SHA256
    assert hashlib.sha256(instance.read_bytes()).hexdigest() == record["instance_sha256"]
    assert hashlib.sha256(reference.read_bytes()).hexdigest() == record["witness_sha256"]
    assert hashlib.sha256(reference.read_bytes()).hexdigest() == TOUR_SHA256
    assert hashlib.sha256(human.read_bytes()).hexdigest() == TOUR_SHA256
    assert len(load_points()) == 100_000


def test_integer_euc2d_distance_rounding():
    assert edge_length(((0, 0), (3, 4)), 0, 1) == 5
    assert edge_length(((0, 0), (1, 1)), 0, 1) == 1
    assert edge_length(((0, 0), (2, 2)), 0, 1) == 3


@pytest.mark.parametrize("kind", ["duplicate", "negative", "too_large", "bool", "float", "nan", "short"])
def test_invalid_tours_rejected(kind):
    tour = list(range(100_000))
    if kind == "duplicate":
        tour[-1] = tour[0]
    elif kind == "negative":
        tour[-1] = -1
    elif kind == "too_large":
        tour[-1] = 100_000
    elif kind == "bool":
        tour[10] = True
    elif kind == "float":
        tour[10] = 1.0
    elif kind == "nan":
        tour[10] = float("nan")
    elif kind == "short":
        tour.pop()
    with pytest.raises(ValueError):
        _validate({"tour": tour})


def test_claimed_scores_never_change_result(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    solution = reference_run()
    expected = _validate(solution)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "fake")):
        assert validate({**solution, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_score_ignored"] is True


def test_baseline_seed_is_repeatable(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "21")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    assert baseline_run() == baseline_run()


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T069 failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T069 failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
