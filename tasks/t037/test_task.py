import json
import os
from pathlib import Path
import sys

import pytest

from tasks.t037.check import validate
from tasks.t037.human import run_code as human_run
from tasks.t037.init_program import run_code as initial_run
from tasks.t037.reference import run_code as reference_run


TASK = json.loads((Path(__file__).parent / "task.json").read_text())
CONFIG = TASK["configurations"][0]


def test_d5_human_formula_recomputes_40_and_all_pair_constraints():
    result = validate(human_run(), CONFIG)
    assert result["objective"] == 40
    assert result["verification_status"] == "exact"
    assert result["details"]["pair_checks"] == 780


def test_simple_initial_program_is_valid():
    assert validate(initial_run(), CONFIG)["objective"] == 10


def test_exact_sixty_degree_boundary_is_allowed():
    dirs = [[1, 1, 0, 0, 0], [1, 0, 1, 0, 0]]
    assert validate({"directions": dirs}, CONFIG)["objective"] == 2


def test_angle_below_sixty_is_rejected():
    with pytest.raises(ValueError, match="less than 60"):
        validate({"directions": [[1, 0, 0, 0, 0], [2, 1, 0, 0, 0]]}, CONFIG)


def test_same_direction_under_positive_scaling_is_rejected():
    with pytest.raises(ValueError, match="less than 60"):
        validate({"directions": [[1, 2, 0, 0, 0], [2, 4, 0, 0, 0]]}, CONFIG)


@pytest.mark.parametrize("bad", [True, 1.25, float("nan"), float("inf"), "nan"])
def test_invalid_coordinates_rejected(bad):
    with pytest.raises(ValueError):
        validate({"directions": [[bad, 0, 0, 0, 0]]}, CONFIG)


@pytest.mark.parametrize("solution", [
    {"directions": [[0, 0, 0, 0, 0]]},
    {"directions": [[1, 0, 0, 0]]},
    {"directions": "invalid"},
])
def test_malformed_or_zero_vectors_rejected(solution):
    with pytest.raises(ValueError):
        validate(solution, CONFIG)


def test_reference_and_claimed_score_are_recomputed():
    candidate = reference_run()
    expected = validate(candidate, CONFIG)["objective"]
    candidate["claimed_score"] = 999999
    assert expected == 40
    assert validate(candidate, CONFIG)["objective"] == expected


def test_config_is_pinned():
    changed = dict(CONFIG)
    changed["parameters"] = dict(CONFIG["parameters"], dimension=6)
    with pytest.raises(ValueError):
        validate({"directions": []}, changed)


def test_generation_runner_reports_program_error_and_timeout():
    from mathbench.evaluate import _run

    environment = dict(os.environ)
    with pytest.raises(RuntimeError, match="candidate failure"):
        _run([sys.executable, "-c", "raise RuntimeError('candidate failure')"], environment, 2)
    with pytest.raises(TimeoutError, match="Wall time limit"):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], environment, 0.1)
