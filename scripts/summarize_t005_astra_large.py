"""Independently review the larger Astra T005-C01 campaign."""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.registry import load_config
from mathbench.replay import replay
from tasks.t005.check import validate


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def audit(solution):
    c = [tuple(Fraction(x[k]) for k in ('x', 'y', 'r')) for x in solution['circles']]
    assert len(c) == 26
    walls = [s for x, y, r in c for s in (x-r, y-r, 1-x-r, 1-y-r)]
    pairs = [(x-a)**2+(y-b)**2-(r+t)**2
             for i, (x, y, r) in enumerate(c) for a, b, t in c[:i]]
    assert all(r > 0 for x, y, r in c)
    assert min(walls) >= 0 and min(pairs) >= 0
    return {'objective': str(sum((r for x, y, r in c), Fraction())),
            'wall_checks': len(walls), 'pair_checks': len(pairs),
            'minimum_wall_slack': str(min(walls)),
            'minimum_squared_pair_slack': str(min(pairs))}


def main():
    base = ROOT/'reports/evolution/t005_c01_astra_large'
    dest = base/'parent_review'
    dest.mkdir(exist_ok=False)
    routes = [('contact_pivot', 'seed_101_revised'),
              ('target_homotopy', 'seed_202_revised'), ('split_merge', 'seed_303_revised')]
    old_path = ROOT/'reports/evolution/t005_c01_astra_retry/best/solution.json'
    old = json.loads(old_path.read_text())
    old_score = Fraction(audit(old)['objective'])
    config = load_config('T005', 'T005-C01')
    runs = []
    for route, seed_dir in routes:
        folder = base/route/seed_dir
        manifest = json.loads((folder/'manifest.json').read_text())
        saved = json.loads((folder/'summary.json').read_text())
        result = json.loads((folder/'candidate/result.json').read_text())
        solution = json.loads((folder/'candidate/solution.json').read_text())
        for relative, digest in manifest['source_sha256'].items():
            assert hashlib.sha256((folder/'sources'/relative).read_bytes()).hexdigest() == digest
        assert manifest['budget']['generation_seconds'] == 960
        assert manifest['controls']['MATHBENCH_SEARCH_SECONDS'] == 900
        assert result['environment']['worker_cpu'] == manifest['environment']['cpu']
        assert result['budget'] == manifest['budget']
        independent = audit(solution)
        score = Fraction(independent['objective'])
        assert saved['passed'] and result['validity'] == 1
        assert score == Fraction(saved['objective']) == Fraction(result['objective'])
        assert score >= old_score
        changed = copy.deepcopy(solution)
        changed['objective'] = '999999'
        assert Fraction(validate(changed, config, strict=True)['objective']) == score
        damaged = copy.deepcopy(solution)
        damaged['circles'][1] = dict(damaged['circles'][0])
        try:
            validate(damaged, config, strict=True)
        except ValueError:
            pass
        else:
            raise AssertionError('Damaged witness accepted')
        checked = replay('T005', folder/'candidate/solution.json', 'T005-C01',
                         strict=True, output_dir=dest/route)
        assert checked['validity'] == 1 and Fraction(checked['objective']) == score
        proposal_audit = None
        proposal = solution.get('search', {}).get('best_new_proposal')
        if proposal:
            proposal_solution = {'circles': proposal}
            proposal_audit = audit(proposal_solution)
            proposal_path = dest/route/'new_proposal.json'
            write(proposal_path, proposal_solution)
            proposal_replay = replay('T005', proposal_path, 'T005-C01', strict=True,
                                     output_dir=dest/route/'new_proposal_replay')
            assert proposal_replay['validity'] == 1
            assert Fraction(proposal_replay['objective']) == Fraction(proposal_audit['objective'])
            assert Fraction(proposal_audit['objective']) <= score
        runs.append({'route': route, 'directory': str(folder.relative_to(base)),
                     'seed': manifest['seed'], 'cpu': manifest['environment']['cpu'],
                     'generation_seconds': result['generation_time'],
                     'started_utc': manifest['started_utc'],
                     'objective': str(score), 'audit': independent,
                     'same_circles_as_previous': solution['circles'] == old['circles'],
                     'source_sha256': manifest['source_sha256']['program.py'],
                     'search': solution.get('search', {}),
                     'new_proposal_audit': proposal_audit,
                     'claimed_score_ignored': True, 'damaged_witness_rejected': True,
                     'independent_replay_passed': True})
    winner = max(runs, key=lambda x: Fraction(x['objective']))
    best = base/'best'
    best.mkdir(exist_ok=False)
    shutil.copy2(base/winner['directory']/'candidate/solution.json', best/'solution.json')
    checked = replay('T005', best/'solution.json', 'T005-C01', strict=True,
                     output_dir=best/'replay')
    assert checked['validity'] == 1
    score = Fraction(winner['objective'])
    with localcontext() as ctx:
        ctx.prec = 100
        dec = lambda x: str(Decimal(x.numerator)/Decimal(x.denominator))
        displayed = Fraction('2.635983084919')
        public = Fraction('2.6359830849176077831865694854434817303966767982744748577457711298607038493344723396767997365079')
        summary = {'review_status': 'passed_sol_review', 'all_three_exactly_verified': True,
                   'winner': winner['route'], 'objective': str(score), 'objective_decimal': dec(score),
                   'best_origin': ('previous_own_high_precision_construction'
                                   if winner['same_circles_as_previous'] else winner['route']),
                   'gain_over_previous': dec(score-old_score),
                   'packomania_displayed_value': str(displayed),
                   'gap_below_packomania_display': dec(displayed-score),
                   'gap_below_reported_public_strict_value': dec(public-score),
                   'exceeds_packomania_display': score > displayed,
                   'new_public_record_established': False,
                   'optimality_proved': False,
                   'allocated_search_seconds': 2700, 'generation_limit_seconds_per_run': 960,
                   'sum_measured_generation_wall_seconds': sum(r['generation_seconds'] for r in runs),
                   'runs': runs,
                   'scope': 'Warm-start follow-up. Previous own witness is retained if no proposal improves it. Not a cold-start or equal-budget model comparison.'}
    summary['interrupted_attempts'] = [
        {'directory': str(f.parent.relative_to(base)), **json.loads(f.read_text())}
        for f in sorted(base.glob('*/*/interrupted.json'))]
    write(base/'summary.json', summary)
    shutil.copy2(Path(__file__), dest/'summarize_t005_astra_large.py')
    write(dest/'review.json', {'status': 'passed_sol_review',
                              'all_source_hashes_checked': True,
                              'all_exact_scores_independently_recomputed': True,
                              'all_runs_and_winner_replayed': True,
                              'invalid_witness_and_false_claim_checks_passed': True})
    rows = '\n'.join(
        f"| {r['route']} | {r['seed']} | {r['generation_seconds']:.3f} | "
        f"{r['same_circles_as_previous']} |" for r in runs)
    commands = '\n'.join(
        '.venv/bin/python scripts/run_t005_experiment.py '
        f"--program reports/evolution/t005_c01_astra_large/{r['route']}/program.py "
        f"--output reports/evolution/t005_c01_astra_large/reproduce_{r['route']} "
        f"--seed {r['seed']} --cpu {r['cpu']} --search-seconds 900 --generation-seconds 960"
        for r in runs)
    (base/'README.md').write_text(f'''# T005-C01 larger-budget Astra search

Status: passed Sol review.

The best exactly verified radius sum is **{summary['objective_decimal']}**.
Gain over the previous verified construction: **{summary['gain_over_previous']}**.
Best origin: `{summary['best_origin']}`.
Exceeds the Packomania displayed value: **{summary['exceeds_packomania_display']}**.
No new public record or optimality proof is established.

## Search methods

Three Astra agents used different search methods on separate CPU cores.

- Contact pivot: release one to four contacts, follow a nullspace motion,
  project the other contacts back to equality, and optimize the new packing.
- Target homotopy: use an augmented Lagrangian to reduce overlap while fixing
  a radius sum above the record. Use cooperative cluster changes and new starts.
- Split and merge: search packings of 24 to 28 circles. Merge nearby circles
  or split a circle, optimize, and return to the required 26 circles.

Each program keeps the previous exact rational witness if it finds no better
verified proposal. These are follow-up searches from our own saved construction.
Public, human, and reference coordinates were excluded from the search inputs.
This is separate from a model comparison that starts from the simple program.

## Budget and final performance

Each formal run had 900 seconds of search, a 960-second generation limit,
60 seconds for verification, 4 GiB memory, and one CPU thread.
The allocated search time was 2700 seconds across three cores.
The previous exploratory limit was 240 seconds per run.
The sum of measured generation wall times was
{summary['sum_measured_generation_wall_seconds']:.3f} seconds.
This sum is not elapsed campaign time or a direct CPU-time measurement.

| Method | Seed | Generation wall seconds | Retained previous circles |
| --- | ---: | ---: | --- |
{rows}

All three saved outputs passed exact verification. A retained witness is not a
new discovery. The full search counters and numerical diagnostics are in
[summary.json](summary.json). Numerical proposal scores do not enter the ranking.
Initial interrupted attempts and their measured costs are also recorded there.
They were stopped to improve candidate screening and output precision.
Development checks and interrupted work are additional to the formal budget.

## Public comparison

The [Packomania table](https://www.packomania.com/csqv/csqv.html), checked on
5 November 2026, lists 2.635983084919 for 26 circles.
Our verified value is lower by {summary['gap_below_packomania_display']}.
[Gother Labs](https://www.gotherlabs.com/results/circle-packing-26-unit-square/)
reports a strict finite-decimal value of 2.6359830849176077831865694854434817303966767982744748577457711298607038493344723396767997365079.
Our value is lower than that reported value by
{summary['gap_below_reported_public_strict_value']}.
That public coordinate witness was not downloaded or independently checked in
this campaign. Agreement of scores does not prove equal geometry or optimality.
See [public source notes](public_comparison.json).

## Exact verification and saved files

The parent reviewer independently checked all 104 wall inequalities, all 325
circle-pair inequalities, positive radii, and the rational sum for every output.
Each saved witness was replayed through the benchmark in a separate process.
A duplicate-circle witness was rejected. A false declared objective was ignored.
Source hashes, actual worker CPUs, and configured limits were checked.
These checks prove feasibility and attained scores. They give no global bound.

- [Best construction](best/solution.json)
- [Best replay](best/replay/verification.json)
- [Independent review](parent_review/review.json)
- [Resource samples](resource_samples.json)
- Per-run sources, manifests, verification, and replay in each method directory.

## Reproduce

Run from the repository root. Use new output directories.

```sh
{commands}
.venv/bin/python -m mathbench replay T005 reports/evolution/t005_c01_astra_large/best/solution.json --config T005-C01
```

Time-limited search can follow a different path on another machine.
The saved rational construction can be checked without repeating the search.
''')
    print(json.dumps({k: v for k, v in summary.items() if k != 'runs'}, indent=2))


if __name__ == '__main__':
    main()
