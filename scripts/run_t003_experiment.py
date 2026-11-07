"""Archive one exploratory T003-C01 program with independent exact checks."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.evaluate import evaluate_candidate
from scripts.run_t003_evolution import archive_sources, audit_witness, experiment_environment


def write(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--program', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('--cpu', type=int, required=True)
    p.add_argument('--steps', type=int, default=1000)
    p.add_argument('--search-seconds', type=float, default=240)
    p.add_argument('--generation-seconds', type=float, default=300,
                   help='Explicit generation limit for larger exploratory runs')
    args = p.parse_args()
    if args.cpu not in os.sched_getaffinity(0):
        p.error('CPU must be in the process affinity set')
    if args.steps <= 0 or not 0 < args.search_seconds <= args.generation_seconds - 30:
        p.error('steps must be positive; search-seconds must leave 30 seconds before the generation limit')
    if not 30 < args.generation_seconds <= 3600:
        p.error('generation-seconds must be in (30, 3600]')
    os.sched_setaffinity(0, {args.cpu})
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[key] = '1'
    os.environ['MATHBENCH_SEARCH_SECONDS'] = str(args.search_seconds)
    os.environ['MATHBENCH_EXPERIMENT_STEPS'] = str(args.steps)
    dest = args.output.resolve()
    dest.mkdir(parents=True, exist_ok=False)
    sources = dest/'sources'
    sources.mkdir()
    source = args.program.resolve(strict=True)
    # Experimental programs must be standalone; no mutable local helper modules.
    shutil.copy2(source, sources/'program.py')
    hashes = archive_sources(sources, ('tasks/t003/check.py', 'tasks/t003/task.json', 'mathbench/evaluate.py',
                     'mathbench/worker.py', 'mathbench/registry.py', 'mathbench/replay.py',
                     'scripts/run_t003_evolution.py', 'scripts/run_t003_experiment.py'))
    hashes['program.py'] = hashlib.sha256((sources/'program.py').read_bytes()).hexdigest()
    manifest = {'task_id':'T003', 'config_id':'T003-C01', 'started_utc':datetime.now(timezone.utc).isoformat(),
                'seed':args.seed, 'source_program':str(source), 'source_sha256':hashes,
                'invocation_argv':[sys.executable, *sys.argv],
                'controls':{'MATHBENCH_EXPERIMENT_STEPS':args.steps, 'MATHBENCH_SEARCH_SECONDS':args.search_seconds},
                'budget':{'generation_seconds':args.generation_seconds, 'verification_seconds':60, 'memory_bytes':4*1024**3, 'threads':1},
                'environment':dict(experiment_environment(), cpu=args.cpu),
                'scope':'Exploratory AI-designed search; separate from the previous fixed-budget comparison.'}
    write(dest/'manifest.json', manifest)
    result = evaluate_candidate('T003', sources/'program.py', 'T003-C01', strict=True,
                                seed=args.seed, generation_timeout=args.generation_seconds,
                                output_dir=dest/'candidate')
    print(json.dumps(result), flush=True)
    if result['validity'] != 1 or 'artifact_error' in result:
        raise RuntimeError('Candidate failed; result saved')
    summary = audit_witness(dest/'candidate/solution.json', result['objective'])
    summary.update(seed=args.seed, objective=result['objective'],
                   generation_seconds=result['generation_time'],
                   verification_scope='Exact rational feasibility and attained score; no optimality proof.')
    write(dest/'summary.json', summary)
    print(json.dumps(summary), flush=True)
    if not summary['passed']:
        raise RuntimeError('Exact experiment audit failed')


if __name__ == '__main__':
    main()
