import copy
import hashlib
import json
import os
from pathlib import Path
import sys

import pytest

from mathbench.evaluate import _run
from tasks.t073.baseline import run_code as baseline_run
from tasks.t073.check import CONFIG_ID, PARAMETERS, validate
from tasks.t073.evolution import run_code as evolution_run
from tasks.t073.human import run_code as human_run
from tasks.t073.init_program import run_code as init_run
from tasks.t073.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _validate(solution):
    return validate(solution, CONFIG)


def test_all_five_entries_and_exact_human_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    solutions = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for solution in solutions:
        result = _validate(solution)
        assert result["verification_status"] == "exact"
        assert result["details"]["monomials_checked"] == 126
        assert result["objective"] == len(solution["points"])
    assert len(solutions[0]["points"]) == 96
    assert len(solutions[1]["points"]) == 24
    assert solutions[1] == solutions[2]
    assert solutions[3] == solutions[4]


def test_reference_is_pinned_and_independent_certificate_matches():
    metadata = json.loads((TASK / "sota.json").read_text())
    record = metadata["configurations"][CONFIG_ID]
    witness = TASK / record["witness"]
    human = TASK / "data/human/d4_24cell.json"
    assert hashlib.sha256(witness.read_bytes()).hexdigest() == record["witness_sha256"]
    assert hashlib.sha256(human.read_bytes()).hexdigest() == record["witness_sha256"]
    raw_certificate = TASK / "data/reference/d4_rational24_independent_certificate.json"
    raw_record = record["independent_certificate"]
    assert hashlib.sha256(raw_certificate.read_bytes()).hexdigest() == raw_record["sha256"]
    frozen = json.loads(witness.read_text())
    raw_points = json.loads(raw_certificate.read_text())["points"]
    normalized = [[[coordinate] for coordinate in point] for point in raw_points]
    assert frozen["points"] == normalized
    assert len(frozen["points"]) == 24


def test_generic_algebraic_coordinates_are_checked_exactly():
    initial = init_run()
    result = _validate(initial)
    assert result["objective"] == 96
    assert result["details"]["coordinate_field_degree"] == 2
    assert result["details"]["minimal_polynomial_irreducible"] is True


def test_duplicate_off_sphere_and_moment_perturbation_rejected():
    source = reference_run()
    duplicate = copy.deepcopy(source)
    duplicate["points"][1] = copy.deepcopy(duplicate["points"][0])
    with pytest.raises(ValueError, match="distinct"):
        _validate(duplicate)

    off_sphere = copy.deepcopy(source)
    off_sphere["points"][0][0] = ["0"]
    with pytest.raises(ValueError, match="unit sphere"):
        _validate(off_sphere)

    wrong_moment = copy.deepcopy(source)
    wrong_moment["points"][-1] = [["3/5"], ["4/5"], ["0"], ["0"]]
    with pytest.raises(ValueError, match="moment mismatch"):
        _validate(wrong_moment)


@pytest.mark.parametrize(
    "mutate",
    [
        lambda x: x.update(minimal_polynomial=[0, 0, 1]),
        lambda x: x.update(isolating_interval=["1", "2"]),
        lambda x: x["points"][0].__setitem__(0, [True]),
        lambda x: x["points"][0].__setitem__(0, [0.0]),
        lambda x: x["points"][0].__setitem__(0, [float("nan")]),
    ],
)
def test_invalid_field_or_coordinate_encoding_rejected(mutate):
    solution = copy.deepcopy(reference_run())
    mutate(solution)
    with pytest.raises(ValueError):
        _validate(solution)


def test_claimed_objective_does_not_change_validation():
    solution = reference_run()
    expected = _validate(solution)
    for key, value in (("objective", -3), ("score", float("nan")), ("claimed_score", "not-used")):
        assert validate({**solution, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T073 failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T073 failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
