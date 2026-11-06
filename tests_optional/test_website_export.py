"""Check website evidence mapping and numeric drawing projections."""
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'website/dist/data'
spec=importlib.util.spec_from_file_location('website_export',ROOT/'scripts/export_website.py')
exporter=importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


def read_asset(path):
    return json.loads((ROOT/'website/dist'/path).read_text())


def test_website_scores_and_raw_witnesses_match_accepted_evidence():
    source=json.loads((ROOT/'reports/acceptance.json').read_text())
    index=json.loads((DATA/'index.json').read_text())
    assert index['counts']=={'tasks':20,'configurations':35,'runs':140,'categories':10}
    assert index['full_llm_experiments'] is False
    count=0
    for task, original in zip(index['tasks'],source['tasks']):
        assert task['id']==original['task_id']
        for cfg in task['configurations']:
            detail=read_asset(cfg['asset'])
            expected={r['program']:r for r in original['runs'] if r['config_id']==cfg['id']}
            assert len(detail['runs'])==4
            for run in detail['runs']:
                r=expected[run['program']]
                assert run['objective']==str(r['objective'])
                assert run['combined_score']==r['combined_score']
                assert run['verification_status']==r['verification_status']
                assert read_asset(run['result'])==r
                raw=ROOT/'reports/witnesses'/task['id']/cfg['id']/run['program']/'solution.json'
                assert (ROOT/'website/dist'/run['witness']).read_bytes()==raw.read_bytes()
                assert read_asset(run['visual'])['kind']
                count+=1
    assert count==140


def test_manifest_and_deduplication():
    manifest=json.loads((DATA/'manifest.json').read_text())
    for path,digest in manifest.items():
        assert hashlib.sha256((DATA/path).read_bytes()).hexdigest()==digest
    cfg=json.loads((DATA/'configurations/T002-C04.json').read_text())
    runs={r['program']:r for r in cfg['runs']}
    assert runs['human']['witness']==runs['reference']['witness']
    assert runs['human']['visual']==runs['reference']['visual']


def test_large_integers_remain_exact():
    x=2**521-3
    assert exporter.safe_integers({'chain':[1,x]})=={'chain':[1,str(x)]}
    cfg=json.loads((DATA/'configurations/T097-C03.json').read_text())
    v=read_asset(next(r for r in cfg['runs'] if r['program']=='human')['visual'])
    assert v['exact'][-1]==str(x)
    assert v['bits'][-1]==521
    for i,pair in enumerate(v['dependencies'][1:],1):
        assert sum(int(v['exact'][j]) for j in pair)==int(v['exact'][i])


