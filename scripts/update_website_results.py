"""Copy accepted best witnesses into an existing Atlas source checkout."""
import argparse
import csv
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def read(path):
    return json.loads(path.read_text())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def number(value):
    return float(Fraction(str(value)))


def visual(task, w, params, template):
    """Produce drawing projections only. Saved checker results supply scores."""
    v = dict(template)
    if task == 'T001':
        v['circles'] = [[*map(number, p), number(w['radius'])] for p in w['centers']]
    elif task == 'T003':
        v['circles'] = [[number(c[k]) for k in ('x', 'y', 'r')] for c in w['circles']]
    elif task == 'T002':
        from tasks.t002.check import corners
        def qfloat(q):
            return float(q.a) + float(q.b) * 2**.5
        polygons = [[[qfloat(x), qfloat(y)] for x, y in corners(s)] for s in w['squares']]
        xs = [p[0] for s in polygons for p in s]
        ys = [p[1] for s in polygons for p in s]
        side = max(max(xs)-min(xs), max(ys)-min(ys))
        v.update(polygons=polygons, bounds=[min(xs), min(ys), side, side])
    elif task in ('T004', 'T005'):
        pts = [[number(x) for x in p] for p in w['points']]
        v['points'] = pts
        if task == 'T004':
            v['pair'] = list(min(combinations(range(len(pts)), 2), key=lambda ij: sum((a-b)**2 for a,b in zip(pts[ij[0]],pts[ij[1]]))))
        else:
            def area(ijk):
                a,b,c = (pts[i] for i in ijk)
                return abs((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
            v['triangle'] = list(min(combinations(range(len(pts)), 3), key=area))
    elif task == 'T006':
        v.update(vertices=w['vertices'], edges=w['edges'])
    elif task == 'T007':
        a = sorted(w['marks'])
        v.update(marks=a, matrix=[[abs(x-y) for y in a] for x in a])
    elif task == 'T008':
        v.update(v=params['v'], t=params['t'], blocks=w['blocks'], matrix=[[int(i in b) for i in range(params['v'])] for b in w['blocks']])
    elif task in ('T009', 'T010'):
        if task == 'T009':
            rows = w['generator_matrix']
            ints = [sum(x << i for i,x in enumerate(r)) for r in rows]
            words = [0]
            for r in ints:
                words += [x ^ r for x in words]
        else:
            words = w['codewords']
            rows = [[(x >> i) & 1 for i in range(params['n'])] for x in words]
        distribution = [0] * (params['n']+1)
        for x in words:
            distribution[x.bit_count()] += 1
        v.update(matrix=rows, distribution=distribution)
    elif task == 'T011':
        rows = w['words']
        v.update(matrix=rows, distribution=[[sum(r[i] == s for r in rows) for s in range(params['q'])] for i in range(len(rows[0]))])
    elif task == 'T012':
        a = sorted(w['set'])
        v['sets'] = [a, sorted({x+y for x in a for y in a}), sorted({x-y for x in a for y in a})]
    elif task == 'T013':
        a = w['sequence']
        v.update(sequence=a, correlation=[sum(a[i]*a[i+k] for i in range(len(a)-k)) for k in range(1,len(a))])
    elif task in ('T014', 'T015', 'T016'):
        a = [number(x) for x in w['coefficients']]
        n = len(a)
        a = [x*2*n/sum(a) for x in a]
        conv = [sum(a[i]*a[k-i] for i in range(max(0,k-n+1),min(n-1,k)+1))/(2*n) for k in range(2*n-1)]
        v.update(profile=a, curve=[0,*conv,0])
    elif task == 'T017':
        from tasks.t017.check import lag_integral
        a = [Fraction(x) for x in w['heights']]
        v.update(profile=[float(x) for x in a], curve=[0,*[float(lag_integral(a,k)) for k in range(1-len(a),len(a))],0])
    elif task == 'T018':
        v['matrix'] = w['matrix']
    elif task == 'T019':
        a = sorted(w['tuple'])
        v.update(exact=list(map(str,a)), positions=[(x-a[0])/(a[-1]-a[0]) for x in a], gap_bits=[(y-x).bit_length() for x,y in zip(a,a[1:])], residues={p:[sum(x%int(p)==r for x in a) for r in range(int(p))] for p in v['residues']})
    elif task == 'T020':
        a = w['chain']
        deps = [[]]
        for i,x in enumerate(a[1:],1):
            seen = {y:j for j,y in enumerate(a[:i])}
            deps.append(next([j,seen[x-y]] for j,y in enumerate(a[:i]) if x-y in seen))
        v.update(exact=list(map(str,a)), bits=[x.bit_length() for x in a], dependencies=deps)
    else:
        raise ValueError(task)
    return v


def active_assets(value):
    if isinstance(value, str) and value.startswith('data/assets/'):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from active_assets(item)
    elif isinstance(value, list):
        for item in value:
            yield from active_assets(item)


def update(checkout, initial_witnesses=None):
    dist = checkout/'dist'
    index = read(dist/'data/index.json')
    own_records = []
    def asset_bytes(raw, suffix='json'):
        name = f'data/assets/{hashlib.sha256(raw).hexdigest()}.{suffix}'
        (dist/name).write_bytes(raw)
        return name
    def asset(value):
        return asset_bytes(encoded(value))
    from mathbench.registry import INITIAL_TASKS, load_task
    from scripts.result_table import display
    from scripts.website_figures import project, grid

    def approximation(value):
        return float(display(value, digits=16))

    def score(run, program, **assets):
        return {
            'program': program, 'objective': str(run['objective']),
            'objective_approx': approximation(run.get('objective_value', run['objective'])),
            'combined_score': run.get('combined_score'),
            'verification_status': run.get('verification_status'),
            **assets,
        }

    def labels(value):
        return dict(en=value, zh=value)

    previous = {task['id']: task for task in index['tasks']}
    tasks = []
    for tid in INITIAL_TASKS:
        folder = ROOT/'tasks'/tid.lower()
        metadata = load_task(tid)
        sota = read(folder/'sota.json')['configurations']
        initial_results = read(folder/'records.json').get('initial_results', {})
        old = previous.get(tid, {})
        existing = {c['id']: c for c in old.get('configurations', [])}
        category = metadata.get('category', 'Other constructions').replace('_', ' ')
        task = {**old, 'id': tid, 'name': old.get('name', labels(metadata['name'])),
                'description': old.get('description', labels('')),
                'metric': old.get('metric', labels('')),
                'category': old.get('category', labels(category)), 'configurations': []}
        tasks.append(task)
        task_template = next((read(dist/c['asset']).get('drawing_template')
                              for c in existing.values()
                              if read(dist/c['asset']).get('drawing_template')), None)
        for config in metadata['configurations']:
            cid = config['id']
            params = config['parameters']
            path = f'data/configurations/{cid}.json'
            data = read(dist/path) if (dist/path).exists() else {'runs': [], 'records': {}}
            runs = data['runs']
            record = sota[cid]
            previous_public = data.get('sota', {}).get('run') or {}
            best = folder/'best'/cid
            result = read(best/'result.json')
            provenance = read(best/'provenance.json')
            if (provenance.get('status') not in ('reviewed_by_sol', 'accepted_by_sol')
                    or result['validity'] != 1 or result['config_id'] != cid):
                raise ValueError(f'Unreviewed saved result: {cid}')

            template = data.get('drawing_template') or task_template

            def construction(run, program, witness_path):
                if not witness_path or not witness_path.is_file():
                    raise ValueError(f'{cid}: missing {program} witness')
                raw = witness_path.read_bytes()
                witness = asset_bytes(raw, 'jsonraw')
                solution = json.loads(raw)
                if tid == 'T011' and len(solution['words'][0]) != 3:
                    projection = grid(solution['words'], 'Independent-set words', '独立集的元组', categorical=True)
                elif template:
                    projection = visual(tid, solution, params, read(dist/template))
                else:
                    projection = project(tid, solution, params)
                return score(run, program, witness=witness, visual=asset(projection))

            own = construction(result, 'own', best/'solution.json')
            own.update(result=asset(result), evidence=asset(provenance))
            initial = initial_results[cid]
            if initial_witnesses:
                initial_folder = initial_witnesses/cid
                checked = read(initial_folder/'result.json')
                if checked['validity'] != 1 or checked['objective'] != initial['objective']:
                    raise ValueError(f'{cid}: initial witness does not match the release score')
                initial_path = initial_folder/'solution.json'
            else:
                initial_path = dist/runs[0]['witness'] if runs and runs[0].get('witness') else None
            runs[:] = [construction(initial, 'init_program', initial_path)]
            public = record['verification']['run']
            assert public['validity'] == 1, cid
            if previous_public.get('objective') == str(public['objective']) and previous_public.get('witness'):
                witness_path = dist/previous_public['witness']
            else:
                witness_name = (record['verification'].get('witness') or record.get('witness')
                                or record.get('best_reproduced', {}).get('witness'))
                witness_path = folder/witness_name if isinstance(witness_name, str) else None
            public_run = construction(public, 'sota', witness_path)
            source = record.get('public_source') or record.get('best_public') or {}
            if isinstance(source, str):
                source = {'source': source}
            public_source = dict(source)
            reproduced = record.get('best_reproduced')
            if not public_source.get('url') and isinstance(reproduced, dict) and reproduced.get('url'):
                public_source['url'] = reproduced['url']
            reported = record.get('highest_reported') or {}
            if reported:
                source = reported.get('source') or public_source
                if isinstance(source, str):
                    source = {'source': source, 'url': reported.get('url') or public_source.get('url')}
                reported = {'value': str(reported['value']), 'value_approx': approximation(reported['value']),
                            'source': source}
            replay = {'record': {'public_source': public_source,
                                  'public_value': str(record['public_value']) if record.get('public_value') is not None else None,
                                  'highest_reported': reported or None},
                      'run': public_run}
            if record.get('public_value') is not None:
                replay['public_value_approx'] = approximation(record['public_value'])
            view = dict(id=cid, task_id=tid, parameters=params, direction=config['direction'],
                        runs=runs, sota=replay, own=own)
            data.update(view)
            task['configurations'].append({**view, 'asset': path,
                'gallery_visual': public_run['visual']})
            (dist/path).write_bytes(encoded(data))
            own_records.append({'task_id':tid,'config_id':cid,**own})
    index.update(tasks=tasks, version='1.0.0', date='2026-11-07', own_result_count=len(own_records),
                 counts=dict(tasks=len(tasks), configurations=len(own_records), runs=sum(len(c['runs']) for t in tasks for c in t['configurations']),
                             categories=len({task['category']['en'] for task in tasks})))
    (dist/'data/index.json').write_bytes(encoded(index))
    (dist/'data/own_results.json').write_bytes(encoded({'updated':index['date'],'count':len(own_records),'results':own_records}))
    # Export the current verified search results.
    csv_path = dist/'data/results.csv'
    fields = ['task_id', 'configuration', 'program', 'direction', 'objective', 'score', 'verification']
    rows = []
    for r in own_records:
        data = next(c for t in index['tasks'] for c in t['configurations'] if c['id']==r['config_id'])
        rows.append(dict(task_id=r['task_id'],configuration=r['config_id'],program='own',direction=data['direction'],objective=r['objective'],score=r['combined_score'],verification=r['verification_status']))
    with csv_path.open('w', newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator=chr(10));writer.writeheader();writer.writerows(rows)
    configurations = {c['asset'] for task in tasks for c in task['configurations']}
    assets = set(active_assets(index))
    for path in configurations:
        assets.update(active_assets(read(dist/path)))
    for folder, active in (('assets', assets), ('configurations', configurations)):
        for path in (dist/'data'/folder).iterdir():
            if path.is_file() and path.relative_to(dist).as_posix() not in active:
                path.unlink()
    manifest = {str(p.relative_to(dist/'data')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((dist/'data').rglob('*')) if p.is_file() and p.name!='manifest.json'}
    (dist/'data/manifest.json').write_bytes(encoded(manifest))
    print(f'Updated {len(own_records)} verified best results and construction figures.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout',type=Path,default=ROOT/'website')
    parser.add_argument('--initial-witnesses', type=Path,
                        help='Directory containing a checked initial result and solution for each config')
    args = parser.parse_args()
    update(args.checkout, args.initial_witnesses)
