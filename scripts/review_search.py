"""Run main-review arithmetic checks and retain stronger saved witnesses."""
import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.registry import load_task
from mathbench.replay import read_witness_bytes, replay
from mathbench.saved_result import best_record_path, read_best_record, write_best_record
from scripts.audits.independent_audit import broken
from scripts.search import bounded_audit, save


QUANTITY_KEYS = {
    'T024': 'point_count',
    'T084': 'discrepancy',
    'T010':'tile_count','T036':'triangle_count','T009':'outer_side','T028':'face_count','T029':'polygon_count','T006':'packed_value','T055':'row_count','T075':'energy','T044':'cutwidth','T079':'minimum_autocorrelation_ratio','T007':'radius','T061':'diameter','T045':'army_size','T023':'distance_ratio','T066':'union_cardinality','T014':'determinant','T037':'edge_count','T062':'largest_element','T018':'area_ratio','T016':'point_count','T072':'max_size','T049':'code_size','T008':'square_count','T096':'tour_cost','T050':'code_size','T048':'code_size',
    'T022':'three_point_lines',
    'T021':'unit_pairs',
    'T026':'steiner_count',
    'T064':'cardinality',
    'T035':'edge_count',
    'T089':'one_count','T057':'round_count','T039':'clique_cardinality','T097':'route_cost','T098':'satisfied_soft_weight','T095':'makespan','T074':'peak_sidelobe','T090':'minimum_factor','T083':'sequence_length','T052':'code_size','T041': 'induced_path_edges',
    'T020': 'distance_count',
    'T099': 'comparator_count',
    'T060': 'difference_basis_size',
    'T043': 'linear_arrangement_cost',
    'T031': 'order',
    'T051': 'code_size',
    'T063': 'cardinality',
    'T004': 'sum_sides', 'T015': 'volume',
    'T059': 'scope',
    'T056': 'square_count',
    'T013': 'direction_count', 'T025': 'crossings',
    'T019': 'point_count',
    'T068': 'prefix_length',
    'T042': 'cut_weight',
    'T034': 'ones',
    'T038': 'color_count',
    'T100': 'string_length',
    'T094': 'makespan', 'T086': 'rank_terms',
    'T093': 'quadratic_cost',
    'T067': 'prefix_length',
    'T065': 'points',
    'T033': 'edges',
    'T032': 'vertices', 'T054': 'rows',
    'T001': 'radius', 'T002': 'sum_radii', 'T017': 'minimum_triangle_area',
    'T030': 'order', 'T058': 'span', 'T053': 'blocks', 'T046': 'minimum_distance',
    'T047': 'codewords', 'T040': 'independent_words', 'T073': 'energy',
    'T076': 'exact_objective', 'T078': 'exact_objective', 'T077': 'exact_objective',
    'T080': 'maximum_overlap', 'T085': 'absolute_determinant',
    'T087': 'diameter', 'T088': 'additions',
}


def objective_number(result):
    if result.get('validity') != 1:
        raise ValueError('A valid construction is required')
    return Fraction(str(result.get('objective_value', result['objective'])))


def better(candidate, previous, direction):
    a, b = objective_number(candidate), objective_number(previous)
    if direction == 'minimize':
        return a < b
    if direction == 'maximize':
        return a > b
    raise ValueError('Unknown objective direction')


