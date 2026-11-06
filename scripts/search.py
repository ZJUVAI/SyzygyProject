"""Archive sequential exploratory searches without changing historical acceptance."""
import argparse, copy, hashlib, importlib, json, os, platform, sys, multiprocessing
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mathbench.evaluate import evaluate_candidate
from mathbench.registry import load_task
from mathbench.replay import replay
from scripts.independent_audit import independent_quantity, broken

def save(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,default=str)+'\n')

def audit_child(conn,task,solution,config):
    try: conn.send(independent_quantity(task,solution,config))
    except Exception as exc: conn.send({'error':repr(exc)})
    finally: conn.close()

def bounded_audit(task,solution,config):
    parent,child=multiprocessing.Pipe(False)
    process=multiprocessing.Process(target=audit_child,args=(child,task,solution,config));process.start();child.close()
    if parent.poll(60): result=parent.recv()
    else: result={'error':'Independent audit exceeded 60 seconds; review pending'}
    if process.is_alive():process.terminate()
    process.join();parent.close();return result

def run():
    ap=argparse.ArgumentParser();ap.add_argument('task');ap.add_argument('--label',default='');args=ap.parse_args();task=args.task.upper()
    dest=ROOT/'tasks'/task.lower()/'runs'/('search'+args.label);dest.mkdir(parents=True,exist_ok=False)
    src=ROOT/'tasks'/task.lower(); program=src/'evolution.py'
    controls={'MATHBENCH_SEARCH_SECONDS':'45','MATHBENCH_EVOLUTION_SECONDS':'45'};os.environ.update(controls)
    hashes={}
    for p in src.rglob('*.py'):
        if '__pycache__' not in str(p):
            relative=p.relative_to(ROOT);target=dest/'sources'/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());hashes[str(relative)]=hashlib.sha256(p.read_bytes()).hexdigest()
    save(dest/'manifest.json',{'task_id':task,'started_utc':datetime.now(timezone.utc).isoformat(),'scope':'AI-assisted exploratory construction search from task seeds. This is not an isolated model benchmark. No record claim.','development_exposure':('Luna reported accidentally displaying human.py during development; no witness use reported. Exclude from isolated cold-start model comparisons.' if task=='T057' else 'Task-specific Luna instructed not to read human, reference, or SOTA witnesses; filesystem access was not security-isolated.'),'controls':controls,'iteration_count':None,'iteration_note':'Where emitted, actual search counts are in solution metadata. Other programs use time cutoffs and do not expose iteration counts; exact replay uses the saved witness.','generation_seconds':300,'verification_seconds':60,'threads':1,'memory_bytes':4*1024**3,'memory_limit_enforced':sys.platform!='darwin','source_sha256':hashes,'python':sys.version,'platform':platform.platform(),'command':f'.venv/bin/python scripts/search.py run {task}','note':'Destination must be new for rerun. Time cutoffs depend on machine. Source snapshots include comparison programs; search does not load them. Local runner is not a security sandbox.'})
    rows=[]
    check=importlib.import_module(f'tasks.{task.lower()}.check')
    for config in load_task(task)['configurations']:
        cid=config['id'];cd=dest/cid;results={}
        for name,file,seed in [('initial','init_program.py',0),('baseline','baseline.py',0),('human','human.py',0),('search_seed0','evolution.py',0),('search_seed1','evolution.py',1)]:
            p=(dest/'sources'/'tasks'/task.lower()/file) if file=='evolution.py' else src/file
            result=evaluate_candidate(task,p,cid,strict=True,seed=seed,output_dir=cd/name)
            save(cd/name/'result.json',result);results[name]=result
            print(task,cid,name,result.get('objective'),result.get('error',''),flush=True)
        candidates=[k for k in ('search_seed0','search_seed1') if results[k]['validity']==1]
        row={'config_id':cid,'direction':config['direction'],'results':results,'status':'failed_search'}
        if candidates:
            from fractions import Fraction
            best=min(candidates,key=lambda k:Fraction(str(results[k].get('objective_value',results[k]['objective'])))) if config['direction']=='minimize' else max(candidates,key=lambda k:Fraction(str(results[k].get('objective_value',results[k]['objective']))))
            solution=json.loads((cd/best/'solution.json').read_text())
            rp=replay(task,cd/best/'solution.json',cid,strict=True,output_dir=cd/'replay');save(cd/'replay/result.json',rp)
            raw=check.validate(solution,config,strict=True)
            modified=copy.deepcopy(solution);modified.update(objective='999999999',score='999999999',claimed_score='999999999')
            tamper=check.validate(modified,config,strict=True)['objective']==raw['objective']
            try: check.validate(broken(task,solution),config,strict=True)
            except (ValueError,TypeError,KeyError,AssertionError): rejected=True
            else: rejected=False
            try: independent=bounded_audit(task,solution,dict(config,id='search-check'))
            except Exception as exc: independent={'error':repr(exc)}
            row.update(best=best,search_metadata={k:solution[k] for k in ('search','_evolution','search_iterations','search_method') if k in solution},replay_command=f'.venv/bin/python -m mathbench replay {task} {cd/best/"solution.json"} --config {cid}',replay=rp,claimed_score_ignored=tamper,malformed_rejected=rejected,independent_quantity=independent,status='checks_passed_pending_review' if rp['validity']==1 and tamper and rejected and 'error' not in independent else 'pending_review')
        rows.append(row);save(dest/'summary.json',{'task_id':task,'configurations':rows})
    print('DONE',task,flush=True)