def test_square_projection_matches_independent_exact_corners():
    import sympy as sp
    cfg=json.loads((DATA/'configurations/T002-C04.json').read_text())
    run=next(r for r in cfg['runs'] if r['program']=='human')
    raw=read_asset(run['witness']);v=read_asset(run['visual'])
    for square,polygon in zip(raw['squares'],v['polygons']):
        x,y,t=[sp.sympify(square[k],locals={'sqrt2':sp.sqrt(2)}) for k in ['x','y','t']]
        c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
        expected=[(float(x+i*c/2-j*s/2),float(y+i*s/2+j*c/2)) for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        for a,b in zip(expected,polygon):assert a==pytest.approx(b)


def test_ruler_differences_and_labs_energy():
    for cid in ['T044-C02','T073-C02']:
        cfg=json.loads((DATA/'configurations'/f'{cid}.json').read_text())
        run=next(r for r in cfg['runs'] if r['program']=='human');v=read_asset(run['visual']);s=read_asset(run['witness'])
        if cid.startswith('T044'):
            assert all(v['matrix'][i][j]==abs(a-b) for i,a in enumerate(s['marks']) for j,b in enumerate(s['marks']))
            assert len({v['matrix'][i][j] for i in range(30) for j in range(i)})==435
        else:
            a=s['sequence'];correlations=[sum(a[i]*a[i+k] for i in range(len(a)-k)) for k in range(1,len(a))]
            assert v['correlation']==correlations
            assert sum(x*x for x in correlations)==int(run['objective'])==352


def test_full_overlap_curve_matches_exact_objective():
    cfg=json.loads((DATA/'configurations/T082-C01.json').read_text())
    for run in cfg['runs']:
        raw=read_asset(run['witness']);v=read_asset(run['visual']);a=list(map(Fraction,raw['heights']));n=len(a)
        curve=[sum((a[i]*(1-a[i+k]) for i in range(max(0,-k),min(n,n-k))),Fraction(0))*Fraction(2,n) for k in range(-n,n+1)]
        assert max(curve)==Fraction(run['objective'])
        assert v['curve']==pytest.approx([float(x) for x in curve])


def test_scores_above_one_and_optimization_directions_are_preserved():
    cfg=json.loads((DATA/'configurations/T066-C01.json').read_text())
    assert cfg['direction']=='maximize'
    assert next(r for r in cfg['runs'] if r['program']=='baseline')['combined_score']>1

    cfg=json.loads((DATA/'configurations/T060-C01.json').read_text())
    assert cfg['direction']=='minimize'
    assert next(r for r in cfg['runs'] if r['program']=='baseline')['combined_score']>1


def test_sota_has_separate_reviewed_replay_evidence():
    report=json.loads((ROOT/'reports/sota_acceptance.json').read_text())
    index=json.loads((DATA/'index.json').read_text())
    for task in index['tasks']:
        for config in task['configurations']:
            detail=read_asset(config['asset']);sota=detail['sota']
            assert config['sota']==sota
            accepted=report['configurations'].get(config['id'],{})
            if sota['status'] not in ('reproduced','conservative_reproduction','best_reproducible'):
                assert sota['run'] is None
                continue
            run=sota['run'];original=accepted['run']
            assert original['validity']==1 and original['strict']
            assert accepted['broken_construction_rejected'] and accepted['claimed_score_ignored']
            assert run['objective']==str(original['objective'])
            assert read_asset(run['result'])==original
            assert (ROOT/accepted['witness']).read_bytes()==(ROOT/'website/dist'/run['witness']).read_bytes()
            assert read_asset(run['visual'])['kind']
            assert sota['record']['public_source']['url'].startswith('https://')
            if sota['status']=='conservative_reproduction':
                assert sota['record']['limitations']


def test_visible_methods_merge_human_and_fixed_reference():
    app=(ROOT/'website/dist/app.js').read_text()
    assert "const cols=['id','direction','init_program','search','sota','reported']" in app
    assert 'Human construction' not in app and 'Fixed reference' not in app
    assert "sota:['Best results','最佳结果']" in app
    assert "bestReplay:['Best result (reproduced)','最佳结果（复现）']" in app
    assert "bestReport:['Best result (reported)','最佳结果（报告）']" in app
    assert 'Known SOTA' not in app and '已知 SOTA' not in app
    assert "function visibleRuns(data)" in app
    assert "searchResult:['Search','搜索结果']" in app


def test_local_improvement_retains_exact_score_and_separate_evidence():
    database=json.loads((ROOT/'reports/own_results.json').read_text())
    detail=json.loads((DATA/'configurations/T005-C01.json').read_text())
    own=detail['own'];record=database['configurations']['T005-C01']
    assert len(detail['runs'])==4
    assert own['objective']==record['run']['objective']==record['replay']['objective']
    assert read_asset(own['evidence'])==record
    assert record['damaged_witness_rejected'] and record['claimed_score_ignored']
    assert hashlib.sha256((ROOT/'website/dist'/own['witness']).read_bytes()).hexdigest()==record['witness_sha256']
    assert Fraction(own['objective'])<Fraction(record['comparison']['public_strict_reported_value'])
    assert record['comparison']['new_public_record'] is False
    assert detail['sota']['run']['program']=='sota'
