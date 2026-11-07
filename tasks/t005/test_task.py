from fractions import Fraction

import pytest

from tasks.t005.check import validate
from tasks.t005.human import run_code as human_run_code
from tasks.t005.init_program import run_code as init_run_code


CONFIG = {"id": "T005-C01", "parameters": {"n": 11}, "direction": "maximize", "human_reference": 1 / 27}


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


def test_area_gradient_matches_difference(monkeypatch):
    import numpy as np
    from tasks.t005 import evolution
    captured=[]
    def inspect(fun,x0,**kwargs):
        constraint=kwargs['constraints'][0]
        z=x0.copy(); eps=1e-6
        analytic=constraint['jac'](z)
        numeric=np.empty_like(analytic)
        for i in range(len(z)):
            delta=np.zeros_like(z); delta[i]=eps
            numeric[:,i]=(constraint['fun'](z+delta)-constraint['fun'](z-delta))/(2*eps)
        assert np.allclose(analytic,numeric,atol=1e-8)
        captured.append(True)
        raise evolution._DeadlineReached
    monkeypatch.setattr(evolution,'minimize',inspect)
    monkeypatch.setenv('MATHBENCH_CONFIG_ID','T005-C01')
    monkeypatch.delenv('MATHBENCH_WARM_START',raising=False)
    evolution.run_code()
    assert captured
