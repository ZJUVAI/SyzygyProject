"""Check every saved comparison in the 19-task search review."""
import json
import hashlib
from pathlib import Path
import sympy

ROOT = Path(__file__).resolve().parents[1]


def main():
    review = json.loads((ROOT/'reports/search_priorities.json').read_text())
    accepted = json.loads((ROOT/'reports/acceptance.json').read_text())
    public = json.loads((ROOT/'reports/sota_acceptance.json').read_text())
    for name, digest in review['source_hashes'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    expected = {t['task_id']: t for t in accepted['tasks'] if t['task_id'] != 'T005'}
    assert {t['task_id'] for t in review['tasks']} == set(expected)
    count = 0
    for task in review['tasks']:
        original = expected[task['task_id']]
        assert {c['configuration_id'] for c in task['configurations']} == {c['id'] for c in original['configurations']}
        for c in task['configurations']:
            cid = c['configuration_id']
            baseline = next(r for r in original['runs'] if r['config_id'] == cid and r['program'] == 'baseline')
            assert str(c['classical_baseline']) == str(baseline['objective']), cid
            source = public['configurations'][cid]
            assert str(c['verified_reference_objective']) == str(source['run']['objective']), cid
            assert str(c['source_public_value']) == str(source['record']['public_value']), cid
            assert c['highest_reported_value'] == source['record'].get('highest_reported', {}).get('value'), cid
            assert c['sota_status'] == source['status'], cid
            b = float(sympy.sympify(str(c['classical_baseline']), locals={'sqrt2': sympy.sqrt(2)}))
            v = float(sympy.sympify(str(c['verified_reference_objective']), locals={'sqrt2': sympy.sqrt(2)}))
            gap = (v-b)/abs(v) if c['direction'] == 'maximize' else (b-v)/abs(v)
            assert abs(gap-c['normalized_gap_to_verified_reference']) < 1e-7, cid
            count += 1
    assert len(expected) == 19 and count == 33
    print('Verified 19 tasks and 33 configurations against frozen runs and the public-result archive.')


if __name__ == '__main__':
    main()
