from fractions import Fraction

import pytest

from tasks.t014.check import validate
from tasks.t014.human import run_code as human_run_code
from tasks.t014.init_program import run_code as init_run_code


CONFIG = {"id": "T014-C01", "parameters": {"n": 11}, "direction": "maximize", "human_reference": 1 / 27}


def test_public_human_witness():
    result = validate(human_run_code(), CONFIG)
    assert result == {"objective": "1/27", "verification_status": "exact", "details": {"triangles_checked": 165}}


def test_initializer_has_positive_exact_score():
    assert Fraction(validate(init_run_code(), CONFIG)["objective"]) > 0


@pytest.mark.parametrize("points", [
    [[0, 0]] * 11,
    [[True, 0]] + [[i / 10, (i / 10) ** 2] for i in range(1, 11)],
    [[float("nan"), 0]] + [[i / 10, (i / 10) ** 2] for i in range(1, 11)],
    [[-1, 0]] + [[i / 10, (i / 10) ** 2] for i in range(1, 11)],
])
def test_invalid_points_rejected(points):
    with pytest.raises(ValueError):
        validate({"points": points, "claimed_score": "999"}, CONFIG)


def test_zero_minimum_area_is_valid():
    points = [[i / 10, 0] for i in range(11)]
    assert validate(points, CONFIG)["objective"] == "0"
