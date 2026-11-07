"""Tests for the fixed regular 120-gon dilation task."""

import copy
from fractions import Fraction
from decimal import Decimal, localcontext
import json
import os
from pathlib import Path
import sys
import time

import pytest

from tasks.t094 import baseline, check, evolution, human, init_program, reference


TASK = Path(__file__).resolve().parent
CONFIG = json.loads((TASK / "task.json").read_text(encoding="utf-8"))["configurations"][0]


def _crosses(a, b, c, d):
    if len({a, b, c, d}) < 4:
        return False
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c
    return (a < c < b) != (a < d < b)


def _independent_edges_check(edges):
    assert len(edges) == 237
    assert len({tuple(sorted(edge)) for edge in edges}) == 237
    edge_set = {tuple(sorted(edge)) for edge in edges}
    assert all(tuple(sorted((i, (i + 1) % 120))) in edge_set for i in range(120))
    diagonals = [edge for edge in edge_set if min((edge[0] - edge[1]) % 120, (edge[1] - edge[0]) % 120) != 1]
    for index, (a, b) in enumerate(diagonals):
        assert not any(_crosses(a, b, c, d) for c, d in diagonals[index + 1 :])


def test_all_program_entries_and_frozen_witness():
    outputs = [
        init_program.run_code(),
        baseline.run_code(),
        human.run_code(),
        reference.run_code(),
        evolution.run_code(),
    ]
    for result in outputs:
        checked = check.validate(result, CONFIG)
        assert checked["verification_status"] == "certified"
        lo, hi = checked["details"]["objective_interval"]
        assert Fraction(lo) <= Fraction(hi)
        _independent_edges_check(result["edges"])
    assert outputs[2] == outputs[3]
    assert outputs[1] == outputs[4]
    assert outputs[0]["edges"] != outputs[2]["edges"]
    assert baseline.run_code()["search_metadata"]["reference_data_read"] is False
    source_witness = json.loads((TASK / "data/source/ubc_6fan_120.json").read_text(encoding="utf-8"))
    assert outputs[2] == source_witness


def test_reference_interval_and_claim_fields_are_ignored():
    witness = human.run_code()
    expected = check.validate(witness, CONFIG)
    lower, upper = map(Fraction, expected["details"]["objective_interval"])
    assert lower <= Fraction(1449476373154, 10**12)
    assert upper < Fraction(1449476373155, 10**12)
    assert expected["details"]["claimed_objective_ignored"] is True
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "false")):
        forged = copy.deepcopy(witness)
        forged[key] = value
        assert check.validate(forged, CONFIG) == expected


@pytest.mark.parametrize(
    "edges",
    [
        None,
        [[0, 1]],
        [[0, 1], [0, 1]],
        [[True, 1]],
        [[0.0, 1]],
        [[0, 120]],
        [[3, 3]],
    ],
)
def test_invalid_edge_data_is_rejected(edges):
    with pytest.raises(ValueError):
        check.validate({"edges": edges}, CONFIG)


def test_crossing_diagonals_are_rejected():
    edges = copy.deepcopy(init_program.run_code()["edges"])
    edges.remove([0, 4])
    edges.append([1, 3])
    with pytest.raises(ValueError, match="cross"):
        check.validate({"edges": edges}, CONFIG)


def test_configuration_is_frozen():
    witness = init_program.run_code()
    variants = [
        {**CONFIG, "id": "T094-C02"},
        {**CONFIG, "parameters": {**CONFIG["parameters"], "vertices": 119}},
        {**CONFIG, "parameters": {**CONFIG["parameters"], "extra": True}},
        {**CONFIG, "parameters": {**CONFIG["parameters"], "vertices": 120.0}},
        {**CONFIG, "direction": "maximize"},
        {**CONFIG, "unexpected": 1},
    ]
    for config in variants:
        with pytest.raises(ValueError):
            check.validate(witness, config)


def _decimal_atan_inverse(q):
    x = Decimal(1) / Decimal(q)
    total = Decimal(0)
    term_power = x
    k = 0
    while True:
        term = term_power / Decimal(2 * k + 1)
        if term < Decimal("1e-105"):
            return total
        total += term if k % 2 == 0 else -term
        term_power *= x * x
        k += 1


def _decimal_pi():
    return Decimal(16) * _decimal_atan_inverse(5) - Decimal(4) * _decimal_atan_inverse(239)


def _decimal_sin(x):
    total = Decimal(0)
    term = x
    k = 0
    while abs(term) >= Decimal("1e-105"):
        total += term
        term *= -(x * x) / Decimal((2 * k + 2) * (2 * k + 3))
        k += 1
    return total


def test_chord_bounds_cover_independent_high_precision_values():
    with localcontext() as context:
        context.prec = 120
        sin_lower = check._sin_taylor(Fraction(1), 19)
        sin_upper = check._sin_taylor(Fraction(1), 18)
        sin_value = Fraction.from_decimal(_decimal_sin(Decimal(1)))
        assert sin_lower < sin_value < sin_upper
        pi = _decimal_pi()
        chords = check._chord_bounds()
        assert chords[60] == (2 * check.SCALE, 2 * check.SCALE)
        for k in range(1, 60):
            exact_approx = Fraction.from_decimal(
                Decimal(2) * _decimal_sin(pi * Decimal(k) / Decimal(120))
            )
            lower, upper = chords[k]
            assert Fraction(lower, check.SCALE) <= exact_approx <= Fraction(upper, check.SCALE)


def test_seeded_search_and_evolution_are_repeatable(monkeypatch):
    monkeypatch.setenv("T094_SEARCH_TRIALS", "1")
    monkeypatch.setenv("MATHBENCH_SEED", "37")
    first = baseline.run_code()
    second = baseline.run_code()
    assert first == second
    assert evolution.run_code() == first


def test_runner_program_error_and_timeout():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional failure')"], env, 5)
    started = time.monotonic()
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(5)"], env, 0.1)
    assert time.monotonic() - started < 3
