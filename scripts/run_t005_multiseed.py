"""Archive fixed-budget T005-C01 runs and compare their best exact witness."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.replay import replay
from scripts.run_t005_evolution import independent_audit


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')



def compare_runs(summary, manifest, previous):
    """Compare fixed-budget batches using exact rational objectives."""
    old = json.loads((previous/'summary.json').read_text())
    old_manifest = json.loads((previous/'manifest.json').read_text())
    for key in ('seeds', 'generations_per_seed', 'population',
                'generation_limit_seconds_per_seed', 'verification_limit_seconds',
                'threads_per_run', 'memory_bytes_per_run'):
        if manifest[key] != old_manifest[key]:
            raise ValueError(f'Comparison budgets differ: {key}')
    if not old['all_runs_passed'] or not summary['all_runs_passed']:
        raise ValueError('Comparison requires complete valid batches')
    old_runs = {r['seed']: r for r in old['runs']}
    deltas = [{'seed': r['seed'], 'previous_objective': old_runs[r['seed']]['objective'],
               'new_objective': r['objective'],
               'improvement': str(Fraction(r['objective'])-Fraction(old_runs[r['seed']]['objective']))}
              for r in summary['runs']]
    before, after = Fraction(old['best_objective']), Fraction(summary['best_objective'])
    return {'previous_directory': str(previous),
            'previous_summary_sha256': hashlib.sha256((previous/'summary.json').read_bytes()).hexdigest(),
            'same_budgets': True, 'paired_seed_results': deltas,
            'previous_best_objective': str(before), 'best_improvement': str(after-before),
            'previous_mean_objective': old['mean_objective'],
            'mean_improvement': summary['mean_objective']-old['mean_objective'],
            'seeds_improved': sum(Fraction(d['improvement']) > 0 for d in deltas),
            'previous_total_generation_seconds': old['total_generation_seconds']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--seeds', nargs='+', type=int, default=list(range(6)))
    parser.add_argument('--generations', type=int, default=1000)
    parser.add_argument('--population', type=int, default=12)
    parser.add_argument('--compare', type=Path, help='Previous batch with the same seeds and budgets')
    parser.add_argument('--public-snapshot', type=Path, help='Use saved table.html and coordinates.txt instead of downloading')
    args = parser.parse_args()
    if len(set(args.seeds)) != len(args.seeds):
        parser.error('seeds must be distinct')
    if not 1 <= args.generations <= 2000 or not 4 <= args.population <= 48:
        parser.error('invalid generation or population budget')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    public = output/'public'
    public.mkdir()
    urls = {'table.html': 'https://www.packomania.com/csqv/csqv.html',
            'coordinates.txt': 'https://www.packomania.com/csqv/txt/csqv26.txt'}
    hashes = {}
    for name, url in urls.items():
        if args.public_snapshot is not None:
            data = (args.public_snapshot/name).read_bytes()
        else:
            request = urllib.request.Request(url, headers={'User-Agent': 'Mathbench research'})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
        (public/name).write_bytes(data)
        hashes[name] = hashlib.sha256(data).hexdigest()
    # Parse the table's N=26 row, not another instance or a coordinate sum.
    from html import unescape
    import re
    table = (public/'table.html').read_text()
    rows = re.findall(r'<tr\b[^>]*>(.*?)</tr>', table, flags=re.I|re.S)
    selected = []
    for row in rows:
        cells = re.findall(r'<td\b[^>]*>(.*?)</td>', row, flags=re.I|re.S)
        text = [unescape(re.sub('<[^>]+>', '', c)).strip() for c in cells]
        if len(text) >= 2 and text[0] == '26':
            selected.append(text[1])
    if len(selected) != 1:
        raise ValueError('Cannot identify a unique N=26 public table row')
    public_value = Fraction(selected[0])
    shutil.copy2(ROOT/'tasks/t005/sota.json', public/'sota_archive.json')
    shutil.copy2(ROOT/'tasks/t005/data/sota26.json', public/'solution.json')
    public_replay = replay('T005', public/'solution.json', 'T005-C01', strict=True,
                           output_dir=public/'replay')
    if public_replay['validity'] != 1:
        raise ValueError('Public conservative witness failed replay')
    # Verify this is still the coordinate source used for the conservative witness.
    current_coordinates = (public/'coordinates.txt').read_text().split()
    archived_coordinates = (ROOT/'tasks/t005/data/packomania26_source.txt').read_text().split()
    coordinates_match = current_coordinates == archived_coordinates
    manifest = {'task_id': 'T005', 'config_id': 'T005-C01', 'started_utc': datetime.now(timezone.utc).isoformat(),
                'seeds': args.seeds, 'generations_per_seed': args.generations, 'population': args.population,
                'generation_limit_seconds_per_seed': 300, 'verification_limit_seconds': 60,
                'threads_per_run': 1, 'memory_bytes_per_run': 4*1024**3,
                'execution': 'sequential; fixed iteration budgets',
                'comparison_previous': str(args.compare.resolve()) if args.compare else None,
                'invocation_argv': [sys.executable, *sys.argv], 'public_urls': urls,
                'public_source_sha256': hashes, 'public_table_value': str(public_value),
                'public_source_mode': 'saved_snapshot' if args.public_snapshot else 'live_download',
                'public_snapshot_directory': str(args.public_snapshot.resolve()) if args.public_snapshot else None,
                'public_coordinate_source_matches_archive': coordinates_match,
                'public_conservative_objective': public_replay['objective'],
                'comparison_scope': 'Best known in the checked Packomania table, not a global upper bound.',
                'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    shutil.copy2(__file__, output/Path(__file__).name)
    write_json(output/'manifest.json', manifest)
    runs = []
    for seed in args.seeds:
        folder = output/f'seed_{seed}'
        command = [sys.executable, str(ROOT/'scripts/run_t005_evolution.py'), '--output', str(folder),
                   '--seed', str(seed), '--generations', str(args.generations), '--population', str(args.population)]
        with (output/f'seed_{seed}.log').open('w') as log:
            proc = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        result_file = folder/'evolution/result.json'
        result = json.loads(result_file.read_text()) if result_file.exists() else {}
        summary_file = folder/'summary.json'
        summary = json.loads(summary_file.read_text()) if summary_file.exists() else {}
        passed = proc.returncode == 0 and summary.get('passed') is True and result.get('validity') == 1
        runs.append({'seed': seed, 'passed': passed, 'returncode': proc.returncode,
                     'objective': result.get('objective') if passed else None,
                     'generation_seconds': result.get('generation_time'),
                     'error': result.get('error'), 'directory': folder.name})
        write_json(output/'progress.json', runs)
        print(json.dumps(runs[-1]), flush=True)
    valid = [r for r in runs if r['passed']]
    if not valid:
        raise RuntimeError('No verified run; inspect progress and logs')
    winner = max(valid, key=lambda r: Fraction(r['objective']))
    best = output/'best'
    best.mkdir()
    shutil.copy2(output/winner['directory']/'evolution/solution.json', best/'solution.json')
    checked = replay('T005', best/'solution.json', 'T005-C01', strict=True, output_dir=best/'replay')
    audit = independent_audit(json.loads((best/'solution.json').read_text()))
    assert checked['validity'] == 1 and checked['objective'] == audit['objective'] == winner['objective']
    score = Fraction(winner['objective'])
    gap = public_value-score
    summary = {'all_runs_passed': len(valid) == len(runs), 'runs': runs, 'best_seed': winner['seed'],
               'best_objective': str(score), 'best_objective_decimal': float(score),
               'independent_audit': audit, 'public_displayed_value': selected[0],
               'gap_to_public_displayed': str(gap), 'gap_to_public_displayed_decimal': float(gap),
               'percent_below_public_displayed': float(100*gap/public_value),
               'ratio_to_public_displayed': float(score/public_value),
               'gap_to_conservative_public_witness': str(Fraction(public_replay['objective'])-score),
               'valid_runs': len(valid), 'total_runs': len(runs),
               'mean_objective': statistics.mean(float(Fraction(r['objective'])) for r in valid),
               'median_objective': statistics.median(float(Fraction(r['objective'])) for r in valid),
               'minimum_objective': str(min(Fraction(r['objective']) for r in valid)),
               'total_generation_seconds': sum(r['generation_seconds'] or 0 for r in runs),
               'limitations': ['The public displayed value is rounded.',
                    'The conservative public witness is slightly below that displayed value.',
                    'A best-known public construction is not an optimality bound.',
                    'Search reproduction depends on saved numeric package versions.']}
    if args.compare is not None:
        previous = args.compare.resolve()
        summary['comparison'] = compare_runs(summary, manifest, previous)
        (output/'previous').mkdir()
        for name in ('summary.json', 'manifest.json'):
            shutil.copy2(previous/name, output/'previous'/name)
    write_json(output/'summary.json', summary)
    print(json.dumps(summary, indent=2), flush=True)
    if not summary['all_runs_passed']:
        raise RuntimeError('Some runs failed; best result saved but batch is incomplete')


if __name__ == '__main__':
    main()
