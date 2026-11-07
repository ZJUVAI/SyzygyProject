"""Exact PSD, norm-interval, source, and runner tests for T086."""

import json
import os
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import sys

import pytest

from tasks.t086.check import PARAMETERS, validate


ROOT = Path(__file__).resolve().parent
CONFIG = {"id": "T086-C01", "parameters": PARAMETERS}
WITNESS_SHA256 = "ed32b4e108875d14fdb1aec7308b6ebe902c95c9004bb3bdc5a155a1d0018eb7"


def _identity():
    return [
        [[1, 0], [0, 0], [0, 0]],
        [[0, 0], [1, 0], [0, 0]],
        [[0, 0], [0, 0], [1, 0]],
    ]


def _diagonal(values):
    return [[[values[r] if r == c else 0, 0] for c in range(3)] for r in range(3)]


def _identity_candidate():
    return {"matrices": [_identity() for _ in range(4)]}


def test_identity_human_baseline_is_exactly_one():
    from tasks.t086.human import run_code as human_run
    from tasks.t086.reference import run_code as reference_run

    witness_path = ROOT / "data/reference/identity_psd_n4_d3.json"
    import hashlib
    assert hashlib.sha256(witness_path.read_bytes()).hexdigest() == WITNESS_SHA256
    human = human_run()
    reference = reference_run()
    assert human == reference == json.loads(witness_path.read_text())
    result = validate(human, CONFIG, strict=True)
    assert result["objective"] == "1"
    assert result["details"]["objective_interval"] == ["1", "1"]
    assert result["details"]["common_product_norm_squared"] == "3"
    assert result["details"]["products_with_replacement"] == 256
    assert result["details"]["products_without_replacement"] == 24


def test_exact_interval_contains_independently_recomputed_diagonal_ratio():
    candidate = {"matrices": [_diagonal([2, 1, 1]), _identity(), _identity(), _identity()]}
    result = validate(candidate, CONFIG)
    lo, hi = map(Fraction, result["details"]["objective_interval"])
    with localcontext() as ctx:
        ctx.prec = 110
        numerator = Decimal(0)
        from math import comb
        for k in range(5):
            norm_squared = Decimal(4**k + 2)
            term = norm_squared.sqrt() * comb(4, k) * (3 ** (4 - k))
            numerator += term
        numerator /= 256
        denominator = Decimal(6).sqrt()
        true_ratio = numerator / denominator
        true_fraction = Fraction(str(true_ratio))
        assert lo <= true_fraction <= hi
    assert result["verification_status"] == "certified"
    assert lo <= Fraction(result["objective"]) == hi
    assert hi - lo < Fraction(1, 10**30)


def test_complex_hermitian_psd_input_is_supported():
    complex_psd = [
        [[1, 0], [0, "1/2"], [0, 0]],
        [[0, "-1/2"], [1, 0], [0, 0]],
        [[0, 0], [0, 0], [1, 0]],
    ]
    result = validate({"matrices": [complex_psd, _identity(), _identity(), _identity()]}, CONFIG)
    assert Fraction(result["details"]["objective_interval"][0]) <= Fraction(result["objective"])
    assert result["details"]["psd_verified_by_all_principal_minors"] is True
    assert result["details"]["without_replacement_denominator_positive"] is True


def test_high_precision_rational_inputs_are_not_artificially_capped():
    eps = f"1/{10**100}"
    # Use explicit fractions; do not route decimal floating-point values through the checker.
    matrices = [_diagonal([f"{k}/{10**100}", eps, eps]) for k in range(1, 5)]
    result = validate({"matrices": matrices}, CONFIG)
    assert result["details"]["sqrt_interval_decimal_scale"] != "1000000000000000000000000000000000000"
    assert Fraction(result["details"]["objective_interval"][0]) <= Fraction(result["objective"])
    assert Fraction(result["objective"]) > 0


