"""Cross-check archived search scores, independent quantities, and hashes."""
import hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'reports/remaining_search'
keys={'T001':'radius','T014':'minimum_triangle_area','T035':'order','T044':'span','T060':'blocks','T066':'minimum_distance','T067':'codewords','N001':'independent_words','T073':'energy','T079':'exact_objective','T080':'exact_objective','T081':'exact_objective','T082':'maximum_overlap','T089':'absolute_determinant','T099':'diameter','T097':'additions'}
results=[]
for p in sorted(base.glob('*/summary.json')):
    d=json.loads(p.read_text());task=d['task_id'];folder=p.parent
    manifest=json.loads((folder/'manifest.json').read_text())
    hashes_ok=all(hashlib.sha256((folder/'sources'/name).read_bytes()).hexdigest()==value for name,value in manifest['source_sha256'].items())
    for row in d['configurations']:
        errors=[];cid=row['config_id'];best=row.get('best');r=row['results'].get(best,{})
        if not hashes_ok:errors.append('Source hash mismatch')
        if r.get('validity')!=1:errors.append('No valid search result')
        if best:
            if row.get('replay',{}).get('objective')!=r['objective']:errors.append('Replay objective mismatch')
            q=row.get('independent_quantity',{})
            try:
                if task in keys:assert F(str(q[keys[task]]))==F(str(r['objective']))
                elif task=='T057':assert abs(float(q['ratio'])-float(r['objective']))<1e-12
                elif task=='T002':
                    import sympy as sp
                    assert sp.simplify(sp.sympify(q['bounding_side'])-sp.sympify(str(r['objective']).replace('sqrt2','sqrt(2)')))==0
                elif task=='T009':
                    import mpmath as mp
                    with mp.workdps(80):
                        angle=mp.mpf(q['minimum_angle_80_digits']);lo,hi=r['details']['angle_interval']
                        assert mp.mpf(lo)-mp.mpf('1e-15')<=angle<=mp.mpf(hi)+mp.mpf('1e-15')
                else:raise ValueError('No independent objective comparison')
            except Exception as exc:errors.append('Independent objective mismatch: '+repr(exc))
            if not row.get('claimed_score_ignored'):errors.append('Claimed-score check failed')
            if not row.get('malformed_rejected'):errors.append('Damaged construction accepted')
        for name in ('initial','human','baseline'):
            if row['results'][name]['validity']!=1:errors.append(name+' failed')
        results.append({'attempt':folder.name,'config_id':cid,'passed':not errors,'errors':errors})
report={'checks':results,'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'note':'Failed setup attempts are preserved. Main report selects corrected runs. Numeric independent checks for T009 and T057 support the exact or interval checker; they do not replace its certificate.'}
(base/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
print('Audit',report['passed'],'passed;',report['failed'],'failed attempt/configuration checks')
for r in results:
    if not r['passed']:print(r['attempt'],r['config_id'],r['errors'])
