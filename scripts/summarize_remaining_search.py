"""Summarize saved exploratory searches with frozen public comparisons."""
import json
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];base=ROOT/'reports/remaining_search'
public=json.loads((ROOT/'reports/sota_acceptance.json').read_text())['configurations']
rows=[]
for p in sorted(base.glob('*/summary.json')):
    if p.parent.name in ('t073','t014','t081','t082'):continue
    for row in json.loads(p.read_text())['configurations']:
        cid=row['config_id'];results=row['results'];key=row.get('best');best=results.get(key,{})
        baseline=results.get('baseline',{});reference=public.get(cid,{}).get('run',{})
        def number(r):
            try:return float(Fraction(str(r.get('objective_value',r.get('objective')))))
            except (ValueError,TypeError,ZeroDivisionError):return None
        b,x,r=map(number,(baseline,best,reference))
        improved=(x<b if row['direction']=='minimize' else x>b) if b is not None and x is not None else None
        rows.append({'config_id':cid,'direction':row['direction'],'task_id':cid.split('-')[0],'status':row['status'],'baseline':b,'best':x,'raw_objective':best.get('objective'),'improved_baseline':improved,'frozen_verified_reference':r,'reference_date':'2026-11-05','summary':str(p.relative_to(ROOT))})
selected={}
for row in rows:
    old=selected.get(row['config_id'])
    if old is None or (row['best'] is not None and (old['best'] is None or (row['best']<old['best'] if row['direction']=='minimize' else row['best']>old['best']))): selected[row['config_id']]=row
rows=sorted(selected.values(),key=lambda r:r['config_id'])
report={'scope':'Sequential cold-start exploratory searches. No new public record claim. No cross-task aggregate score.','task_count':len({r['task_id'] for r in rows}),'configuration_count':len(rows),'configurations':rows}
(base/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Remaining task search results','','Public comparisons use the saved 2026-11-05 evidence. They are not a current public ranking. Each search has a 45-second target, a 300-second generation limit, a 60-second verification limit, 4 GiB memory, and one thread. Two seeds are run per configuration. Time-limited search depends on the machine. Exact raw values and errors are saved in each task summary. Historical acceptance is unchanged.','','| Configuration | Classical baseline | Search best | Frozen verified reference | Review |','|---|---:|---:|---:|---|']
for r in rows:
    fmt=lambda v:'—' if v is None else f'{v:.12g}'
    lines.append(f"| [{r['config_id']}]({Path(r['summary']).relative_to('reports/remaining_search')}) | {fmt(r['baseline'])} | {fmt(r['best'])} | {fmt(r['frozen_verified_reference'])} | {r['status']} |")
(base/'README.md').write_text('\n'.join(lines)+'\n')
print(report['task_count'],'tasks',len(rows),'configurations',sum(r['improved_baseline'] is True for r in rows),'improved')
