"""Resume task searches sequentially; preserve every existing attempt."""
import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mathbench.registry import load_task
ORDER='T073 T080 T089 T014 T079 T081 T082 T001 T009 T002 T044 T060 T066 T067 N001 T057 T099 T097 T035'.split()
base=ROOT/'reports/remaining_search'
for task in ORDER:
    expected={c['id'] for c in load_task(task)['configurations']}
    completed=set()
    for path in base.glob(task.lower()+'*/summary.json'):
        data=json.loads(path.read_text())
        completed.update(r['config_id'] for r in data['configurations'] if r.get('status')=='reviewed_by_sol')
    if expected<=completed:
        print(task,'already reviewed; skip',flush=True);continue
    label='_resume_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    print(task,'running all configurations in a new attempt',flush=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/run_remaining_search.py'),task,'--label',label],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/summarize_remaining_search.py')],cwd=ROOT,check=True)
subprocess.run([sys.executable,str(ROOT/'scripts/audit_remaining_search.py')],cwd=ROOT,check=True)
