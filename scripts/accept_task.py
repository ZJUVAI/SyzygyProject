"""Save Sol's source review after the independent admission checks pass.

This does not add a task to the release registry. The main reviewer does that
after checking the mathematical definition and the supplied source evidence.
"""
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest.mock import patch

from mathbench import registry

from mathbench.registry import ROOT
from scripts.admit_tasks import REQUIRED_PROGRAMS, record_program
from scripts.audit_sota import same_exact_value
from scripts.review_search import objective_number
from mathbench.replay import replay


def _write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def approve_review_statuses(value):
    """Update draft status fields after every configuration passes review."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key in ('status', 'review_status', 'acceptance_status') and item == 'pending_sol_review':
                value[key] = 'accepted_by_sol'
            else:
                approve_review_statuses(item)
    elif isinstance(value, list):
        for item in value:
            approve_review_statuses(item)



def sync_own_records(sota_config, records_config, config, selected, result, solution, digest, review_date=None, *, generation_result=None):
    """Make own-result metadata refer to the artifact selected during admission."""
    review_date = review_date or datetime.now(timezone.utc).date().isoformat()
    cid=config['id']
    for parent in (sota_config, records_config):
        for key in ('best_own_search', 'own_search_record'):
            if not isinstance(parent.get(key),dict):
                continue
            parent[key]=dict(value=result['objective'],
                objective_value=result.get('objective_value',result['objective']),
                program=selected+'.py', witness=f'best/{cid}/solution.json',
                witness_sha256=digest, parameters=config['parameters'],seed=0,
                verification_status=result['verification_status'],
                review_status='reviewed_by_sol',date_checked=review_date,
                origin_type='Task-local construction from the simple seed; comparison assets were not read.',
                search_metadata=solution.get('search_metadata',{}),
                generation_record=generation_result if generation_result is not None else result,
                evidence_state='Strict replay and independent Sol review passed.')
            if 'objective_interval' in result.get('details',{}):
                parent[key]['objective_interval'] = result['details']['objective_interval']


def _checked_witness(task, metadata, cid, source, checked):
    """Replay exactly the bytes that will be written to the archive."""
    raw = (source / 'solution.json').read_bytes()
    expected = checked['run']
    if hashlib.sha256(raw).hexdigest() != checked.get('solution_sha256'):
        raise ValueError(f'{cid}: selected witness changed or lacks an admission checksum')
    if (expected.get('task_id'), expected.get('config_id')) != (task, cid):
        raise ValueError(f'{cid}: admission result does not identify this configuration')
    load_task = registry.load_task
    admitted_tasks = (*registry.INITIAL_TASKS, task)
    with TemporaryDirectory(prefix='accept-witness-') as temporary:
        path = Path(temporary) / 'solution.json'
        path.write_bytes(raw)
        with (patch.object(registry, 'INITIAL_TASKS', admitted_tasks),
              patch.object(registry, 'load_task',
                           lambda tid: metadata if tid == task else load_task(tid))):
            result = replay(task, path, cid, strict=True)
    if (result['validity'] != 1 or result.get('task_id') != task
            or result.get('config_id') != cid
            or result['objective'] != expected['objective']):
        raise ValueError(f'{cid}: selected witness failed strict replay or changed its objective')
    return raw, result


def accept(task, label, source_review, review_date=None):
    review_date = review_date or datetime.now(timezone.utc).date().isoformat()
    if not isinstance(source_review, dict) or not source_review:
        raise ValueError('Sol must supply a concrete source review')
    directory = ROOT / 'tasks' / task.lower()
    run = directory / 'runs' / label
    evidence = json.loads((run / 'review.json').read_text())
    if evidence['status'] != 'checks_passed_pending_source_review':
        raise ValueError('A full successful admission run is required')
    metadata = json.loads((directory / 'task.json').read_text())
    if set(evidence['configurations']) != {c['id'] for c in metadata['configurations']}:
        raise ValueError('Configuration coverage does not match the admission run')
    pending = {config['id'] for config in metadata['configurations']
               if config.get('acceptance_status') == 'pending_sol_review'}
    expanding = metadata.get('acceptance_status') == 'accepted_by_sol' and bool(pending)
    for name, digest in evidence['source_sha256'].items():
        if name.endswith('.py') or Path(name).parts[0] == 'data':
            if hashlib.sha256((directory / name).read_bytes()).hexdigest() != digest:
                raise ValueError('Construction or checker source changed: ' + name)
    sota = json.loads((directory / 'sota.json').read_text())
    records = json.loads((directory / 'records.json').read_text())
    promotions = []
    for config in metadata['configurations']:
        cid = config['id']
        checked_config = evidence['configurations'][cid].get('configuration')
        if checked_config is not None and json.dumps(checked_config, sort_keys=True) != json.dumps(config, sort_keys=True):
            raise ValueError('Configuration or frozen human reference changed after admission: ' + cid)
        if (checked_config is None or evidence['configurations'][cid].get('configuration_capture_stage')
                != 'admission_generation'):
            raise ValueError('Fresh admission with a configuration snapshot is required: ' + cid)
        programs = evidence['configurations'][cid]['programs']
        record = sota['configurations'][cid]
        public_program = record_program(record)
        if set(programs) != {*REQUIRED_PROGRAMS, public_program}:
            raise ValueError('Missing a required program check')
        for checked in programs.values():
            if checked['run']['validity'] != 1 or not all(checked[k] for k in (
                    'claimed_score_ignored', 'damaged_construction_rejected', 'strict_replay_passed')):
                raise ValueError('A program failed admission')
        if expanding and cid not in pending:
            # The controls above check the old configuration after code changes.
            # Its frozen comparison and own-search archives remain authoritative.
            continue
        initial = programs['init_program']['run']
        records.setdefault('initial_results', {})[cid] = {
            k: initial[k] for k in ('objective', 'objective_value', 'validity',
                                     'verification_status', 'combined_score') if k in initial}
        reference = programs[public_program]
        recorded_value = record['reproduced_value']
        reproduced_value = reference['run']['objective']
        if str(recorded_value) != str(reproduced_value) and not same_exact_value(recorded_value, reproduced_value):
            raise ValueError('Reconcile reproduced_value with the verified reference first')
        record['program'] = public_program + '.py'
        record['review_status'] = 'accepted_by_sol'
        record['verification'] = dict(status='reviewed_by_sol', reviewer='Sol main agent',
            date=review_date, run=reference['run'],
            independent_quantity=reference['independent_quantity'],
            broken_construction_rejected=True, claimed_score_ignored=True)
        names = ('init_program', 'baseline', 'evolution')
        choose = min if config['direction'] == 'minimize' else max
        selected = choose(names, key=lambda name: objective_number(programs[name]['run']))
        source = run / cid / ('initial' if selected == 'init_program' else selected)
        raw, replayed = _checked_witness(task, metadata, cid, source, programs[selected])
        best = directory / 'best' / cid
        retain_incumbent = False
        provenance_path = best / 'provenance.json'
        if provenance_path.exists():
            provenance = json.loads(provenance_path.read_text())
            if provenance.get('status') in ('reviewed_by_sol', 'accepted_by_sol'):
                incumbent = replay(task, best / 'solution.json', cid, strict=True)
                saved_result = json.loads((best / 'result.json').read_text())
                if incumbent['validity'] != 1 or incumbent['objective'] != saved_result['objective']:
                    raise ValueError('The accepted incumbent failed replay: ' + cid)
                candidate_value = objective_number(replayed)
                incumbent_value = objective_number(incumbent)
                retain_incumbent = choose(candidate_value, incumbent_value) == incumbent_value
        if not retain_incumbent:
            previous = run / 'previous_best' / cid
            if best.exists() and previous.exists():
                raise ValueError('Previous best backup already exists')
            solution = json.loads(raw)
            provenance = dict(status='reviewed_by_sol', reviewer='Sol main agent',
                date=review_date, seed=0,
                origin='Task-local construction from the simple seed; comparison witnesses were not read.',
                program=selected + '.py', generation_record=programs[selected]['run'],
                search_metadata=solution.get('search_metadata', solution.get('search', {})),
                solution_sha256=hashlib.sha256(raw).hexdigest(),
                replay_command=f'python -m mathbench replay {task} {best.relative_to(ROOT) / "solution.json"} --config {cid}')
            promotions.append((best, previous, raw, replayed, provenance))
        archive = records.get('configurations', {}).get(cid, {})
        if isinstance(archive.get('best_reproduced'), dict):
            archive['best_reproduced']['review_status'] = 'reviewed_by_sol'
        if not retain_incumbent:
            sync_own_records(record, archive, config, selected, replayed, solution,
                             provenance['solution_sha256'], review_date,
                             generation_result=programs[selected]['run'])
        source = archive.get('source_review', {})
        if isinstance(source, dict) and source.get('status') == 'pending_sol_review':
            source['status'] = 'reviewed_by_sol'
        if isinstance(record.get('reference_record'), dict):
            record['reference_record']['reproduction_status'] = 'Exact shared-runner replay and independent Sol review passed.'
        if not retain_incumbent and isinstance(record.get('own_search_record'), dict):
            record['own_search_record'].update(status='reviewed_by_sol',
                value=replayed['objective'],
                reproduction_status='Saved own construction passed shared-runner replay and independent Sol review.')
    metadata['acceptance_status'] = 'accepted_by_sol'
    for config in metadata['configurations']:
        config['acceptance_status'] = 'accepted_by_sol'
    review_key = 'configuration_expansion_review' if expanding else 'acceptance_review'
    metadata[review_key] = dict(reviewer='Sol main agent', date=review_date,
        decision='实现完成并通过Sol验收',
        source_review=source_review)
    if expanding:
        metadata[review_key]['configuration_ids'] = sorted(pending)
    for name in ('README.md', 'IMPLEMENTATION.md'):
        path = directory / name
        if not path.is_file():
            continue
        content = path.read_text().replace('待 Sol 验收', f'已通过 Sol 验收（{review_date}）')
        content = content.replace('pending Sol review', f'accepted by Sol on {review_date}')
        content = content.replace('Status: pending_sol_review', 'Status: accepted_by_sol')
        content = content.replace('`pending_sol_review`', '`accepted_by_sol`')
        path.write_text(content)
    records['review_status'] = 'accepted_by_sol'
    for document in (metadata, records, sota):
        approve_review_statuses(document)
    for best, previous, raw, result, provenance in promotions:
        if best.exists():
            previous.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(best), str(previous))
        best.mkdir(parents=True)
        (best / 'solution.json').write_bytes(raw)
        _write(best / 'result.json', result)
        _write(best / 'provenance.json', provenance)
    _write(directory / 'records.json', records)
    sota['review_status'] = 'accepted_by_sol'
    _write(directory / 'task.json', metadata)
    _write(directory / 'sota.json', sota)
