from fractions import Fraction
from itertools import combinations

import pytest

from tasks.t005.check import validate
from tasks.t005.human import SOLUTION
from tasks.t005.task import run_code


CONFIG = {"id": "T005-C01", "parameters": {"n": 11}, "direction": "maximize", "human_reference": "1/27"}


def test_goldberg_witness_exact_score():
    result = validate(SOLUTION, CONFIG)
    assert result["objective"] == "1/27"
    assert result["verification_status"] == "exact"
    assert result["details"] == {"triangles_checked": 165}


def test_seed_is_valid_and_positive():
    assert Fraction(validate(run_code(), CONFIG)["objective"]) > 0


@pytest.mark.parametrize("bad", [
    {"points": [[0, 0]] * 11},
    {"points": [[-1, 0]] + [[i / 10, (i / 10) ** 2] for i in range(1, 11)]},
])
def test_invalid_inputs_rejected(bad):
    with pytest.raises(ValueError):
        validate(bad, CONFIG)

@pytest.mark.parametrize(("n", "score", "count"), [
    (12, "101871433411936556933637520697548102056943915772631725289/3125000000000000000000000000000000000000000000000000000000", 220),
    (16, "7/341", 560),
])
def test_expansion_human_witnesses_are_exact(n, score, count):
    from tasks.t005.human import SOLUTIONS
    result = validate(SOLUTIONS[n], {"parameters": {"n": n}})
    assert result["objective"] == score
    assert result["verification_status"] == "exact"
    assert result["details"]["triangles_checked"] == count
