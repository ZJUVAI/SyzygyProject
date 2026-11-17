"""Archive sequential exploratory searches without changing historical acceptance."""
import argparse, copy, hashlib, importlib, json, os, platform, sys, multiprocessing, shlex
from datetime import datetime, timezone
from itertools import chain
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mathbench.evaluate import evaluate_candidate
from mathbench.registry import INITIAL_TASKS, load_task, resolve_task_id
from mathbench.replay import read_witness_bytes, replay
from mathbench.saved_result import best_record_path, read_best_record
from scripts.audits.independent_audit import independent_quantity, broken

def save(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,default=str)+'\n')

def source_files(src):
    """Exclude generated runs before traversal to prevent recursive snapshots."""
    for folder, directories, filenames in os.walk(src):
        directories[:] = sorted(d for d in directories if d not in ('runs', '__pycache__'))
        for name in sorted(filenames):
            if name.endswith(('.py', '.cpp', '.h', '.hpp')):
                yield Path(folder) / name

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
    ap=argparse.ArgumentParser();ap.add_argument('task');ap.add_argument('--label',default='')
    ap.add_argument('--seconds',type=float,default=45)
    ap.add_argument('--baseline-seconds',type=float,default=45)
    ap.add_argument('--seeds',type=int,nargs='+',default=[0,1])
    ap.add_argument('--config',action='append',dest='config_ids')
    ap.add_argument('--cpu',type=int)
    args=ap.parse_args()
    try:
        task = resolve_task_id(args.task)
    except ValueError as error:
        ap.error(str(error))
    if not 0 < args.seconds <= 240 or not 0 < args.baseline_seconds <= 240:
        ap.error('Search budgets must be in (0, 240] seconds; generation remains limited to 300 seconds')
    if len(set(args.seeds))!=len(args.seeds):ap.error('Seeds must be distinct')
    if args.cpu is not None:
        if not hasattr(os,'sched_getaffinity') or args.cpu not in os.sched_getaffinity(0):ap.error('Requested CPU is unavailable')
        os.sched_setaffinity(0,{args.cpu})
    configurations=load_task(task)['configurations']
    if args.config_ids:
        if not set(args.config_ids)<={c['id'] for c in configurations}:ap.error('Unknown configuration')
        configurations=[c for c in configurations if c['id'] in args.config_ids]
    dest=ROOT/'tasks'/task.lower()/'runs'/('search'+args.label);dest.mkdir(parents=True,exist_ok=False)
    src=ROOT/'tasks'/task.lower(); program=src/'evolution.py'
    controls={'MATHBENCH_SEARCH_SECONDS':str(args.baseline_seconds),'MATHBENCH_EVOLUTION_SECONDS':str(args.seconds)};os.environ.update(controls)
    hashes={}
    shared_sources = sorted((ROOT / 'mathbench').glob('*.py'))
    for path in chain(shared_sources, source_files(src)):
        relative = path.relative_to(ROOT)
        target = dest / 'sources' / relative
        contents = path.read_bytes()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)
        hashes[str(relative)] = hashlib.sha256(contents).hexdigest()
    save(dest/'manifest.json',{'task_id':task,'started_utc':datetime.now(timezone.utc).isoformat(),'scope':'AI-assisted exploratory construction search from task seeds. This is not an isolated model benchmark. No record claim.','development_exposure':('Luna reported accidentally displaying human.py during development; no witness use reported. Exclude from isolated cold-start model comparisons.' if task=='T069' else 'Search programs must not read human, reference, or SOTA witnesses; filesystem access was not security-isolated.'),'controls':controls,'iteration_count':None,'iteration_note':'Where emitted, actual search counts are in solution metadata. Other programs use time cutoffs and do not expose iteration counts; exact replay uses the saved witness.','generation_seconds':300,'verification_seconds':60,'threads':1,'memory_bytes':4*1024**3,'memory_limit_enforced':sys.platform!='darwin','source_sha256':hashes,'python':sys.version,'platform':platform.platform(),'command':f'.venv/bin/python scripts/search.py run {task}','note':'Destination must be new for rerun. Time cutoffs depend on machine. Source snapshots include comparison programs; search does not load them. Local runner is not a security sandbox.'})
    manifest_path=dest/'manifest.json';manifest=json.loads(manifest_path.read_text())
    manifest.update(scope='AI-assisted local continuation search with optional own-best warm starts; not an isolated model comparison.',command=shlex.join(['.venv/bin/python','scripts/search.py','run',*sys.argv[1:]]),seeds=args.seeds,configuration_ids=[c['id'] for c in configurations],worker_cpu=min(os.sched_getaffinity(0)) if hasattr(os,'sched_getaffinity') else None,warm_start_sha256={})
    save(manifest_path,manifest)
    rows=[]
    check=importlib.import_module(f'tasks.{task.lower()}.check')
    for config in configurations:
        cid=config['id'];cd=dest/cid;results={}
        own_best=best_record_path(src/'data');warm_start=None
        if own_best.exists():
            warm_start=cd/'warm_start.json';warm_start.parent.mkdir(parents=True,exist_ok=True);warm_start.write_bytes(read_witness_bytes(own_best))
            manifest['warm_start_sha256'][cid]=hashlib.sha256(warm_start.read_bytes()).hexdigest();save(manifest_path,manifest)
        searches=[(f'search_seed{seed}','evolution.py',seed) for seed in args.seeds]
        for name,file,seed in [('initial','init_program.py',0),('baseline','baseline.py',0),('human','human.py',0),*searches]:
            os.environ.pop('MATHBENCH_WARM_START',None)
            if file=='evolution.py' and warm_start is not None:os.environ['MATHBENCH_WARM_START']=str(warm_start)
            p=(dest/'sources'/'tasks'/task.lower()/file) if file=='evolution.py' else src/file
            result=evaluate_candidate(task,p,cid,strict=True,seed=seed,output_dir=cd/name)
            save(cd/name/'result.json',result);results[name]=result
            print(task,cid,name,result.get('objective'),result.get('error',''),flush=True)
        os.environ.pop('MATHBENCH_WARM_START',None)
        candidates=[name for name,_,_ in searches if results[name]['validity']==1]
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
            row.update(best=best,search_metadata={k:solution[k] for k in ('search','_evolution','search_iterations','search_method','search_metadata') if k in solution},replay_command=f'.venv/bin/python -m mathbench replay {task} {cd/best/"solution.json"} --config {cid}',replay=rp,claimed_score_ignored=tamper,malformed_rejected=rejected,independent_quantity=independent,status='checks_passed_pending_review' if rp['validity']==1 and tamper and rejected and 'error' not in independent and all(results[name]['validity']==1 for name in ('initial','baseline','human')) else 'pending_review')
        rows.append(row);save(dest/'summary.json',{'task_id':task,'configurations':rows})
    print('DONE',task,flush=True)