def summary():
    """Summarize saved exploratory searches with frozen public comparisons."""
    import json
    from fractions import Fraction
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[1];base=ROOT
    public={cid:record.get('verification',{}) for path in (ROOT/'tasks').glob('*/sota.json') for cid,record in json.loads(path.read_text())['configurations'].items()}
    def number(r):
        try:return float(Fraction(str(r.get('objective_value',r.get('objective')))))
        except (ValueError,TypeError,ZeroDivisionError):return None
    rows=[]
    for p in sorted(base.glob('tasks/*/runs/*/summary.json')):
        for row in json.loads(p.read_text())['configurations']:
            cid=row['config_id'];results=row['results'];key=row.get('best');best=results.get(key,{})
            baseline=results.get('baseline',{});reference=public.get(cid,{}).get('run',{})
            b,x,r=map(number,(baseline,best,reference))
            improved=(x<b if row['direction']=='minimize' else x>b) if b is not None and x is not None else None
            rows.append({'config_id':cid,'direction':row['direction'],'task_id':cid.split('-')[0],'status':row['status'],'baseline':b,'best':x,'raw_objective':best.get('objective'),'improved_baseline':improved,'frozen_verified_reference':r,'reference_date':'2026-11-05','summary':str(p.relative_to(ROOT))})
    for path in (ROOT/'tasks').glob('*/best/*/result.json'):
        best=json.loads(path.read_text());cid=path.parent.name;tid=path.parents[2].name.upper()
        config=next(c for c in load_task(tid)['configurations'] if c['id']==cid)
        provenance=json.loads((path.parent/'provenance.json').read_text())
        numeric=best.get('objective_value',best.get('objective'))
        rows.append({'config_id':cid,'direction':config['direction'],'task_id':tid,
                     'status':provenance['status'],'baseline':None,
                     'best':float(Fraction(str(numeric))), 'raw_objective':best['objective'],
                     'improved_baseline':None,
                     'frozen_verified_reference':number(public.get(cid,{}).get('run',{})),
                     'reference_date':'2026-11-05','summary':str(path.relative_to(ROOT))})
    selected={}
    for row in rows:
        old=selected.get(row['config_id'])
        if old is None or (row['best'] is not None and (old['best'] is None or (row['best']<old['best'] if row['direction']=='minimize' else row['best']>old['best']))): selected[row['config_id']]=row
    rows=sorted(selected.values(),key=lambda r:r['config_id'])
    report={'scope':'Saved constructions and exploratory searches; not an isolated model comparison. No public record claim or aggregate score.','task_count':len({r['task_id'] for r in rows}),'configuration_count':len(rows),'configurations':rows}
    print(json.dumps(report,ensure_ascii=False,indent=2))



def audit():
    """Cross-check archived search scores, independent quantities, and hashes."""
    import hashlib,json,sys
    from fractions import Fraction as F
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[1];base=ROOT
    keys={'T001':'radius','T014':'minimum_triangle_area','T035':'order','T044':'span','T060':'blocks','T066':'minimum_distance','T067':'codewords','N001':'independent_words','T073':'energy','T079':'exact_objective','T080':'exact_objective','T081':'exact_objective','T082':'maximum_overlap','T089':'absolute_determinant','T099':'diameter','T097':'additions'}
    results=[]
    for p in sorted(base.glob('tasks/*/runs/*/summary.json')):
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
    for path in (ROOT/'tasks').glob('*/best/*/result.json'):
        expected=json.loads(path.read_text());cid=path.parent.name;task=path.parents[2].name.upper()
        checked=replay(task,path.parent/'solution.json',cid,strict=True)
        passed=checked['validity']==1 and checked['objective']==expected['objective']
        results.append({'attempt':str(path.parent.relative_to(ROOT)), 'config_id':cid,
                        'passed':passed,'errors':[] if passed else ['Saved best failed exact replay']})
    report={'checks':results,'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'note':'Failed setup attempts are preserved. Main report selects corrected runs. Numeric independent checks for T009 and T057 support the exact or interval checker; they do not replace its certificate.'}
    # Checks are printed; task-local run artifacts contain the evidence.
    print('Audit',report['passed'],'passed;',report['failed'],'failed attempt/configuration checks')
    for r in results:
        if not r['passed']:print(r['attempt'],r['config_id'],r['errors'])


def resume():
    """Resume task searches sequentially; preserve every existing attempt."""
    import json, subprocess, sys
    from datetime import datetime, timezone
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(ROOT))
    from mathbench.registry import load_task
    ORDER='T073 T080 T089 T014 T079 T081 T082 T001 T009 T002 T044 T060 T066 T067 N001 T057 T099 T097 T035'.split()
    base=ROOT
    for task in ORDER:
        expected={c['id'] for c in load_task(task)['configurations']}
        completed=set()
        for path in (ROOT/'tasks'/task.lower()/'runs').glob('*/summary.json'):
            data=json.loads(path.read_text())
            completed.update(r['config_id'] for r in data['configurations'] if r.get('status') in ('reviewed_by_sol','checks_passed_pending_review'))
        if expected<=completed:
            print(task,'checks already completed; skip',flush=True);continue
        label='_resume_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        print(task,'running all configurations in a new attempt',flush=True)
        subprocess.run([sys.executable,str(ROOT/'scripts/search.py'),'run',task,'--label',label],cwd=ROOT,check=True)
        subprocess.run([sys.executable,str(ROOT/'scripts/search.py'),'summary'],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/search.py'),'audit'],cwd=ROOT,check=True)


if __name__ == '__main__':
    commands = {'run': run, 'resume': resume, 'summary': summary, 'audit': audit}
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        raise SystemExit('Usage: python scripts/search.py {run TASK|resume|summary|audit}')
    command = sys.argv.pop(1)
    commands[command]()
