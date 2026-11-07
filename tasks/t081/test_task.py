"""Tests for the T081 exact planar-distance task."""

import copy
from fractions import Fraction as F
from functools import cmp_to_key
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import pytest

from tasks.t081 import baseline, check, evolution, human, init_program, reference


TASK = Path(__file__).resolve().parent
CONFIG = json.loads((TASK / "task.json").read_text())["configurations"][0]


def _add(x, y):
    return x[0] + y[0], x[1] + y[1]


def _sub(x, y):
    return x[0] - y[0], x[1] - y[1]


def _mul(x, y):
    return x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def _sign_sqrt3(value):
    a, b = value
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    if a > 0:
        difference = a * a - 3 * b * b
        return (difference > 0) - (difference < 0)
    difference = 3 * b * b - a * a
    return (difference > 0) - (difference < 0)


def _cmp_sqrt3(left, right):
    return _sign_sqrt3(_sub(left, right))


def _symbolic_rechenberg_points():
    zero = (F(0), F(0))
    one = (F(1), F(0))
    half = (F(1, 2), F(0))
    root3 = (F(0), F(1))
    rhalf = (F(0), F(1, 2))
    return [
        (zero, zero),
        (one, zero),
        (half, rhalf),
        (half, _add(one, rhalf)),
        (_sub(half, rhalf), _add(half, rhalf)),
        (_add(half, rhalf), _add(half, rhalf)),
        (_mul((-one[0], -one[1]), rhalf), half),
        (_mul((-one[0], -one[1]), rhalf), (F(-1, 2), F(0))),
        (zero, (F(-1), F(0))),
        (one, (F(-1), F(0))),
        (_add(one, rhalf), (F(-1, 2), F(0))),
        (_add(one, rhalf), half),
    ]


def test_all_five_entries_and_saved_baseline_are_valid(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T081-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    outputs = [
        init_program.run_code(),
        baseline.run_code(),
        human.run_code(),
        reference.run_code(),
        evolution.run_code(),
    ]
    values = [check.validate(output, CONFIG)["objective"] for output in outputs]
    assert values[0] == 13
    assert values[1] == values[4]
    assert F(values[1]) > 8
    assert values[2] == values[3]
    saved = json.loads((TASK / "best/seed-0.json").read_text())
    assert check.validate(saved, CONFIG)["objective"] == values[1]
    assert saved["points"] == outputs[1]["points"]
    assert outputs[1]["search_metadata"]["reference_data_read"] is False


def test_exact_qsqrt3_reconstruction_matches_public_report():
    points = _symbolic_rechenberg_points()
    distances = []
    for i in range(12):
        for j in range(i + 1, 12):
            dx = _sub(points[i][0], points[j][0])
            dy = _sub(points[i][1], points[j][1])
            distances.append(_add(_mul(dx, dx), _mul(dy, dy)))
    order = cmp_to_key(_cmp_sqrt3)
    minimum = min(distances, key=order)
    maximum = max(distances, key=order)
    assert minimum == (F(1), F(0))
    assert maximum == (F(5), F(2))
    assert distances.count(minimum) == 21
    rational_value = F(check.validate(human.run_code(), CONFIG)["objective"])
    assert _sign_sqrt3((rational_value - 5, F(-2))) > 0
    assert F(CONFIG["human_reference"]) > rational_value


def test_source_assets_are_frozen_and_the_page_reports_the_same_parameter():
    page = (TASK / "data/source/index.html").read_bytes()
    diagram = (TASK / "data/source/mm12.gif").read_bytes()
    assert hashlib.sha256(page).hexdigest() == (
        "2e4558ef1115ba5ca203fb0474a9dc8e4eb39558ff0c76e74e8feec84e98658e"
    )
    assert hashlib.sha256(diagram).hexdigest() == (
        "3b7ecd7f25e1253479bc997869642631a5c2c3a4ebba8e5f3de3b8d6e4a75c09"
    )
    assert b"<font size=+2>12.</font>" in page
    assert b"5 + 2&radic;3" in page
    assert b"Ingo Rechenberg" in page
    assert hashlib.sha256((TASK / "data/reference/rechenberg12_rational.json").read_bytes()).hexdigest() == (
        "ec135111b953a7eca739c733a3bdb4ee5d38fa7a90250d491220260e7b566e5b"
    )


def test_claimed_score_fields_cannot_change_exact_validation():
    solution = reference.run_code()
    expected = check.validate(solution, CONFIG, strict=True)
    for key in ("objective", "score", "claimed_score"):
        changed = copy.deepcopy(solution)
        changed[key] = "1/999999999999999999"
        assert check.validate(changed, CONFIG, strict=True) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


@pytest.mark.parametrize(
    "points",
    [
        [[i, 0] for i in range(11)],
        [[i, 0] for i in range(11)] + [[11, 0, 1]],
        [[i, 0] for i in range(11)] + [[True, 0]],
        [[i, 0] for i in range(11)] + [[float("nan"), 0]],
    ],
)
def test_invalid_point_lists_and_values_are_rejected(points):
    with pytest.raises(ValueError):
        check.validate({"points": points}, CONFIG)


@pytest.mark.parametrize("coordinate", [True, 0.5, float("nan"), "1/0", "1/-2"])
def test_rejects_nonrational_or_malformed_coordinates(coordinate):
    points = [[x, y] for y in range(3) for x in range(4)]
    points[0][0] = coordinate
    with pytest.raises(ValueError):
        check.validate({"points": points}, CONFIG)


def test_rejects_duplicate_points_and_accepts_unbounded_exact_coordinates():
    duplicate = [[x, y] for y in range(3) for x in range(4)]
    duplicate[-1] = duplicate[0]
    with pytest.raises(ValueError, match="coincide"):
        check.validate({"points": duplicate}, CONFIG)
    base = 10**5000
    collinear = [[str(base * x), "0"] for x in range(12)]
    assert check.validate({"points": collinear}, CONFIG)["objective"] == 121


def test_config_and_seed_are_fixed_and_reproducible(monkeypatch):
    with pytest.raises(ValueError):
        check.validate(init_program.run_code(), {**CONFIG, "id": "T081-C02"})
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T081-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "13")
    monkeypatch.setattr(baseline, "ITERATIONS", 50)
    assert baseline.run_code() == baseline.run_code()


def test_runner_errors_and_timeouts_use_shared_run_helper():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="T081 deliberate error"):
        _run([sys.executable, "-c", "raise RuntimeError('T081 deliberate error')"], env, 5)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
    assert time.monotonic() - start < 3
