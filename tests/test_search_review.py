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
