"""Recheck the saved T005 improvement and update the local result database."""
from copy import deepcopy
from datetime import date
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.registry import load_config
from mathbench.replay import replay
from scripts.run_t005_evolution import independent_audit
from tasks.t005.check import validate


def main():
    folder = ROOT / 'reports/evolution/t005_c01_astra_retry'
    witness = folder / 'best/solution.json'
    solution = json.loads(witness.read_text())
    config = load_config('T005', 'T005-C01')
    audit = independent_audit(solution)
    altered = deepcopy(solution)
    altered['objective'] = '999999'
    assert validate(altered, config, strict=True)['objective'] == audit['objective']
    broken = deepcopy(solution)
    broken['circles'][1] = deepcopy(broken['circles'][0])
    try:
        validate(broken, config, strict=True)
    except ValueError:
        pass
    else:
        raise ValueError('Damaged witness accepted')
    review = ROOT / 'reports/evolution/t005_c01_website_review'
    result = replay('T005', witness, 'T005-C01', strict=True, output_dir=review)
    assert result['validity'] == 1 and result['objective'] == audit['objective']
    original = json.loads((folder / 'refine/candidate/result.json').read_text())
    assert original['objective'] == result['objective']
    manifest = json.loads((folder / 'refine/manifest.json').read_text())
    for name, digest in manifest['source_sha256'].items():
        assert hashlib.sha256((folder / 'refine/sources' / name).read_bytes()).hexdigest() == digest
    public = '2.6359830849176077831865694854434817303966767982744748577457711298607038493344723396767997365079'
    objective = Fraction(result['objective'])
    record = {
        'task_id': 'T005', 'status': 'accepted_by_sol',
        'classification': 'ai_assisted_local_search',
        'method': 'Own topology search followed by high-precision contact refinement and exact rational repair',
        'scope': 'Warm-start follow-up; separate from cold-start and equal-budget model comparisons.',
        'witness': str(witness.relative_to(ROOT)),
        'witness_sha256': hashlib.sha256(witness.read_bytes()).hexdigest(),
        'program': str((folder / 'best/program.py').relative_to(ROOT)),
        'manifest': str((folder / 'refine/manifest.json').relative_to(ROOT)),
        'run': original, 'replay': result, 'independent_audit': audit,
        'damaged_witness_rejected': True, 'claimed_score_ignored': True,
        'comparison': {
            'public_source_url': 'https://www.gotherlabs.com/results/circle-packing-26-unit-square/',
            'public_source_checked': date.today().isoformat(),
            'public_strict_reported_value': public,
            'public_strict_reported_minus_own': str(Fraction(public) - objective),
            'public_strict_witness_replayed_here': False,
            'new_public_record': False,
            'note': 'Near match to this strict public report. No global optimality or exhaustive public ranking claim.'
        }
    }
    database = {'date': date.today().isoformat(), 'reviewer': 'Sol main agent',
                'scope': 'Verified local improvements. Historical acceptance and public SOTA records remain separate.',
                'configurations': {'T005-C01': record}}
    target = ROOT / 'reports/own_results.json'
    if target.exists():
        previous = json.loads(target.read_text())
        previous['configurations'].update(database['configurations'])
        database['configurations'] = previous['configurations']
    target.write_text(json.dumps(database, indent=2) + '\n')
    print('Accepted T005-C01 local improvement; exact replay and negative checks passed.')


if __name__ == '__main__':
    main()
