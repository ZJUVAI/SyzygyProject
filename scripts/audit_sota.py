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
        path = folder / 'data/bestknown.json'
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
            key = {'T010':'tile_count','T036':'triangle_count','T009':'outer_side','T028':'face_count','T029':'polygon_count','T006':'packed_value','T055':'row_count','T075':'energy','T044':'cutwidth','T079':'minimum_autocorrelation_ratio','T007':'radius','T061':'diameter','T045':'army_size','T023':'distance_ratio','T066':'union_cardinality','T014':'determinant','T037':'edge_count','T062':'largest_element','T018':'area_ratio','T016':'point_count','T072':'max_size','T049':'code_size','T008':'square_count','T096':'tour_cost','T050':'code_size','T048':'code_size','T022':'three_point_lines','T021':'unit_pairs','T026':'steiner_count','T064':'cardinality','T035':'edge_count','T089':'one_count','T057':'round_count','T039':'clique_cardinality','T097':'route_cost','T098':'satisfied_soft_weight','T095':'makespan','T074':'peak_sidelobe','T090':'minimum_factor','T083':'sequence_length','T052':'code_size','T041':'induced_path_edges','T020':'distance_count','T099':'comparator_count','T060':'difference_basis_size','T043':'linear_arrangement_cost','T031':'order','T051':'code_size','T063':'cardinality','T004':'sum_sides','T015':'volume','T059':'scope','T056':'square_count','T019':'point_count','T025':'crossings','T013':'direction_count','T068':'prefix_length','T034':'ones','T042':'cut_weight','T100':'string_length','T038':'color_count','T094':'makespan','T086':'rank_terms','T093':'quadratic_cost','T067':'prefix_length','T065':'points','T033':'edges','T032':'vertices','T054':'rows','T001':'radius','T002':'sum_radii','T017':'minimum_triangle_area',
                   'T030':'order','T058':'span','T069':'ratio','T053':'blocks',
                   'T046':'minimum_distance','T047':'codewords','T073':'energy',
                   'T076':'exact_objective','T078':'exact_objective','T077':'exact_objective',
                   'T080':'maximum_overlap','T040':'independent_words','T085':'absolute_determinant',
                   'T087':'diameter','T088':'additions'}.get(tid)
            if key:
                if tid == 'T069':
                    assert math.isclose(float(checked['objective']), quantity[key], rel_tol=1e-14)
                else:
                    assert Fraction(str(checked['objective'])) == Fraction(str(quantity[key]))
            elif tid in ('T027', 'T082', 'T081', 'T005', 'T012', 'T091', 'T092', 'T070', 'T071', 'T024', 'T084'):
                from scripts.review_search import check_quantity
                check_quantity(tid, quantity, result)
            elif tid == 'T011':
                assert math.isclose(checked['objective'], float(quantity['minimum_angle_80_digits']), rel_tol=1e-14)
            elif tid == 'T003':
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
