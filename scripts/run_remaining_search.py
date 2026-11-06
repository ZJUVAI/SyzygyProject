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

def main():
    ap=argparse.ArgumentParser();ap.add_argument('task');ap.add_argument('--label',default='');args=ap.parse_args();task=args.task.upper()
    dest=ROOT/'reports/remaining_search'/(task.lower()+args.label);dest.mkdir(parents=True,exist_ok=False)
    src=ROOT/'tasks'/task.lower(); program=src/'evolution.py'
    controls={'MATHBENCH_SEARCH_SECONDS':'45','MATHBENCH_EVOLUTION_SECONDS':'45'};os.environ.update(controls)
    hashes={}
    for p in src.rglob('*.py'):
        if '__pycache__' not in str(p):
            relative=p.relative_to(ROOT);target=dest/'sources'/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());hashes[str(relative)]=hashlib.sha256(p.read_bytes()).hexdigest()
    save(dest/'manifest.json',{'task_id':task,'started_utc':datetime.now(timezone.utc).isoformat(),'scope':'AI-assisted exploratory construction search from task seeds. This is not an isolated model benchmark. No record claim.','development_exposure':('Luna reported accidentally displaying human.py during development; no witness use reported. Exclude from isolated cold-start model comparisons.' if task=='T057' else 'Task-specific Luna instructed not to read human, reference, or SOTA witnesses; filesystem access was not security-isolated.'),'controls':controls,'iteration_count':None,'iteration_note':'Where emitted, actual search counts are in solution metadata. Other programs use time cutoffs and do not expose iteration counts; exact replay uses the saved witness.','generation_seconds':300,'verification_seconds':60,'threads':1,'memory_bytes':4*1024**3,'source_sha256':hashes,'python':sys.version,'platform':platform.platform(),'command':f'.venv/bin/python scripts/run_remaining_search.py {task}','note':'Destination must be new for rerun. Time cutoffs depend on machine. Source snapshots include comparison programs; search does not load them. Local runner is not a security sandbox.'})
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
            row.update(best=best,search_metadata={k:solution[k] for k in ('search','_evolution','search_iterations','search_method') if k in solution},replay_command=f'.venv/bin/python -m mathbench replay {task} {cd/best/"solution.json"} --config {cid}',replay=rp,claimed_score_ignored=tamper,malformed_rejected=rejected,independent_quantity=independent,status='reviewed_by_sol' if rp['validity']==1 and tamper and rejected and 'error' not in independent else 'pending_review')
        rows.append(row);save(dest/'summary.json',{'task_id':task,'configurations':rows})
    print('DONE',task,flush=True)
if __name__=='__main__': main()
