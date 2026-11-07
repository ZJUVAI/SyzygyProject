"""Reproduce admission checks before registry release."""
import argparse
import copy
import hashlib
import importlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench import registry
from mathbench.evaluate import evaluate_candidate
from mathbench.export import export_seed
from mathbench.replay import replay
from scripts.audits.independent_audit import independent_quantity, broken


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def review(task, label):
    directory = ROOT / 'tasks' / task.lower()
    metadata = json.loads((directory / 'task.json').read_text())
    if metadata['task_id'] != task:
        raise ValueError('Task ID does not match its directory')
    # This change applies only to this review process. CLI release admission is separate.
    registry.INITIAL_TASKS = tuple(dict.fromkeys((*registry.INITIAL_TASKS, task)))
    # Include draft configurations only in this admission process.
    released_load_task = registry.load_task
    registry.load_task = lambda task_id: metadata if task_id == task else released_load_task(task_id)
    checker = importlib.import_module(f'tasks.{task.lower()}.check')
    destination = directory / 'runs' / label
    destination.mkdir(parents=True, exist_ok=False)
    evidence = {'task_id': task, 'reviewer': 'Sol main agent',
                'command': f'.venv/bin/python scripts/admit_tasks.py {task} --label {label}',
                'configurations': {}}
    for config in metadata['configurations']:
        cid = config['id']
        folder = destination / cid
        results = {}
        for program in ('init_program', 'baseline', 'human', 'reference', 'evolution'):
            output = folder / ('initial' if program == 'init_program' else program)
            result = evaluate_candidate(task, directory / (program + '.py'), cid,
                                        strict=True, seed=0, output_dir=output)
            save(output / 'result.json', result)
            if result['validity'] != 1:
                raise AssertionError((task, cid, program, result))
            solution = json.loads((output / 'solution.json').read_text())
            checked = checker.validate(solution, config, strict=True)
            modified = copy.deepcopy(solution)
            modified.update(objective=987654321, score=-1, claimed_score=987654321)
            assert checker.validate(modified, config, strict=True) == checked
            try:
                checker.validate(broken(task, solution), config, strict=True)
            except ValueError:
                pass
            else:
                raise AssertionError(f'{cid}: broken {program} was accepted')
            quantity = independent_quantity(task, solution, config)
            from scripts.review_search import check_quantity
            check_quantity(task, quantity, result)
            replayed = replay(task, output / 'solution.json', cid, strict=True)
            assert replayed['validity'] == 1 and replayed['objective'] == result['objective']
            results[program] = {'run': result, 'independent_quantity': quantity,
                                'claimed_score_ignored': True,
                                'damaged_construction_rejected': True,
                                'strict_replay_passed': True}
            print(cid, program, str(result['objective'])[:100], flush=True)
        cold = export_seed(task, folder / 'cold_seed', cid)
        cold_result = evaluate_candidate(task, cold / 'init_program.py', cid, strict=True)
        assert cold_result['validity'] == 1
        assert 'human_reference' not in json.loads((cold / 'configuration.json').read_text())
        failures = {}
        for name, body, timeout in (
            ('program_error', "raise RuntimeError('admission error')", 5),
            ('timeout', 'while True: pass', 0.2),
            ('nonfinite', "return {'invalid': float('nan')}", 5)):
            program = folder / (name + '.py')
            program.write_text('def run_code():\n    ' + body + '\n')
            result = evaluate_candidate(task, program, cid, strict=True,
                                        generation_timeout=timeout)
            assert result['validity'] == 0 and result['objective'] is None
            assert result['combined_score'] == 0
            assert result['error_type'] == ('TimeoutError' if name == 'timeout' else 'RuntimeError')
            failures[name] = result
        evidence['configurations'][cid] = {'configuration': copy.deepcopy(config),
            'configuration_capture_stage': 'admission_generation', 'programs': results,
            'cold_seed_export': cold_result, 'failure_checks': failures}
        save(destination / 'review.json', evidence)
    evidence['source_sha256'] = {
        str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob('*'))
        if path.is_file() and not {'runs', '__pycache__', 'best'} & set(path.relative_to(directory).parts)
        and path.name not in ('acceptance.json', 'task.json', 'sota.json')}
    evidence['status'] = 'checks_passed_pending_source_review'
    save(destination / 'review.json', evidence)
    return evidence


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tasks', nargs='+')
    parser.add_argument('--label', default='admission_20261106')
    args = parser.parse_args()
    for task in args.tasks:
        if not (task.startswith(('T', 'N')) and task[1:].isdigit()):
            parser.error('Expected a task ID such as T022')
        review(task, args.label)