def test_psd_checker_rejects_nonhermitian_and_negative_principal_minors():
    invalid_matrices = []
    invalid_matrices.append([[[ -1, 0], [0, 0], [0, 0]], [[0, 0], [1, 0], [0, 0]], [[0, 0], [0, 0], [1, 0]]])
    invalid_matrices.append([[[1, 0], [0, 1], [0, 0]], [[0, 0], [1, 0], [0, 0]], [[0, 0], [0, 0], [1, 0]]])
    invalid_matrices.append([[[1, 0], [2, 0], [0, 0]], [[2, 0], [1, 0], [0, 0]], [[0, 0], [0, 0], [1, 0]]])
    indefinite = [
        [[1, 0], ["9/10", 0], ["9/10", 0]],
        [["9/10", 0], [1, 0], ["-9/10", 0]],
        [["9/10", 0], ["-9/10", 0], [1, 0]],
    ]
    invalid_matrices.append(indefinite)
    for matrix in invalid_matrices:
        with pytest.raises(ValueError):
            validate({"matrices": [matrix, _identity(), _identity(), _identity()]}, CONFIG)


def test_input_shape_exact_coefficients_and_denominator_conditions():
    candidate = _identity_candidate()
    for bad_value in (True, 1.0, float("nan"), float("inf"), None, "not-rational"):
        bad = _identity_candidate()
        bad["matrices"][0][0][0][0] = bad_value
        with pytest.raises(ValueError):
            validate(bad, CONFIG)
    with pytest.raises(ValueError, match="exactly four"):
        validate({"matrices": candidate["matrices"][:3]}, CONFIG)
    with pytest.raises(ValueError, match="three rows"):
        validate({"matrices": [[_identity()[0], _identity()[1]], _identity(), _identity(), _identity()]}, CONFIG)
    zero = _diagonal([0, 0, 0])
    with pytest.raises(ValueError, match="without-replacement mean norm must be positive"):
        validate({"matrices": [zero, _identity(), _identity(), _identity()]}, CONFIG)


def test_claimed_score_changes_do_not_change_recomputed_result():
    candidate = _identity_candidate()
    expected = validate(candidate, CONFIG)
    for key, value in (("objective", "-999"), ("score", float("nan")), ("claimed_score", {"fake": True})):
        assert validate({**candidate, key: value}, CONFIG) == expected


def test_all_five_programs_produce_psd_candidates(monkeypatch):
    monkeypatch.setenv("MATHBENCH_CONFIG_ID", "T086-C01")
    monkeypatch.setenv("MATHBENCH_SEED", "12")
    monkeypatch.setenv("MATHBENCH_BASELINE_ITERATIONS", "4")
    monkeypatch.setenv("MATHBENCH_EVOLUTION_ITERATIONS", "2")
    monkeypatch.setenv("MATHBENCH_POPULATION", "3")
    from tasks.t086.init_program import run_code as init_run
    from tasks.t086.baseline import run_code as baseline_run
    from tasks.t086.evolution import run_code as evolution_run
    from tasks.t086.human import run_code as human_run
    from tasks.t086.reference import run_code as reference_run

    outputs = [init_run(), baseline_run(), evolution_run(), human_run(), reference_run()]
    results = [validate(output, CONFIG, strict=True) for output in outputs]
    assert all(result["verification_status"] == "certified" for result in results)
    assert results[0]["objective"] == "1"
    assert results[3]["objective"] == results[4]["objective"] == "1"
    assert outputs[1]["search_metadata"]["iterations_run"] == 4
    assert outputs[2]["search_metadata"]["generations_run"] == 2


def test_sota_and_records_track_exact_identity_score():
    sota = json.loads((ROOT / "sota.json").read_text())
    records = json.loads((ROOT / "records.json").read_text())
    result = validate(_identity_candidate(), CONFIG)
    item = sota["configurations"]["T086-C01"]
    record = records["configurations"]["T086-C01"]
    assert item["reproduced_value"] == result["objective"] == "1"
    assert item["public_value"] == item["best_human"]["value"] == 1
    assert item["best_reproduced"]["objective_interval"] == ["1", "1"]
    assert record["best_reproduced"]["value"] == "1"
    assert item["ai_assisted_search_report"]["reported_reference_bound"] == 1


def test_runner_error_and_timeout_paths():
    from mathbench.evaluate import _run

    env = dict(os.environ)
    with pytest.raises(RuntimeError, match="intentional T086 worker failure"):
        _run([sys.executable, "-c", "raise RuntimeError('intentional T086 worker failure')"], env, 5)
    with pytest.raises(TimeoutError):
        _run([sys.executable, "-c", "import time; time.sleep(2)"], env, 0.1)
