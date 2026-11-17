import gzip
import json
from pathlib import Path
import pytest
from mathbench.evaluate import evaluate_candidate
from mathbench.export import export_seed
from mathbench.registry import ROOT
from mathbench.replay import read_witness_bytes, replay
from mathbench.saved_result import read_best_record, write_best_record


@pytest.mark.parametrize('adapter,task,config', [
    ('simpletes_evaluator','T073','T073-C01'),
    ('dream_rsi_evaluator','T002','T002-C02')])
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
    packed = witness.with_suffix('.json.gz')
    packed.write_bytes(gzip.compress(witness.read_bytes(), mtime=0))
    witness.unlink()
    assert replay('T073', packed)['objective'] == 578
    assert replay('T073', witness)['objective'] == 578


def test_best_record_replays_and_preserves_original_bytes(tmp_path):
    from tasks.t073.human import run_code
    directory = tmp_path / "t073" / "data"
    saved = directory / "results.json.gz"
    solution = run_code()
    raw = (json.dumps(solution, indent=2) + "\n").encode()
    result = {"config_id": "T073-C01", "objective": 578}
    provenance = {"seed": 0}
    initial = {"objective": 1000}
    write_best_record(saved, result, provenance, raw, initial_result=initial)
    assert read_best_record(saved) == {
        "result": result, "initial_result": initial, "provenance": provenance, "solution": solution,
    }
    assert read_witness_bytes(directory / "best" / "solution.json") == raw
    previous = tmp_path / "t073" / "best" / "T073-C01" / "solution.json"
    assert read_witness_bytes(previous) == raw
    assert replay("T073", saved)["objective"] == 578


def test_cold_seed_export(tmp_path):
    folder=export_seed('T003',tmp_path/'cold')
    assert {p.name for p in folder.iterdir()}=={'instruction.txt','init_program.py','configuration.json'}
    assert 'human_reference' not in json.loads((folder/'configuration.json').read_text())
    assert evaluate_candidate('T003',folder/'init_program.py',strict=True)['validity']==1


@pytest.mark.parametrize('task,public_input,comparison', [
    ('T096', 'data/source/mona-lisa100K.tsp.gz', 'data/human/monalisa_5757191.tour.gz'),
    ('T026', 'data/source/ortho40.instance.json', 'data/reference/ortho40_19.solution.json'),
    ('T093', 'data/tai256c.dat.gz', 'data/tai256c.sln'),
    ('T042', 'data/source/G70.gz', 'data/human/human_g70_1flip.json'),
    ('T043', 'data/source/gd96a.rmf', 'data/reference/spectral_adjacent_ordering.json'),
    ('T038', 'data/DSJC1000.5.bits', 'data/human_witness.json'),
    ('T039', 'data/source/C2000.9.bits', 'data/reference/grosso_locatelli_pullan_2005_clique80.json'),
    ('T097', 'data/source/X-n1001-k43.vrp', 'data/reference/public_72332.sol'),
    ('T098', 'data/source/b4794d123e18a908924d3d33cdeeae3b.wcnf.gz', 'data/reference/mse2026_boums_60_assignment.json'),
    ('T095', 'data/source/ta41_instance.json', 'data/reference/ta41_2006_schedule.json')])
def test_public_input_export_excludes_comparison_assets(tmp_path, monkeypatch, task, public_input, comparison):
    from mathbench import export
    source = tmp_path / 'source'
    (source / 'data').mkdir(parents=True)
    (source / 'init_program.py').write_text('def run_code(): return {}\n')
    (source / 'instruction.txt').write_text('Use the public instance.\n')
    for name, text in ((public_input, 'public instance data\n'),
                       (comparison, 'private comparison witness\n'),
                       ('data/source/private_record.json', 'private source record\n')):
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    extra_public_files = ()
    for name in extra_public_files:
        (source / name).write_text('def run_simple_seed(): return {}\n')
    (source / 'bestknown.json').write_text('{"record": 123}\n')
    config = {'id': task + '-C01', 'parameters': {'n': 256},
              'direction': 'minimize', 'human_reference': 123}
    monkeypatch.setattr(export, 'load_config', lambda *args: config)
    monkeypatch.setattr(export, 'task_path', lambda *args: source)
    output = export.export_seed(task, tmp_path / 'public')
    assert {str(p.relative_to(output)) for p in output.rglob('*') if p.is_file()} == {
        'init_program.py', 'instruction.txt', 'configuration.json', public_input} | set(extra_public_files)
    assert 'human_reference' not in json.loads((output / 'configuration.json').read_text())


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
    from tasks.t078.baseline import run_code
    monkeypatch.delenv('MATHBENCH_SEARCH_SECONDS',raising=False)
    monkeypatch.setenv('MATHBENCH_SEED','7')
    assert run_code()==run_code()