def check_quantity(task, quantity, result):
    assert 'error' not in quantity, quantity
    if task in QUANTITY_KEYS:
        assert Fraction(str(quantity[QUANTITY_KEYS[task]])) == Fraction(str(result['objective']))
    elif task=='T082':
        a,b=map(Fraction,quantity['ratio_interval'])
        lo,hi=map(Fraction,result['details']['objective_interval'])
        assert lo<=a<=b<=hi and objective_number(result)==lo
        assert quantity['fourth_power_ratio']==result['details']['fourth_power_ratio']
        assert quantity['M2']==result['details']['sphere_average_M2']
        assert quantity['M4']==result['details']['sphere_average_M4']
    elif task in ('T027','T081'):
        a,b=map(Fraction,quantity['ratio_interval'])
        lo,hi=map(Fraction,result['details']['objective_interval'])
        assert lo<=a<=b<=hi and objective_number(result)==hi
    elif task=='T005':
        import sympy as sp
        lo,hi=map(Fraction,result['details']['objective_interval'])
        exact=sp.sympify(quantity['exact_side'])
        assert exact>=sp.Rational(lo.numerator,lo.denominator) and exact<=sp.Rational(hi.numerator,hi.denominator)
        assert objective_number(result)==hi
        assert hi-lo<Fraction(1,10**40)
    elif task in ('T070', 'T071'):
        a,b=map(Fraction,quantity['ratio_interval'])
        lo,hi=map(Fraction,result['details']['objective_interval'])
        assert lo<=a<=b<=hi
        assert Fraction(result['objective'])==lo
        assert hi-lo<lo*Fraction(1,10**70)
    elif task == 'T092':
        a,b=map(Fraction,quantity['mahler_interval'])
        lo,hi=map(Fraction,result['details']['objective_interval'])
        assert lo<=a<=b<=hi
        assert Fraction(result['objective'])==hi
        assert hi-lo<=lo*Fraction(1,10**10)
    elif task == 'T091':
        lo,hi = map(Fraction,result['details']['objective_interval'])
        if 'exact_supnorm' in quantity:
            a = b = Fraction(quantity['exact_supnorm'])
        else:
            a, b = map(Fraction, quantity['supnorm_interval'])
        assert max(lo, a) <= min(hi, b)
        assert b-a <= hi*Fraction(1,10**10)
        assert Fraction(result['objective']) == hi
        assert hi-lo <= hi*Fraction(1,10**10)
    elif task == 'T012':
        a, b = map(Fraction, quantity['energy_interval'])
        lo, hi = map(Fraction, result['details']['objective_interval'])
        assert max(a, lo) <= min(b, hi)
        assert Fraction(result['objective']) == hi
        assert hi-lo < Fraction(1, 10**18)
    elif task == 'T003':
        import sympy as sp
        assert sp.simplify(sp.sympify(quantity['bounding_side']) -
                           sp.sympify(str(result['objective']).replace('sqrt2', 'sqrt(2)'))) == 0
    elif task == 'T069':
        assert quantity['sumset'] == result['details']['sumset_size']
        assert quantity['difference_set'] == result['details']['difference_set_size']
        assert abs(quantity['ratio'] - float(result['objective'])) < 1e-12
    elif task == 'T011':
        import mpmath as mp
        with mp.workdps(80):
            angle = mp.mpf(quantity['minimum_angle_80_digits'])
            lo, hi = result['details']['angle_interval']
            assert mp.mpf(lo) - mp.mpf('1e-15') <= angle <= mp.mpf(hi) + mp.mpf('1e-15')
    else:
        raise ValueError('No independent objective check for ' + task)


