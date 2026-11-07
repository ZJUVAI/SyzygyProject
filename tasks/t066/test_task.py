import hashlib
import json
import os
from pathlib import Path
import sys
from fractions import Fraction

import pytest

from mathbench.evaluate import _run
from tasks.t066.algebra import add, mul, sub, zero
from tasks.t066.baseline import run_code as baseline_run
from tasks.t066.check import CONFIG_ID, PARAMETERS, validate
from tasks.t066.evolution import run_code as evolution_run
from tasks.t066.human import DEGREE, MODULUS, build_human_orchard, run_code as human_run
from tasks.t066.init_program import run_code as init_run
from tasks.t066.reference import run_code as reference_run


TASK = Path(__file__).parent
CONFIG = {"id": CONFIG_ID, "parameters": PARAMETERS}


def _validate(solution):
    return validate(solution, CONFIG)


def test_all_five_entries_and_reproduced_score(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "0")
    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    for solution in outputs:
        checked = _validate(solution)
        assert checked["verification_status"] == "exact"
        assert isinstance(checked["objective"], int)
    assert _validate(human_run())["objective"] == 40
    assert _validate(reference_run())["objective"] == 40


def test_frozen_reference_matches_formula_and_hash():
    path = TASK / "data/reference/cubic_tangent_17.json"
    raw = path.read_bytes()
    metadata = json.loads((TASK / "sota.json").read_text())
    record = metadata["configurations"][CONFIG_ID]
    assert hashlib.sha256(raw).hexdigest() == record["witness_sha256"]
    saved = json.loads(raw)
    assert saved == build_human_orchard()
    assert _validate(saved)["objective"] == 40


def test_independent_determinant_identity_and_zero_sum_count():
    witness = build_human_orchard()
    assert len(witness["points"]) == 17
    exact = []
    for point in witness["points"]:
        exact.append((
            tuple(Fraction(v) for v in point["x"]),
            tuple(Fraction(v) for v in point["y"]),
        ))
    zero_element = zero(DEGREE)
    collinear = set()
    for i in range(17):
        for j in range(i + 1, 17):
            for k in range(j + 1, 17):
                xi, yi = exact[i]
                xj, yj = exact[j]
                xk, yk = exact[k]
                det = sub(
                    mul(sub(xj, xi), sub(yk, yi), MODULUS),
                    mul(sub(yj, yi), sub(xk, xi), MODULUS),
                )
                if det == zero_element:
                    collinear.add((i, j, k))
    expected = {
        (i, j, k)
        for i in range(17)
        for j in range(i + 1, 17)
        for k in range(j + 1, 17)
        if (i + j + k) % 17 == 0
    }
    assert len(expected) == 40
    assert collinear == expected


def test_a_line_with_more_than_three_points_does_not_count():
    solution = {
        "minimal_polynomial": [0, 1],
        "isolating_interval": ["-1", "1"],
        "points": [{"x": [i], "y": [0]} for i in range(17)],
    }
    checked = _validate(solution)
    assert checked["objective"] == 0
    assert checked["details"]["largest_line_incidence"] == 17


def test_large_exact_integer_coordinates_have_no_precision_cap():
    large = 10 ** 5000
    solution = {
        "minimal_polynomial": [0, 1],
        "isolating_interval": ["-1", "1"],
        "points": [{"x": [str(large + i)], "y": [i * i]} for i in range(17)],
    }
    checked = _validate(solution)
    assert checked["verification_status"] == "exact"


@pytest.mark.parametrize(
    "solution",
    [
        {"minimal_polynomial": [0, 1], "isolating_interval": ["-1", "1"], "points": [{"x": [0], "y": [0]}] * 17},
        {"minimal_polynomial": [0, 1], "isolating_interval": ["-1", "1"], "points": [{"x": [True], "y": [0]} for _ in range(17)]},
        {"minimal_polynomial": [0, 1], "isolating_interval": ["-1", "1"], "points": [{"x": [float("nan")], "y": [0]} for _ in range(17)]},
        {"minimal_polynomial": [0, 2], "isolating_interval": ["-1", "1"], "points": [{"x": [i], "y": [i * i]} for i in range(17)]},
        {"minimal_polynomial": [-1, 0, 1], "isolating_interval": ["0", "2"], "points": [{"x": [i], "y": [i * i]} for i in range(17)]},
        {"minimal_polynomial": [-2, 0, 1], "isolating_interval": ["-2", "2"], "points": [{"x": [i], "y": [i * i]} for i in range(17)]},
        {"minimal_polynomial": [0, 1], "isolating_interval": ["1", "1"], "points": [{"x": [i], "y": [i * i]} for i in range(17)]},
        {"minimal_polynomial": [0, 1], "isolating_interval": ["-1", "1"], "points": [{"x": [i], "y": [i * i]} for i in range(16)]},
    ],
)
def test_invalid_constructions_rejected(solution):
    with pytest.raises(ValueError):
        _validate(solution)


def test_claimed_scores_do_not_change_validation():
    solution = build_human_orchard()
    expected = _validate(solution)
    for key, value in (("objective", -1), ("score", float("nan")), ("claimed_score", "fake")):
        assert validate({**solution, key: value}, CONFIG) == expected
    assert expected["details"]["claimed_objective_ignored"] is True


def test_search_is_seeded_and_does_not_read_reference(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", CONFIG_ID)
    monkeypatch.setenv("MATHBENCH_SEED", "23")
    monkeypatch.delenv("MATHBENCH_SEARCH_SECONDS", raising=False)
    first, second = baseline_run(), baseline_run()
    assert first == second
    assert first["search_metadata"]["reference_data_read"] is False
    _validate(first)


def test_runner_error_and_timeout_without_registry():
    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T066 failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T066 failure')"], env, 3)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(10)"], env, 0.2)
