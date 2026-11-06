"""Replay task SOTA candidates and save a separate, reviewed evidence snapshot.

Historical acceptance results and their frozen normalization stay unchanged.
"""
from __future__ import annotations

import argparse
import importlib
import json
import math
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.evaluate import evaluate_candidate
from mathbench.registry import INITIAL_TASKS, load_task
from scripts.independent_audit import independent_quantity, broken


def same_exact_value(left, right):
    """Compare literals as exact rationals, including decimal literals."""
    import sympy as sp
    def parse(value):
        return sp.sympify(str(value).replace('sqrt2', 'sqrt(2)'), rational=True)
    return sp.simplify(parse(left) - parse(right)) == 0


def audit(task_ids):
    destination = ROOT / 'reports/sota_acceptance.json'
    report = json.loads(destination.read_text()) if destination.exists() else {
        'date': '2026-11-05', 'reviewer': 'Sol main agent', 'configurations': {}}
    for tid in task_ids:
        folder = ROOT / 'tasks' / tid.lower()
        path = folder / 'sota.json'
        if not path.exists():
            print(tid, 'awaiting task review', flush=True)
            continue
        records = json.loads(path.read_text())
        checker = importlib.import_module(f'tasks.{tid.lower()}.check')
        for config in load_task(tid)['configurations']:
            cid = config['id']
            record = records['configurations'][cid]
            program = record.get('program')
            if not program:
                report['configurations'][cid] = dict(task_id=tid, status='pending_reproduction', record=record)
                continue
            output = ROOT / 'reports/sota_witnesses' / tid / cid
            result = evaluate_candidate(tid, folder / program, cid, strict=True, output_dir=output)
            if not result['validity']:
                raise ValueError(f'{cid}: {result}')
            solution = json.loads((output / 'solution.json').read_text())
            checked = checker.validate(solution, config, strict=True)
            # Independently compute at least one mathematical quantity.
            quantity = independent_quantity(tid, solution, config)
            key = {'T001':'radius','T005':'sum_radii','T014':'minimum_triangle_area',
                   'T035':'order','T044':'span','T057':'ratio','T060':'blocks',
                   'T066':'minimum_distance','T067':'codewords','T073':'energy',
                   'T079':'exact_objective','T080':'exact_objective','T081':'exact_objective',
                   'T082':'maximum_overlap','N001':'independent_words','T089':'absolute_determinant',
                   'T099':'diameter','T097':'additions'}.get(tid)
            if key:
                if tid == 'T057':
                    assert math.isclose(float(checked['objective']), quantity[key], rel_tol=1e-14)
                else:
                    assert Fraction(str(checked['objective'])) == Fraction(str(quantity[key]))
            elif tid == 'T009':
                assert math.isclose(checked['objective'], float(quantity['minimum_angle_80_digits']), rel_tol=1e-14)
            elif tid == 'T002':
                import sympy as sp
                assert sp.simplify(sp.sympify(str(checked['objective']).replace('sqrt2','sqrt(2)')) - sp.sympify(quantity['bounding_side'])) == 0
            assert same_exact_value(checked['objective'], record['reproduced_value']), f'{cid}: reproduced_value must equal the exact checker output'
            try:
                checker.validate(broken(tid, solution), config, strict=True)
            except (ValueError, TypeError):
                pass
            else:
                raise AssertionError(f'{cid}: damaged construction accepted')
            assert checker.validate(dict(solution, objective=987654321), config, strict=True)['objective'] == checked['objective']
            # A task's provenance assertion alone does not authorize a SOTA label.
            # Review the source and numerical comparison in the owning chat.
            prior = report['configurations'].get(cid, {})
            if prior.get('record') != record or prior.get('run',{}).get('objective') != result['objective']:
                prior = {}
            status = prior.get('status', 'pending_source_review')
            report['configurations'][cid] = dict(
                prior, task_id=tid, status=status, record=record, run=result,
                witness=str((output / 'solution.json').relative_to(ROOT)),
                independent_quantity=quantity, broken_construction_rejected=True,
                claimed_score_ignored=True)
            print(cid, str(result['objective'])[:90], 'strict replay and independent check passed', flush=True)
        destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tasks', nargs='*', choices=INITIAL_TASKS)
    args = parser.parse_args()
    audit(args.tasks or INITIAL_TASKS)
