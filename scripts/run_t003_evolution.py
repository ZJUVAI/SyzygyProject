"""Run and archive a T003-C01 evolutionary construction experiment."""
import argparse
import copy
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.evaluate import evaluate_candidate
from mathbench.registry import load_config
from mathbench.replay import replay
from tasks.t003.check import validate


def independent_audit(solution):
    """Recompute all inequalities without calling the benchmark checker."""
    circles = [tuple(Fraction(c[k]) for k in ('x', 'y', 'r')) for c in solution['circles']]
    if len(circles) != 26:
        raise ValueError('Expected 26 circles')
    walls = [v for x, y, r in circles for v in (x-r, y-r, 1-x-r, 1-y-r)]
    pairs = [(x-a)**2 + (y-b)**2 - (r+s)**2
             for i, (x, y, r) in enumerate(circles) for a, b, s in circles[:i]]
    if min(r for _, _, r in circles) <= 0 or min(walls) < 0 or min(pairs) < 0:
        raise ValueError('Independent feasibility audit failed')
    return {'objective': str(sum((r for _, _, r in circles), Fraction())),
            'minimum_wall_slack': str(min(walls)),
            'minimum_squared_pair_slack': str(min(pairs)), 'pair_checks': len(pairs)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--generations', type=int, default=12)
    parser.add_argument('--population', type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.generations <= 2000 or not 4 <= args.population <= 48:
        parser.error('generations must be 1..2000 and population must be 4..48')
    destination = args.output.resolve()
    # An experiment directory is immutable after creation; do not mix old witnesses.
    destination.mkdir(parents=True, exist_ok=False)
    controls = {'MATHBENCH_EVOLUTION_GENERATIONS': str(args.generations),
                'MATHBENCH_EVOLUTION_POPULATION': str(args.population)}
    os.environ.update(controls)
    sources = destination / 'sources'
    sources.mkdir()
    hashes = {}
    for name in ('tasks/t003/evolution.py', 'tasks/t003/init_program.py',
                 'tasks/t003/check.py', 'tasks/t003/task.json',
                 'scripts/run_t003_evolution.py', 'mathbench/evaluate.py',
                 'mathbench/worker.py', 'mathbench/replay.py', 'mathbench/registry.py'):
        content = (ROOT / name).read_bytes()
        target = sources / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        hashes[name] = hashlib.sha256(content).hexdigest()
    command = [sys.executable, 'scripts/run_t003_evolution.py', '--output', str(destination)+'-rerun',
               '--seed', str(args.seed), '--generations', str(args.generations),
               '--population', str(args.population)]
    import numpy
    import scipy
    manifest = {'task_id': 'T003', 'config_id': 'T003-C01', 'seed': args.seed,
                'started_utc': datetime.now(timezone.utc).isoformat(), 'controls': controls,
                'source_sha256': hashes, 'reproduce_command': shlex.join(command),
                'replay_command': shlex.join([sys.executable, '-m', 'mathbench', 'replay',
                    'T003', str(destination / 'evolution/solution.json'), '--config', 'T003-C01']),
                'environment': {'python': sys.version, 'platform': platform.platform(),
                    'machine': platform.machine(), 'numpy': numpy.__version__, 'scipy': scipy.__version__},
                'scope': 'Construction evolution for one public configuration; no optimality claim.',
                'isolation': 'Local resource limits only; not a security sandbox.'}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    results = {}
    for label, program in [('initial', ROOT/'tasks/t003/init_program.py'),
                           ('evolution', sources/'tasks/t003/evolution.py')]:
        results[label] = evaluate_candidate('T003', program, 'T003-C01', strict=True,
                                           seed=args.seed, output_dir=destination/label)
        print(label, json.dumps(results[label]), flush=True)
        if results[label]['validity'] != 1 or 'artifact_error' in results[label]:
            raise RuntimeError(f'{label} failed; see saved result')
    solution_path = destination/'evolution/solution.json'
    solution = json.loads(solution_path.read_text())
    audit = independent_audit(solution)
    config = load_config('T003', 'T003-C01')
    modified = copy.deepcopy(solution)
    modified['objective'] = '999999'
    tampered = validate(modified, config, strict=True)
    damaged = copy.deepcopy(solution)
    damaged['circles'][1] = dict(damaged['circles'][0])
    try:
        validate(damaged, config, strict=True)
    except ValueError:
        rejected = True
    else:
        rejected = False
    replayed = replay('T003', solution_path, 'T003-C01', strict=True,
                      output_dir=destination/'replay')
    passed = (audit['objective'] == results['evolution']['objective'] == tampered['objective']
              == replayed['objective'] and replayed['validity'] == 1 and rejected
              and Fraction(audit['objective']) >= Fraction(results['initial']['objective']))
    summary = {'passed': passed, 'independent_audit': audit, 'damaged_witness_rejected': rejected,
               'claimed_score_ignored': tampered['objective'] == audit['objective'],
               'initial_objective': results['initial']['objective'],
               'improvement': str(Fraction(audit['objective'])-Fraction(results['initial']['objective'])),
               'verification_scope': 'Exact rational feasibility and attained value; no global optimality proof.'}
    (destination/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    if not passed:
        raise RuntimeError('Experiment audit failed')


if __name__ == '__main__':
    main()
