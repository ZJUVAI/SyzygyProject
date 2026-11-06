import json
from pathlib import Path
import pytest
from mathbench.evaluate import evaluate_candidate
from mathbench.export import export_seed
from mathbench.registry import ROOT
from mathbench.replay import replay


@pytest.mark.parametrize('adapter,task,config', [
    ('simpletes_evaluator','T073','T073-C01'),
    ('dream_rsi_evaluator','T005','T005-C02')])
def test_upstream_interface(adapter,task,config):
    import importlib
    evaluate=importlib.import_module('mathbench.'+adapter).evaluate
    result=evaluate(ROOT/'tasks'/task.lower()/'init_program.py')
    assert result['validity']==1 and result['config_id']==config
    assert result['verification_status'] in ('exact','certified')
    assert isinstance(result['combined_score'],float)


def test_saved_witness_replay(tmp_path):
    from tasks.t073.human import run_code
    witness=tmp_path/'solution.json';witness.write_text(json.dumps(run_code()))
    assert replay('T073',witness)['objective']==578


def test_cold_seed_export(tmp_path):
    folder=export_seed('T002',tmp_path/'cold')
    assert {p.name for p in folder.iterdir()}=={'instruction.txt','init_program.py','configuration.json'}
    assert 'human_reference' not in json.loads((folder/'configuration.json').read_text())
    assert evaluate_candidate('T002',folder/'init_program.py',strict=True)['validity']==1


@pytest.mark.parametrize('body,error', [
    ('raise RuntimeError("failure")','RuntimeError'),
    ('return {"sequence":[float("nan")]*100}','RuntimeError'),
    ('return {"sequence":[0]*100}','RuntimeError')])
def test_candidate_failures(tmp_path,body,error):
    program=tmp_path/'bad.py';program.write_text('def run_code():\n    '+body+'\n')
    result=evaluate_candidate('T073',program,strict=True)
    assert result['validity']==0 and result['combined_score']==0
    assert result['error_type']==error


def test_fixed_search_reproducibility(monkeypatch):
    from tasks.t080.baseline import run_code
    monkeypatch.delenv('MATHBENCH_SEARCH_SECONDS',raising=False)
    monkeypatch.setenv('MATHBENCH_SEED','7')
    assert run_code()==run_code()
