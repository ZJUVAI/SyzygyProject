from fractions import Fraction
import math
import pytest

from tasks.t016.check import validate
from tasks.t016.human import run_code as human_program

CONFIG = {
    "id": "T016-C01",
    "parameters": {
        "steps": 208,
        "support": ["-1/4", "1/4"],
        "signed_values_allowed": True,
        "integral": 1,
    },
}


def test_human_witness_exact_score_and_signed_admissibility():
    result = validate(human_program(), CONFIG, strict=True)
    assert result["verification_status"] == "exact"
    assert result["objective"] == "6280435861361744576/4160000022692211721"
    assert math.isclose(float(Fraction(result["objective"])), 1.5097201507458786, rel_tol=0, abs_tol=1e-15)


def test_signed_coefficients_and_negative_mass_are_valid():
    coeff = [0] * 208
    coeff[0], coeff[1] = 2, -1
    result = validate({"coefficients": coeff}, CONFIG)
    assert Fraction(result["objective"]) == 1664
    assert result["details"]["max_abs_indices"]
    # Scaling by a negative nonzero constant leaves the objective unchanged.
    scaled = validate({"coefficients": [-2 * x for x in coeff]}, CONFIG)
    assert scaled["objective"] == result["objective"]


def test_single_nonzero_boundary_coefficient():
    coeff = [0] * 208
    coeff[-1] = "-3/7"
    assert validate({"coefficients": coeff}, CONFIG)["objective"] == "416"


@pytest.mark.parametrize("coeff", [None, [1] * 207, [1] * 209, [True] + [0] * 207,
                                    [float("nan")] + [0] * 207, [float("inf")] + [0] * 207,
                                    ["1/0"] + [0] * 207, ["oops"] + [0] * 207,
                                    [0] * 208])
def test_invalid_coefficients_rejected(coeff):
    with pytest.raises(ValueError):
        validate({"coefficients": coeff}, CONFIG)


def test_configuration_mismatch_rejected():
    bad = {"parameters": dict(CONFIG["parameters"], steps=150)}
    with pytest.raises(ValueError):
        validate({"coefficients": [1] * 208}, bad)


def test_claimed_score_is_ignored_and_score_is_independently_computed():
    coeff = [0] * 208
    coeff[0] = 1
    coeff[1] = 1
    result = validate({"coefficients": coeff, "objective": -999999}, CONFIG)
    assert Fraction(result["objective"]) == Fraction(416 * 2, 4)
    assert result["objective"] != -999999
