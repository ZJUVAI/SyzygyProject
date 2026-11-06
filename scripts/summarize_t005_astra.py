"""Independently review the six Astra exploratory T005-C01 runs."""
import json
import hashlib
import os
from pathlib import Path
from fractions import Fraction
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mathbench.replay import replay
from scripts.run_t005_evolution import independent_audit


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def main():
    base=ROOT/'reports/evolution/t005_c01_astra_parallel'
    os.sched_setaffinity(0, {3})
    rows=[]
    labels={'lp':'固定圆心 LP', 'topology':'接触结构重插', 'penalty':'连续罚函数'}
    for route,cpu in [('lp',0),('topology',1),('penalty',2)]:
        program_hash=None
        for seed in (0,1):
            folder=base/route/f'seed_{seed}'
            manifest=json.loads((folder/'manifest.json').read_text())
            result=json.loads((folder/'candidate/result.json').read_text())
            summary=json.loads((folder/'summary.json').read_text())
            assert summary['passed'] and result['validity']==1
            assert result['strict'] and result['verification_status']=='certified'
            assert result['environment']['worker_cpu']==cpu
            assert result['budget']=={'generation_seconds':300, 'verification_seconds':60,
                                      'memory_bytes':4*1024**3, 'threads':1}
            for name,digest in manifest['source_sha256'].items():
                assert hashlib.sha256((folder/'sources'/name).read_bytes()).hexdigest()==digest
            digest=manifest['source_sha256']['program.py']
            if program_hash is None:program_hash=digest
            assert digest==program_hash
            assert hashlib.sha256((base/route/'program.py').read_bytes()).hexdigest()==digest
            solution=json.loads((folder/'candidate/solution.json').read_text())
            audit=independent_audit(solution)
            assert audit['objective']==result['objective']==summary['objective']
            assert summary['damaged_witness_rejected'] and summary['claimed_score_ignored']
            assert json.loads((folder/'replay/result.json').read_text())['objective']==result['objective']
            rows.append({'route':route,'label':labels[route],'model':'gpt-6-astra','seed':seed,
                         'objective':result['objective'],'objective_decimal':float(Fraction(result['objective'])),
                         'cpu':cpu,'started_utc':manifest['started_utc'],
                         'generation_seconds':result['generation_time'],
                         'directory':str(folder.relative_to(base)),
                         'program_sha256':digest,'audit':audit})
    winner=max(rows,key=lambda r:Fraction(r['objective']))
    best=base/'best'
    best.mkdir(exist_ok=False)
    shutil.copy2(base/winner['directory']/'candidate/solution.json', best/'solution.json')
    checked=replay('T005',best/'solution.json','T005-C01',strict=True,output_dir=best/'replay')
    assert checked['validity']==1 and checked['objective']==winner['objective']
    public=base/'public'
    public.mkdir(exist_ok=False)
    archive=ROOT/'reports/evolution/t005_c01_multiseed_v2_g1000/public'
    for name in ('table.html','coordinates.txt','solution.json','sota_archive.json'):
        shutil.copy2(archive/name,public/name)
    reference=replay('T005',public/'solution.json','T005-C01',strict=True,output_dir=public/'replay')
    assert reference['validity']==1
    previous=json.loads((ROOT/'reports/evolution/t005_c01_multiseed_v2_g1000/summary.json').read_text())
    score=Fraction(winner['objective']); old=Fraction(previous['best_objective'])
    displayed=Fraction('2.635983084919'); exact_public=Fraction(reference['objective'])
    summary={'all_six_exactly_verified':True,'runs':rows,'best':winner,
             'previous_best_objective':str(old),'improvement_over_previous':str(score-old),
             'public_displayed_value':'2.635983084919','public_conservative_objective':str(exact_public),
             'gap_to_public_displayed':str(displayed-score),
             'gap_to_public_displayed_decimal':float(displayed-score),
             'percent_below_public_displayed':float(100*(displayed-score)/displayed),
             'gap_to_conservative_public_witness':str(exact_public-score),
             'total_formal_generation_seconds':sum(r['generation_seconds'] for r in rows),
             'protocol':'Three parallel routes on CPUs0/1/2, two sequential seeds per route, soft240/hard300seconds per run.',
             'comparison_scope':'Exploratory algorithm and budget changes; not a controlled comparison between language models.',
             'reviewer':'Sol main agent','review_status':'passed_sol_review','optimality_proved':False}
    write(base/'summary.json',summary)
    write(best/'selection.json',{'selection_rule':'Maximum exact objective among six formal Astra runs; development runs excluded.',
                                'selected':winner,'solution_sha256':hashlib.sha256((best/'solution.json').read_bytes()).hexdigest()})
    table='\n'.join(f"| {r['label']} | {r['seed']} | {r['objective_decimal']:.12f} | {r['generation_seconds']:.2f} | CPU {r['cpu']} |" for r in rows)
    direction='提高' if score>old else '降低'
    report=f'''# Astra 并行搜索 T005-C01

## 结果

先由 Astra 只读检查策略，再由三个 Astra 代理并行实现和运行。
Sol 主代理复核了六次正式运行的原始构造、全部约束、分数、源码哈希和 CPU 绑定。
六次正式结果均通过原评测器、独立有理数审计、负例、篡改分数检查和重放。

本轮最佳路线为 **{winner['label']}**，种子 **{winner['seed']}**。
精确半径和为 `{winner['objective']}`，约 **{float(score):.12f}**。
相对此前最佳 **{float(old):.9f}**，{direction}了 **{abs(float(score-old)):.12f}**。
与公开表格值 **2.635983084919** 相差 **{float(displayed-score):.12f}**，
低于该值 **{float(100*(displayed-score)/displayed):.8f}%**。

| 路线 | 种子 | 半径和 | 生成实测秒数 | 绑定核 |
|---|---|---|---|---|
{table}

## Astra 建议与实际路线

[建议全文](strategy_advice.md)和[建议清单](advice.json)保存了咨询结果。

- 固定圆心 LP：重新分配半径，减少局部冲突引发的整体缩小。
- 接触结构重插：缩小局部圆簇，移走并重插圆，再抛光新的接触结构。
- 连续罚函数：允许搜索中暂时重叠，跨过旧邻居，之后恢复可行半径并抛光。

三条路线都使用生成的冷起点。程序不读人类、公开或既有搜索见证。
源码均为独立单文件。每条路线在正式两个种子之间冻结源码。
各路线的 README 记录实际实现、开发运行、正式结果及局限。

LP 路线的主循环抛光排程只覆盖部分链。这一局限已经记录。
接触签名和罚函数只用于探索；它们不作为数学证书。

## 预算与并行

每条路线运行种子 0、1，依次运行。三条路线分配 CPU 0、1、2，因此可同时搜索。
每次软预算为 240 秒，包含最终抛光。生成硬上限 300 秒。
验证另限 60 秒。每次内存上限 4 GiB，单数值线程。
六次正式生成的墙时间合计为 **{sum(r['generation_seconds'] for r in rows):.2f} 秒**。
三条路线并行执行。这个合计值不等于实际等待时间，也不等于精确 CPU 使用量。
各程序提前停止探索并预留抛光时间，故不一定用满软预算。

开发短运行保存在各路线的 `development/`，不进入正式最佳结果选择。
`runner_smoke/` 只验证归档器和 CPU 绑定，也不进入排名。

本轮使用时间预算，局部求解次数和迭代数与此前固定 1,000 代实验不同。
结果比较说明找到了哪些构造，不构成 Astra 与其他模型的公平能力比较。

## 精确验证与公开对照

量化圆心后，用整数平方根向下取整得到距离下界，再给半径分配设置保守约束。
向下舍入半径并修复局部冲突后，原评测器和独立 Fraction 实现检查：
26 个半径均为正、104 条墙约束和 325 条圆对约束。
最终半径和完全由构造重算。候选声明的分数不参与正式评分。

[Packomania 表格](https://www.packomania.com/csqv/csqv.html)的 N=26 行
在 2026-11-05 重新核对，仍显示 2.635983084919。
该值为显示小数，不代表最优性证明。公开坐标的保守有理数见证
在本轮再次通过重放，半径和为 `{reference['objective']}`。
其值略低于公开显示值，以覆盖坐标舍入误差。
本轮最佳与该精确公开见证的差为 `{exact_public-score}`。

本轮证明了构造可行和所得分数。没有提供 Lean 证明或全局最优性证明。
现有基准的冻结人类对照、正式参考和验收数量均未改变。

## 保存内容与重放

- [最佳构造](best/solution.json)
- [最佳选择与哈希](best/selection.json)
- [主代理重新运行的精确验证](best/replay/verification.json)
- [完整机器结果](summary.json)
- [LP 路线](lp/README.md)
- [接触结构路线](topology/README.md)
- [罚函数路线](penalty/README.md)

各种子目录保存源码、环境、预算、种子、见证、验证和重放结果。
各程序的实际调用数与进展记录保存在构造的 `search` 字段。
时间截断的搜索结果受机器速度影响。保存的有理数见证可独立重放：

```sh
.venv/bin/python -m mathbench replay T005 \\
  reports/evolution/t005_c01_astra_parallel/best/solution.json --config T005-C01
```
'''
    (base/'README.md').write_text(report)
    print(json.dumps(summary,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
