"""Independent experiment audit must reject a damaged saved witness."""
from copy import deepcopy
from fractions import Fraction
import pytest
from scripts.run_t003_evolution import independent_audit
from tasks.t003.init_program import run_code


def test_independent_audit(monkeypatch):
    monkeypatch.setenv('MATHBENCH_CONFIG_ID', 'T003-C01')
    solution = run_code()
    solution['objective'] = '999'
    assert independent_audit(solution)['objective'] == str(Fraction(26, 12))
    damaged = deepcopy(solution)
    damaged['circles'][1] = dict(damaged['circles'][0])
    with pytest.raises(ValueError, match='feasibility'):
        independent_audit(damaged)
    damaged = deepcopy(solution)
    damaged['circles'][0]['x'] = '0'
    with pytest.raises(ValueError, match='feasibility'):
        independent_audit(damaged)
