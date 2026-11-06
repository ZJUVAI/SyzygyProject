"""Check staged configurations without adding them to the release registry.

This script records evidence. It does not grant acceptance.
"""
import argparse
from fractions import Fraction
import importlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench import evaluate as runner
from mathbench import export as exporter
from mathbench.registry import load_task, task_path
from scripts.independent_audit import broken, independent_quantity


def check_quantity(task_id, checked, quantity):
    if task_id == 'T002':
        import sympy as sp
        a = sp.sympify(str(checked['objective']).replace('sqrt2', 'sqrt(2)'))
        assert sp.simplify(a - sp.sympify(quantity['bounding_side'])) == 0
    elif task_id == 'T009':
        value = float(quantity['minimum_angle_80_digits'])
        assert checked['objective'] <= value + 1e-15
        assert math.isclose(checked['objective'], value, rel_tol=1e-14)
    else:
        key = {'T001': 'radius', 'T014': 'minimum_triangle_area',
               'T044': 'span', 'T073': 'energy', 'T097': 'additions'}[task_id]
        assert Fraction(str(checked['objective'])) == Fraction(str(quantity[key]))


def review(task_id, destination):
    folder = task_path(task_id)
    stage = json.loads((folder / 'configuration_expansion.json').read_text())
    planned = json.loads((ROOT / 'research/configuration_selection.json').read_text())
    selected = next(t for t in planned['tasks'] if t['task_id'] == task_id)
    selected = {c['id']: c for c in selected['configurations']}
    live = load_task(task_id)
    result = {'task_id': task_id, 'status': 'pending_sol_review', 'configurations': []}
    test = subprocess.run([sys.executable, '-m', 'pytest', str(folder), '-q'],
                          cwd=ROOT, text=True, capture_output=True, timeout=180)
    result['tests'] = {'passed': test.returncode == 0, 'output': test.stdout + test.stderr}
    checker = importlib.import_module('tasks.' + task_id.lower() + '.check')
    for config in stage['configurations']:
        assert config['parameters'] == selected[config['id']]['parameters']
        assert config['direction'] == live['configurations'][0]['direction']
        record = {'config_id': config['id'], 'parameters': config['parameters'], 'runs': []}
        with tempfile.TemporaryDirectory(prefix='mathbench-cold-review-') as temp:
            with patch.object(exporter, 'load_config', return_value=config):
                cold = exporter.export_seed(task_id, Path(temp) / 'seed', config['id'])
            with patch.object(runner, 'load_config', return_value=config):
                record['cold_export_check'] = runner.evaluate_candidate(
                    task_id, cold / 'init_program.py', config['id'], strict=True)
        for name in ('init_program', 'baseline', 'human', 'reference'):
            target = destination / task_id / config['id'] / name
            with patch.object(runner, 'load_config', return_value=config):
                run = runner.evaluate_candidate(task_id, folder / (name + '.py'),
                                                config['id'], strict=True, seed=0,
                                                output_dir=target)
            run['program'] = name
            record['runs'].append(run)
            print(task_id, config['id'], name, run['validity'], run['objective'], flush=True)
        human = next(r for r in record['runs'] if r['program'] == 'human')
        if human['validity'] == 1:
            solution = json.loads((destination / task_id / config['id'] / 'human/solution.json').read_text())
            checked = checker.validate(solution, config, strict=True)
            quantity = independent_quantity(task_id, solution, config)
            check_quantity(task_id, checked, quantity)
            try:
                checker.validate(broken(task_id, solution), config, strict=True)
            except (ValueError, TypeError):
                pass
            else:
                raise AssertionError('Damaged witness accepted')
            claimed = dict(solution, objective=987654321)
            assert checker.validate(claimed, config, strict=True)['objective'] == checked['objective']
            numeric = float(Fraction(str(checked.get('objective_value', checked['objective']))))
            assert math.isclose(config['human_reference'], numeric, rel_tol=1e-12)
            record['independent_audit'] = {
                'reviewer': 'Sol main agent', 'independent_quantity': quantity,
                'broken_construction_rejected': True, 'claimed_score_ignored': True}
        record['automated_checks_passed'] = (
            result['tests']['passed'] and len(record['runs']) == 4 and
            all(r['validity'] == 1 for r in record['runs']) and 'independent_audit' in record and
            record['cold_export_check']['validity'] == 1)
        result['configurations'].append(record)
    result['automated_checks_passed'] = all(c['automated_checks_passed'] for c in result['configurations'])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tasks', nargs='+')
    parser.add_argument('--output', default='runs/configuration_expansion')
    args = parser.parse_args()
    destination = ROOT / args.output
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / 'review.json'
    existing = json.loads(target.read_text()) if target.exists() else []
    for task in args.tasks:
        try:
            record = review(task, destination)
        except Exception as exc:
            record = {'task_id': task, 'status': 'pending_sol_review', 'error': repr(exc),
                      'automated_checks_passed': False}
            print(task, repr(exc), flush=True)
        existing = [r for r in existing if r['task_id'] != task] + [record]
        target.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + '\n')
    if not all(r['automated_checks_passed'] for r in existing if r['task_id'] in args.tasks):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
