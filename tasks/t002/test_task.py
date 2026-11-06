from tasks.t002.check import validate
import json
from pathlib import Path

CONFIG={'parameters':{'n':26}}
SEED=json.loads((Path(__file__).parent/'data'/'seed.json').read_text())

def test_grid_witness_and_exact_score():
    r=validate(SEED,CONFIG,strict=True)
    assert r['objective']=='6'
    assert r['verification_status']=='certified'
    assert r['details']['pair_checks']==325

def test_initializer_defaults_to_original_configuration(monkeypatch):
    monkeypatch.delenv('MATHBENCH_CONFIG_ID', raising=False)
    from tasks.t002.init_program import run_code
    assert validate(run_code(), CONFIG, strict=True)['objective'] == '6'

def test_human_entry_point_defaults_to_original_configuration(monkeypatch):
    monkeypatch.delenv('MATHBENCH_CONFIG_ID', raising=False)
    from tasks.t002.human import run_code
    assert validate(run_code(), CONFIG, strict=True)['objective'] == '7/2+3/2*sqrt2'

def test_claim_is_ignored():
    x={**SEED,'objective':1}
    assert validate(x,CONFIG)['objective']=='6'
    assert validate(x,CONFIG)['details']['claimed_objective_mismatch']

def test_rejects_wrong_count_and_config():
    with __import__('pytest').raises(ValueError): validate({'squares':SEED['squares'][:-1]},CONFIG)
    with __import__('pytest').raises(ValueError): validate(SEED,{'parameters':{'n':25}})

def test_rejects_overlap():
    x={'squares':[{'x':'1/2','y':'1/2','t':'0'} for _ in range(26)]}
    with __import__('pytest').raises(ValueError): validate(x,CONFIG)

def test_rational_rotation():
    # A single rotated corner set remains rational; duplicate 26 copies still collide.
    from tasks.t002.check import corners
    p=corners({'x':'0','y':'0','t':'1/2'})[0]
    assert (p[0].a,p[0].b,p[1].a,p[1].b)==(__import__('fractions').Fraction(1,10),0,__import__('fractions').Fraction(-7,10),0)

def test_rejects_bool_and_nonfinite():
    x={'squares':[dict(s) for s in SEED['squares']]}; x['squares'][0]['x']=True
    with __import__('pytest').raises(ValueError): validate(x,CONFIG)
    x={'squares':[dict(s) for s in SEED['squares']]}; x['squares'][0]['t']=float('inf')
    with __import__('pytest').raises(ValueError): validate(x,CONFIG)

def test_friedman_1997_reconstruction_exactly():
    human=json.loads((Path(__file__).parent/'data'/'human_friedman_1997.json').read_text())
    r=validate(human,CONFIG,strict=True)
    assert r['objective']=='7/2+3/2*sqrt2'
    assert r['details']['bounding_width']==r['details']['bounding_height']==r['objective']

import os
import pytest

@pytest.mark.parametrize(('n','cid','score','pairs'),[(29,'T002-C03','2966942899906512939318226046481160904289990651293931822604648091421/500000000000000000000000000000000000000000000000000000000000000000',406),(38,'T002-C04','6+1/2*sqrt2',703)])
def test_staged_expansion_human_witnesses(n,cid,score,pairs,monkeypatch):
    monkeypatch.setenv('MATHBENCH_CONFIG_ID',cid)
    from tasks.t002.human import run_code
    result=validate(run_code(),{'parameters':{'n':n}},strict=True)
    assert result['objective']==score
    assert result['verification_status']=='certified'
    assert result['details']['pair_checks']==pairs

def test_staged_initial_programs_are_valid(monkeypatch):
    from tasks.t002.init_program import run_code
    for n,cid in ((29,'T002-C03'),(38,'T002-C04')):
        monkeypatch.setenv('MATHBENCH_CONFIG_ID',cid)
        result=validate(run_code(),{'parameters':{'n':n}},strict=True)
        assert result['verification_status']=='certified'

def test_rejects_retired_n17():
    with pytest.raises(ValueError): validate({'squares':[]},{'parameters':{'n':17}})

@pytest.mark.parametrize(('n','cid'),[(29,'T002-C03'),(38,'T002-C04')])
def test_staged_claimed_scores_cannot_change_recomputed_objective(n,cid,monkeypatch):
    monkeypatch.setenv('MATHBENCH_CONFIG_ID',cid)
    from tasks.t002.human import run_code
    witness=run_code()
    actual=validate(witness,{'parameters':{'n':n}},strict=True)['objective']
    altered={**witness,'objective':-999}
    result=validate(altered,{'parameters':{'n':n}},strict=True)
    assert result['objective']==actual
    assert result['details']['claimed_objective_mismatch']