def search_summaries(root, task='*'):
    """Read summaries from this runner, alongside other task experiments."""
    for path in sorted(root.glob(f'tasks/{task}/runs/*/summary.json')):
        data = json.loads(path.read_text())
        if 'task_id' in data and isinstance(data.get('configurations'), list):
            yield path, data


def summary():
    """Summarize saved exploratory searches with frozen public comparisons."""
    import json
    from fractions import Fraction
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[1];base=ROOT
    public={cid:record.get('verification',{}) for path in (ROOT/'tasks').glob('*/data/bestknown.json') for cid,record in json.loads(path.read_text())['configurations'].items()}
    def number(r):
        try:return float(Fraction(str(r.get('objective_value',r.get('objective')))))
        except (ValueError,TypeError,ZeroDivisionError):return None
    official = {c["id"]: c for task in INITIAL_TASKS for c in load_task(task)["configurations"]}
    rows=[]
    for p, data in search_summaries(base):
        for row in data['configurations']:
            cid=row['config_id']
            if cid not in official:continue
            results=row['results'];key=row.get('best');best=results.get(key,{})
            baseline=results.get('baseline',{});reference=public.get(cid,{}).get('run',{})
            b,x,r=map(number,(baseline,best,reference))
            improved=(x<b if row['direction']=='minimize' else x>b) if b is not None and x is not None else None
            rows.append({'config_id':cid,'direction':row['direction'],'task_id':cid.split('-')[0],'status':row['status'],'baseline':b,'best':x,'raw_objective':best.get('objective'),'improved_baseline':improved,'frozen_verified_reference':r,'summary':str(p.relative_to(ROOT))})
    for directory in (ROOT/'tasks').glob('*/data'):
        path=best_record_path(directory)
        if not path.is_file(): continue
        record=read_best_record(path)
        best=record['result'];cid=best['config_id'];tid=path.parents[1].name.upper()
        if cid not in official:continue
        config=official[cid]
        provenance=record['provenance']
        numeric=best.get('objective_value',best.get('objective'))
        rows.append({'config_id':cid,'direction':config['direction'],'task_id':tid,
                     'status':provenance['status'],'baseline':None,
                     'best':float(Fraction(str(numeric))), 'raw_objective':best['objective'],
                     'improved_baseline':None,
                     'frozen_verified_reference':number(public.get(cid,{}).get('run',{})),
                     'summary':str(path.relative_to(ROOT))})
    selected={}
    for row in rows:
        old=selected.get(row['config_id'])
        if old is None or (row['best'] is not None and (old['best'] is None or (row['best']<=old['best'] if row['direction']=='minimize' else row['best']>=old['best']))): selected[row['config_id']]=row
    rows=sorted(selected.values(),key=lambda r:r['config_id'])
    report={'scope':'Saved constructions and exploratory searches; not an isolated model comparison. No public record claim or aggregate score.','task_count':len({r['task_id'] for r in rows}),'configuration_count':len(rows),'configurations':rows}
    print(json.dumps(report,ensure_ascii=False,indent=2))



