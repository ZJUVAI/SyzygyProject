import json
import os
from pathlib import Path

import pytest

from tasks.t010.check import validate

ROOT=Path(__file__).parent
CASES=(('T010-C02',23,10,84,16),('T010-C03',25,10,196,64))

def config(cid,n,d): return {'id':cid,'parameters':{'n':n,'distance':d}}

@pytest.mark.parametrize('cid,n,d,size,human_size',CASES)
def test_saved_public_and_human_constructions(cid,n,d,size,human_size,monkeypatch):
    monkeypatch.setenv('MATHBENCH_CONFIG_ID',cid)
    suffix=n
    public=json.loads((ROOT/'data'/f'parity_extended_{n}_{size}_{d}.json').read_text())['codewords']
    human=json.loads((ROOT/'data'/f'bch_shortened_{n}.json').read_text())['codewords']
    c=config(cid,n,d)
    checked=validate({'codewords':public,'objective':-1},c)
    assert (checked['objective'],checked['details']['minimum_pairwise_distance'])==(size,d)
    assert checked['details']['pairs_checked']==size*(size-1)//2
    assert checked==validate({'codewords':public,'objective':size**4},c)
    h=validate({'codewords':human},c)
    assert h['objective']==human_size and h['details']['minimum_pairwise_distance']>=d

@pytest.mark.parametrize('cid,n,d,size,human_size',CASES)
def test_all_programs_and_cold_start(cid,n,d,size,human_size,monkeypatch):
    monkeypatch.setenv('MATHBENCH_CONFIG_ID',cid)
    monkeypatch.setenv('MATHBENCH_BASELINE_TRIALS','25')
    from tasks.t010 import baseline,evolution,human,init_program,reference,sota
    c=config(cid,n,d)
    assert validate(init_program.run_code(),c)['objective']==1
    assert validate(human.run_code(),c)['objective']==human_size
    assert validate(reference.run_code(),c)['objective']==size
    assert validate(sota.run_code(),c)['objective']==size
    assert validate(baseline.run_code(),c)['verification_status']=='exact'
    assert validate(evolution.run_code(),c)['verification_status']=='exact'

@pytest.mark.parametrize('n,d',[(23,10),(25,10)])
def test_rejects_damaged_words_and_duplicates(n,d):
    c={'parameters':{'n':n,'distance':d}}
    with pytest.raises(ValueError): validate({'codewords':[0,1]},c)
    with pytest.raises(ValueError): validate({'codewords':[0,0]},c)

def test_config_metadata_and_source_counts():
    task=json.loads((ROOT/'task.json').read_text())
    assert [(c['parameters']['n'],c['parameters']['distance']) for c in task['configurations'][-2:]]==[(23,10),(25,10)]
    assert [c['acceptance_status'] for c in task['configurations'][-2:]]==['accepted_by_sol']*2
    for n,count,d in ((22,84,9),(24,196,9)):
        words=list(map(int,(ROOT/'data'/f'source_{n}_{count}_{d}.txt').read_text().split()))
        assert len(words)==count and len(set(words))==count
        assert min((a^b).bit_count() for i,a in enumerate(words) for b in words[i+1:])==d
