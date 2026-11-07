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
from scripts.audits.independent_audit import independent_quantity, broken


def same_exact_value(left, right):
    """Compare literals as exact rationals, including decimal literals."""
    def radical_terms(value):
        if not isinstance(value,str) or not value.startswith('sqrt_sum:'):
            return None
        terms=json.loads(value.removeprefix('sqrt_sum:'))
        if not isinstance(terms,list) or not terms or any(type(d)is not int or d<0 for d in terms):
            raise ValueError('Invalid exact radical sum')
        return terms
    try:
        a,b=radical_terms(left),radical_terms(right)
    except ValueError:
        return False
    # Identical terms are the common archive path. Avoid constructing a large
    # symbolic expression for a triangulation with thousands of edges.
    if a is not None and b is not None and sorted(a)==sorted(b):
        return True
    import sympy as sp
    def parse(value,terms):
        if terms is not None:
            return sp.Add(*(sp.sqrt(d) for d in terms))
        return sp.sympify(str(value).replace('sqrt2', 'sqrt(2)'), rational=True)
    return sp.simplify(parse(left,a) - parse(right,b)) == 0



def audit(task_ids):
    report = {'configurations': {}}
    for tid in task_ids:
        folder = ROOT / 'tasks' / tid.lower()
        path = folder / 'sota.json'
        if not path.exists():
            print(tid, 'awaiting task review', flush=True)
            continue
        records = json.loads(path.read_text())
        report['configurations'].update({cid:record.get('verification',{}) for cid,record in records['configurations'].items()})
        checker = importlib.import_module(f'tasks.{tid.lower()}.check')
        for config in load_task(tid)['configurations']:
            cid = config['id']
            record = {k:v for k,v in records['configurations'][cid].items() if k!='verification'}
            program = record.get('program')
            if not program:
                report['configurations'][cid] = dict(task_id=tid, status='pending_reproduction', record=record)
                continue
            output = folder / 'runs' / 'sota' / cid
            result = evaluate_candidate(tid, folder / program, cid, strict=True, output_dir=output)
            if not result['validity']:
                raise ValueError(f'{cid}: {result}')
            solution = json.loads((output / 'solution.json').read_text())
            checked = checker.validate(solution, config, strict=True)
            # Independently compute at least one mathematical quantity.
            quantity = independent_quantity(tid, solution, config)
            key = {'T099':'tile_count','T100':'triangle_count','T098':'outer_side','T095':'face_count','T097':'polygon_count','T093':'packed_value','T091':'row_count','T090':'energy','T088':'cutwidth','T087':'minimum_autocorrelation_ratio','T085':'radius','T084':'diameter','T082':'army_size','T081':'distance_ratio','T079':'union_cardinality','T078':'determinant','T075':'edge_count','T076':'largest_element','T074':'area_ratio','T073':'point_count','T072':'max_size','T071':'code_size','T070':'square_count','T069':'tour_cost','T068':'code_size','T067':'code_size','T066':'three_point_lines','T065':'unit_pairs','T064':'steiner_count','T062':'cardinality','T061':'edge_count','T060':'one_count','T058':'round_count','T059':'clique_cardinality','T057':'route_cost','T055':'satisfied_soft_weight','T056':'makespan','T054':'peak_sidelobe','T053':'minimum_factor','T051':'sequence_length','T052':'code_size','T050':'induced_path_edges','T049':'distance_count','T048':'comparator_count','T047':'difference_basis_size','T045':'linear_arrangement_cost','T044':'order','T043':'code_size','T042':'cardinality','T041':'sum_sides','T040':'volume','T039':'scope','T038':'square_count','T035':'point_count','T036':'crossings','T037':'direction_count','T034':'prefix_length','T032':'ones','T033':'cut_weight','T031':'string_length','T030':'color_count','T028':'makespan','T029':'rank_terms','T027':'quadratic_cost','T026':'prefix_length','T025':'points','T024':'edges','T022':'vertices','T023':'rows','T001':'radius','T003':'sum_radii','T005':'minimum_triangle_area',
                   'T006':'order','T007':'span','T012':'ratio','T008':'blocks',
                   'T009':'minimum_distance','T010':'codewords','T013':'energy',
                   'T014':'exact_objective','T015':'exact_objective','T016':'exact_objective',
                   'T017':'maximum_overlap','T011':'independent_words','T018':'absolute_determinant',
                   'T019':'diameter','T020':'additions'}.get(tid)
            if key:
                if tid == 'T012':
                    assert math.isclose(float(checked['objective']), quantity[key], rel_tol=1e-14)
                else:
                    assert Fraction(str(checked['objective'])) == Fraction(str(quantity[key]))
            elif tid in ('T096', 'T094', 'T092', 'T089', 'T086', 'T083', 'T021', 'T046', 'T063', 'T077', 'T080'):
                from scripts.review_search import check_quantity
                check_quantity(tid, quantity, result)
            elif tid == 'T004':
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
        for cid, record in records['configurations'].items():
            record['verification'] = {k:v for k,v in report['configurations'].get(cid,{}).items() if k!='record'}
        path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tasks', nargs='*', choices=INITIAL_TASKS)
    args = parser.parse_args()
    audit(args.tasks or INITIAL_TASKS)