def review(path, candidate_only=False):
    data = json.loads(path.read_text())
    manifest = json.loads((path.parent / 'manifest.json').read_text())
    expected = manifest.get('configuration_ids')
    # Do not write a summary while its search process is still adding rows.
    if not expected or len(data['configurations']) != len(expected):
        return 0
    task = data['task_id']
    review_date = datetime.now(timezone.utc).date().isoformat()
    directory = ROOT / 'tasks' / task.lower()
    task_metadata = load_task(task)
    configs = {c['id']: c for c in task_metadata['configurations']}
    assert all(hashlib.sha256((path.parent / 'sources' / name).read_bytes()).hexdigest() == digest
               for name, digest in manifest['source_sha256'].items())
    count = 0
    for row in data['configurations']:
        if row.get('status') in ('reviewed_by_sol', 'candidate_verified_controls_incomplete'):
            continue
        cid = row['config_id']
        if candidate_only and not row.get('best'):
            print('NO_VALID_CANDIDATE', cid, path.parent.name, flush=True)
            continue
        failed_evaluations = [name for name, r in row['results'].items() if r['validity'] != 1]
        assert candidate_only or not failed_evaluations, (cid, 'Invalid evaluation')
        warm_hash = manifest.get('warm_start_sha256', {}).get(cid)
        if warm_hash:
            assert hashlib.sha256((path.parent / cid / 'warm_start.json').read_bytes()).hexdigest() == warm_hash
        result = row['results'][row['best']]
        objective_number(result)  # A failed selected construction can never pass this review.
        witness = path.parent / cid / row['best'] / 'solution.json'
        solution = json.loads(witness.read_text())
        destination = directory / 'runs' / f'sol_optimize_review_{review_date.replace("-", "")}' / cid / path.parent.name
        checked = replay(task, witness, cid, strict=True, output_dir=destination / 'replay')
        assert checked['validity'] == 1 and checked['objective'] == result['objective'], checked
        checker = importlib.import_module(f'tasks.{task.lower()}.check')
        raw = checker.validate(solution, configs[cid], strict=True)
        changed = copy.deepcopy(solution)
        changed.update(objective='999999999', score='999999999', claimed_score='999999999')
        assert checker.validate(changed, configs[cid], strict=True)['objective'] == raw['objective']
        try:
            checker.validate(broken(task, solution), configs[cid], strict=True)
        except (ValueError, TypeError, KeyError, AssertionError):
            pass
        else:
            raise AssertionError('Damaged construction accepted: ' + cid)
        quantity = bounded_audit(task, solution, dict(configs[cid], id='search-check'))
        check_quantity(task, quantity, result)
        record = dict(reviewer='Sol main agent', status='reviewed_by_sol', date=review_date,
                      source_summary=str(path.relative_to(ROOT)), source_hashes_verified=True,
                      independent_quantity=quantity, claimed_score_ignored=True,
                      damaged_construction_rejected=True,
                      initial_baseline_human_valid=all(row['results'][name]['validity'] == 1 for name in ('initial', 'baseline', 'human')),
                      scope='Own-construction continuation; not an isolated model comparison or a public record claim.')
        if failed_evaluations:
            record.update(failed_evaluations=failed_evaluations,
                          review_scope='Selected saved construction only. Failed evaluations remain failed; this does not accept the full run or establish a controlled program comparison.')
        if manifest.get('search_agent'):
            record['search_agent'] = manifest['search_agent']
        if manifest.get('native_kernel'):
            record['native_kernel'] = manifest['native_kernel']
        if manifest.get('generation_record'):
            record['generation_record'] = manifest['generation_record']
        save(destination / 'review.json', dict(record, strict_replay=checked))
        best = best_record_path(directory / 'data')
        saved = read_best_record(best) if best.is_file() else {}
        previous = saved.get('result')
        improved = (previous is None or previous.get('config_id') != cid
                    or better(result, previous, configs[cid]['direction']))
        if improved:
            if previous is not None:
                backup = path.parent / 'previous_best' / cid
                if backup.exists():
                    raise ValueError('Previous best backup already exists: ' + str(backup))
                backup.mkdir(parents=True)
                shutil.copy2(best, backup / best.name)
            record.update(classification='ai_assisted_local_continuation', seed=result['seed'],
                          controls=manifest['controls'], budget=result['budget'],
                          environment=result['environment'], source_sha256=manifest['source_sha256'],
                          warm_start_sha256=warm_hash,
                          replay_command=f'.venv/bin/python -m mathbench replay {task} {best.relative_to(ROOT)} --config {cid}')
            write_best_record(best, result, record, witness.read_bytes(),
                              initial_result=saved.get('initial_result', row['results']['initial']))
        row.update(status='candidate_verified_controls_incomplete' if failed_evaluations else 'reviewed_by_sol', sol_review=str((destination / 'review.json').relative_to(ROOT)))
        count += 1
        print('REVIEWED', cid, 'PROMOTED' if improved else 'kept prior best', flush=True)
    save(path, data)
    return count


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', default='search_optimize_20261106')
    parser.add_argument('--candidate-only', action='store_true',
                        help='Review a valid selected witness while retaining failed controls or other candidates as failed. Does not accept the full run.')
    args = parser.parse_args()
    total = sum(review(p, candidate_only=args.candidate_only) for p in sorted((ROOT / 'tasks').glob(f'*/runs/{args.prefix}*/summary.json')))
    print('Reviewed', total, 'new attempt/configuration results')