def audit():
    """Cross-check archived search scores, independent quantities, and hashes."""
    import hashlib,json,sys
    from fractions import Fraction as F
    from pathlib import Path
    ROOT=Path(__file__).resolve().parents[1];base=ROOT
    keys={'T010':'tile_count','T036':'triangle_count','T009':'outer_side','T028':'face_count','T029':'polygon_count','T006':'packed_value','T055':'row_count','T075':'energy','T044':'cutwidth','T079':'minimum_autocorrelation_ratio','T007':'radius','T061':'diameter','T045':'army_size','T023':'distance_ratio','T066':'union_cardinality','T014':'determinant','T037':'edge_count','T062':'largest_element','T018':'area_ratio','T016':'point_count','T072':'max_size','T049':'code_size','T008':'square_count','T096':'tour_cost','T050':'code_size','T048':'code_size','T022':'three_point_lines','T021':'unit_pairs','T026':'steiner_count','T064':'cardinality','T035':'edge_count','T089':'one_count','T057':'round_count','T039':'clique_cardinality','T097':'route_cost','T098':'satisfied_soft_weight','T095':'makespan','T074':'peak_sidelobe','T090':'minimum_factor','T083':'sequence_length','T052':'code_size','T041':'induced_path_edges','T020':'distance_count','T099':'comparator_count','T060':'difference_basis_size','T043':'linear_arrangement_cost','T031':'order','T051':'code_size','T063':'cardinality','T004':'sum_sides','T015':'volume','T059':'scope','T056':'square_count','T019':'point_count','T025':'crossings','T013':'direction_count','T068':'prefix_length','T034':'ones','T042':'cut_weight','T100':'string_length','T038':'color_count','T094':'makespan','T086':'rank_terms','T093':'quadratic_cost','T067':'prefix_length','T065':'points','T033':'edges','T032':'vertices','T054':'rows','T001':'radius','T002':'sum_radii','T017':'minimum_triangle_area','T030':'order','T058':'span','T053':'blocks','T046':'minimum_distance','T047':'codewords','T040':'independent_words','T073':'energy','T076':'exact_objective','T078':'exact_objective','T077':'exact_objective','T080':'maximum_overlap','T085':'absolute_determinant','T087':'diameter','T088':'additions'}
    results=[]
    for p, d in search_summaries(base):
        task=d['task_id'];folder=p.parent
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
                    elif task=='T069':assert abs(float(q['ratio'])-float(r['objective']))<1e-12
                    elif task=='T003':
                        import sympy as sp
                        assert sp.simplify(sp.sympify(q['bounding_side'])-sp.sympify(str(r['objective']).replace('sqrt2','sqrt(2)')))==0
                    elif task in ('T027','T082','T081','T005','T012','T091','T092','T070','T071', 'T024', 'T084'):
                        from scripts.review_search import check_quantity
                        check_quantity(task,q,r)
                    elif task=='T011':
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
    for directory in (ROOT/'tasks').glob('*/data'):
        path=best_record_path(directory)
        if not path.is_file(): continue
        expected=read_best_record(path)['result'];cid=expected['config_id'];task=path.parents[1].name.upper()
        if task not in INITIAL_TASKS:continue
        checked=replay(task,path,cid,strict=True)
        passed=checked['validity']==1 and checked['objective']==expected['objective']
        results.append({'attempt':str(path.relative_to(ROOT)), 'config_id':cid,
                        'passed':passed,'errors':[] if passed else ['Saved best failed exact replay']})
    report={'checks':results,'passed':sum(r['passed'] for r in results),'failed':sum(not r['passed'] for r in results),'note':'Failed setup attempts are preserved. Main report selects corrected runs. Numeric independent checks for T011 and T069 support the exact or interval checker; they do not replace its certificate.'}
    # Checks are printed; task-local run artifacts contain the evidence.
    print('Audit',report['passed'],'passed;',report['failed'],'failed attempt/configuration checks')
    for r in results:
        if not r['passed']:print(r['attempt'],r['config_id'],r['errors'])


# Keep the original search priorities. The registry supplies the remaining tasks.
_RESUME_PRIORITY = 'T073 T078 T085 T017 T076 T077 T080 T001 T011 T003 T002 T058 T053 T046 T047 T040 T069 T087 T088 T030'.split()


def resume_order():
    priority = tuple(task for task in _RESUME_PRIORITY if task in INITIAL_TASKS)
    return priority + tuple(task for task in INITIAL_TASKS if task not in priority)


def resume():
    """Resume task searches sequentially; preserve every existing attempt."""
    import subprocess

    for task in resume_order():
        expected={c['id'] for c in load_task(task)['configurations']}
        completed=set()
        for _, data in search_summaries(ROOT, task.lower()):
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
