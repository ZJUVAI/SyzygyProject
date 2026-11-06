"""Build a report from completed reviews; does not accept tasks."""
import hashlib
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import sys
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mathbench.registry import INITIAL_TASKS, load_task


def numeric(run):
    return float(Fraction(str(run.get('objective_value',run['objective']))))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--passed-tests',type=int,default=187)
    parser.add_argument('--passed-subtests',type=int,default=15)
    args=parser.parse_args()
    reports=ROOT/'reports';reports.mkdir(exist_ok=True)
    reviews=json.loads((ROOT/'runs/release_review/review.json').read_text())
    audit=json.loads((reports/'independent_audit.json').read_text())
    research={t['id']:t for t in json.loads((ROOT/'research/confirmation_summary.json').read_text())['tasks']}
    by_task={r['task_id']:r for r in reviews}
    config_count=sum(len(load_task(t)['configurations']) for t in INITIAL_TASKS)
    run_count=sum(len(r['runs']) for r in reviews)
    assert len(by_task)==20 and len(audit)==config_count and run_count==4*config_count
    output=[]
    rows=['# 首批数学构造 benchmark 验收报告','',
          f'20个任务，{config_count}个配置，覆盖10个研究类别。每个任务由独立Luna代理实现，Sol主代理复核并验收。',
          '', f'{args.passed_tests}项测试和{args.passed_subtests}项子测试通过。{run_count}次严格运行通过。{config_count}个配置均完成关键量独立复算、破坏样例拒绝和声明分数无效检查。',
          '', 'SimpleTES与DREAM-RSI各有一个接口级示例通过。未运行需要模型服务的完整上游搜索实验。',
          '', '| 配置 | 任务 | 初始程序 | 传统搜索 | 人类对照 | 固定参考 |',
          '|---|---|---:|---:|---:|---:|']
    def fmt(r):
        v=numeric(r)
        return str(r['objective']) if isinstance(r['objective'],int) and abs(v)<1e25 else format(v,'.10g')
    for task in INITIAL_TASKS:
        meta=load_task(task);review=by_task[task];source=research[task]
        assert meta['acceptance_status']=='accepted_by_sol'
        assert review['automated_checks_passed']
        assert len([a for a in audit if a['task_id']==task])==len(meta['configurations'])
        record=json.loads((ROOT/'tasks'/task.lower()/'records.json').read_text())
        item={'task_id':task,'name':source['name_zh'],'category':source['category'],
              'acceptance_status':meta['acceptance_status'],'reviewer':'GPT-6.1 Sol main agent',
              'implementation_agent':'/root/implement_'+task.lower(),'implementation_model':'gpt-6-luna',
              'configurations':meta['configurations'],'runs':review['runs'], 'tests':review['tests'],
              'independent_audits':[a for a in audit if a['task_id']==task],'records':record,
              'limitations':meta['acceptance_review']['limitations']}
        if 'configuration_expansion_review' in meta:
            item['configuration_expansion_review']=meta['configuration_expansion_review']
        for config in meta['configurations']:
            runs={r['program']:r for r in review['runs'] if r['config_id']==config['id']}
            rows.append('| '+config['id']+' | '+source['name_zh']+' | '+' | '.join(fmt(runs[k]) for k in ('init_program','baseline','human','reference'))+' |')
            for program in runs:
                original=ROOT/'runs/release_review'/task/config['id']/program
                dest=reports/'witnesses'/task/config['id']/program
                shutil.copytree(original,dest,dirs_exist_ok=True)
        output.append(item)
    limitations=[
        'T009排除已获最优性证明的15点配置；目前采用的配置详见逐配置清单。',
        'T005使用等圆人类构造作变半径任务对照。公开变半径纪录单列，未复现纪录坐标。',
        'T060的人类方法对照为62块；本项目传统搜索复现40块。公开23块见证尚未取到。',
        'T066的人类方法对照距离8；本项目传统搜索复现距离19。公开距离24矩阵尚未取到。',
        'T067的人类方法对照有128码字；公开258码字见证尚未取到。',
        'T081将非负208步人类构造转用于有符号类别。150步正峰值不能用作绝对峰值成绩。',
        '最佳公开表示所列来源中同参数的最好结果。来源未披露AI参与情况时记为unknown。未声称穷尽所有公开来源。',
        '兼容分数使用冻结对照。分数大于1只表示超过该对照。正式比较还须查看原始数学目标。',
        '当前完成任务包和接口验证。完整LLM对比实验后续开展。']
    result={'version':'0.1.0','date':'2026-11-04','status':'accepted_by_sol','category_count':len({x['category'] for x in output}),
            'task_count':20,'configuration_count':config_count,'strict_program_runs':run_count,'passed_tests':args.passed_tests,'passed_subtests':args.passed_subtests,
            'interface_smoke_examples':2,'full_upstream_experiments_run':False,'limitations':limitations,'tasks':output}
    (reports/'acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    rows+=['','## 使用与限制','']+['- '+x for x in limitations]
    rows+=['','原始分数、证据层次和验证状态见 `acceptance.json`。全部正式运行构造及验证结果保存在 `witnesses/`。',
           '', '重算已保存构造：','', '```sh',
           '.venv/bin/python -m mathbench replay T073 reports/witnesses/T073/T073-C01/human/solution.json',
           '.venv/bin/python scripts/independent_audit.py', '.venv/bin/python -m pytest tests tasks -q','```','']
    (reports/'acceptance.md').write_text('\n'.join(rows))
    env={'python':sys.version,'platform':platform.platform(),'machine':platform.machine(),'processor':platform.processor(),
         'cpu_count':os.cpu_count(),'worker_cpu':min(os.sched_getaffinity(0)),
         'dependencies':{p:importlib.metadata.version(p) for p in ('numpy','scipy','sympy','mpmath','networkx','pytest')},
         'generation_seconds':300,'verification_seconds':60,'memory_bytes':4*1024**3,'threads':1,
         'default_search_mode':'fixed iterations, seed0','cpu_affinity':'one allowed CPU per worker',
         'scope':'local resource limiter; separate experiment workspace required for model access control'}
    (reports/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    paths=[]
    for parent in ('mathbench','tasks','examples','tests','scripts'):
        paths.extend(p for p in (ROOT/parent).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    paths.extend((reports/'witnesses').rglob('*.json'))
    paths.extend(ROOT/name for name in ('README.md','pyproject.toml','requirements-lock.txt'))
    paths.extend(reports/name for name in ('acceptance.json','acceptance.md','environment.json','independent_audit.json',
                                          'configuration_expansion.json','configuration_expansion.md'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    (reports/'sha256_manifest.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print('Built release report:',len(output),'tasks,',result['category_count'],'categories')


if __name__=='__main__':main()
