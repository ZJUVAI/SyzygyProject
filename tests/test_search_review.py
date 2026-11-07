"""Keep improvements that disappear when rounded to binary floats."""
import pytest
from scripts.review_search import better, objective_number


def test_saved_best_comparison_uses_exact_objectives():
    previous = dict(validity=1, objective='100000000000000000001/100000000000000000000')
    candidate = dict(validity=1, objective='100000000000000000002/100000000000000000000')
    assert better(candidate, previous, 'maximize')
    assert not better(candidate, previous, 'minimize')
    assert not better(candidate, candidate, 'maximize')


def test_invalid_candidate_cannot_be_promoted():
    with pytest.raises(ValueError):
        objective_number(dict(validity=0, objective=999999))


@pytest.mark.parametrize('changed', ['parameters', 'human_reference'])
def test_admission_cannot_transfer_to_changed_configuration(tmp_path, monkeypatch, changed):
    import copy
    import json
    import scripts.accept_task as module
    config = {'id': 'EXAMPLE-C01', 'parameters': {'n': 11},
              'human_reference': 10, 'direction': 'maximize'}
    current = copy.deepcopy(config)
    current[changed] = {'n': 12} if changed == 'parameters' else 11
    directory = tmp_path / 'tasks/example'
    run = directory / 'runs/checked'
    run.mkdir(parents=True)
    evidence = {'status': 'checks_passed_pending_source_review',
                'source_sha256': {}, 'configurations': {
                    config['id']: {'configuration': config}}}
    (run / 'review.json').write_text(json.dumps(evidence))
    (directory / 'task.json').write_text(json.dumps({'configurations': [current]}))
    for name in ('sota.json', 'records.json'):
        (directory / name).write_text('{}')
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    with pytest.raises(ValueError, match='changed after admission'):
        module.accept('EXAMPLE', 'checked', {'source': 'Reviewed original instance.'})
    assert json.loads((run / 'review.json').read_text()) == evidence
    assert not (directory / 'acceptance.json').exists()


def test_candidate_only_review_still_rejects_a_failed_selected_witness(tmp_path, monkeypatch):
    import json
    import scripts.review_search as module
    manifest = {'configuration_ids': ['example'], 'source_sha256': {}}
    summary = {'task_id': 'EXAMPLE', 'configurations': [
        {'config_id': 'example', 'best': 'search_seed1', 'results': {
            'initial': {'validity': 0}, 'search_seed1': {'validity': 0, 'objective': 999}}}]}
    (tmp_path / 'manifest.json').write_text(json.dumps(manifest))
    path = tmp_path / 'summary.json'
    path.write_text(json.dumps(summary))
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    monkeypatch.setattr(module, 'load_task', lambda _: {'configurations': [{'id': 'example'}]})
    with pytest.raises(ValueError, match='valid construction'):
        module.review(path, candidate_only=True)
    assert json.loads(path.read_text()) == summary


@pytest.mark.parametrize('snapshot', [{}, {'configuration_capture_stage': 'sol_review'}])
def test_acceptance_requires_admission_snapshot(tmp_path, monkeypatch, snapshot):
    import json
    import scripts.accept_task as module

    directory = tmp_path / 'tasks/example'
    run = directory / 'runs/checked'
    run.mkdir(parents=True)
    config = {'id': 'EXAMPLE-C01'}
    if snapshot:
        snapshot = {**snapshot, 'configuration': config}
    evidence = {'status': 'checks_passed_pending_source_review', 'source_sha256': {},
                'configurations': {config['id']: snapshot}}
    (run / 'review.json').write_text(json.dumps(evidence))
    (directory / 'task.json').write_text(json.dumps({'configurations': [config]}))
    for name in ('sota.json', 'records.json'):
        (directory / name).write_text('{}')
    monkeypatch.setattr(module, 'ROOT', tmp_path)

    with pytest.raises(ValueError, match='Fresh admission'):
        module.accept('EXAMPLE', 'checked', {'source': 'Reviewed.'})
    assert not (directory / 'best').exists()


@pytest.mark.parametrize('mutation', ['bytes', 'objective', 'configuration', None])
def test_selected_witness_is_bound_to_strict_replay(tmp_path, monkeypatch, mutation):
    import hashlib
    import scripts.accept_task as module

    raw = b'{"points":[[0,0]]}\n'
    path = tmp_path / 'solution.json'
    path.write_bytes(raw if mutation != 'bytes' else b'{}')
    result = {'task_id': 'T001', 'config_id': 'T001-C01', 'validity': 1, 'objective': 1}
    checked = {'run': result, 'solution_sha256': hashlib.sha256(raw).hexdigest()}

    def strict_replay(task, staged, cid, *, strict):
        assert strict and staged != path and staged.read_bytes() == raw
        actual = dict(result)
        if mutation == 'objective':
            actual['objective'] = 2
        if mutation == 'configuration':
            actual['config_id'] = 'T001-C02'
        return actual

    monkeypatch.setattr(module, 'replay', strict_replay)
    if mutation:
        with pytest.raises(ValueError, match='selected witness'):
            module._checked_witness('T001', {}, 'T001-C01', tmp_path, checked)
    else:
        assert module._checked_witness('T001', {}, 'T001-C01', tmp_path, checked) == (raw, result)
