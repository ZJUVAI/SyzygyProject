"""Export accepted benchmark evidence to a deterministic static website snapshot."""
from __future__ import annotations
import csv
import hashlib
import io
import json
import math
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'website' / 'dist' / 'data'
CATALOG = {
'T001': ('Equal circles in a square', '等圆装入正方形', 'Pack n equal, disjoint circles inside the unit square. Maximize their common radius.', '在单位正方形内放置 n 个等圆。圆的内部不能相交。最大化公共半径。', 'Common radius', '公共半径'),
'T002': ('Unit squares in a square', '单位正方形装填', 'Place n unit squares, with rotations allowed. Minimize the side of their enclosing square.', '放置 n 个单位正方形，允许旋转。最小化外接正方形的边长。', 'Enclosing side', '外接边长'),
'T005': ('Unequal-circle packing', '变半径圆装填', 'Pack n circles in the unit square. Radii may differ. Maximize the sum of radii.', '在单位正方形内放置 n 个圆。半径可以不同。最大化半径之和。', 'Sum of radii', '半径之和'),
'T009': ('Tammes sphere packing', 'Tammes 球面码', 'Place n distinct directions on the unit sphere. Maximize the smallest pairwise angle, measured in radians.', '在单位球面上放置 n 个不同方向。最大化最小两点夹角，单位为弧度。', 'Minimum angle (rad)', '最小夹角（弧度）'),
'T014': ('Heilbronn triangles', 'Heilbronn 三角形', 'Place n distinct points in the unit square. Maximize the smallest triangle area over every triple.', '在单位正方形内放置 n 个不同的点。最大化所有三点三角形中的最小面积。', 'Minimum triangle area', '最小三角形面积'),
'T035': ('Smallest cage graph', '最小笼图', 'Construct a connected simple 4-regular graph with girth at least 10. Minimize its vertex count.', '构造连通的简单 4 正则图。最短环长度至少为 10。最小化顶点数。', 'Vertices', '顶点数'),
'T044': ('Golomb rulers', 'Golomb 尺', 'Choose integer marks with distinct positive pairwise differences. Minimize the span of the ruler.', '选择整数刻度。所有正的两两差必须不同。最小化刻度跨度。', 'Ruler length', '尺长'),
'T060': ('Covering designs', '覆盖设计', 'Cover every 4-subset of 24 points with 14-element blocks. Minimize the number of blocks.', '用 14 元素块覆盖 24 个点的每个 4 元素子集。最小化块数。', 'Blocks', '块数'),
'T066': ('Binary linear codes', '二元线性码', 'Construct a binary linear code of length 68 and dimension 15. Maximize its minimum Hamming distance.', '构造长度 68、维数 15 的二元线性码。最大化最小汉明距离。', 'Minimum distance', '最小距离'),
'T067': ('Binary code size', '二元码规模', 'Construct distinct 17-bit words with pairwise Hamming distance at least 6. Maximize their count.', '构造不同的 17 位码字。两两汉明距离至少为 6。最大化码字数。', 'Codewords', '码字数'),
'N001': ('Independent sets in C₇⁵', 'C₇ 强积独立集', 'Choose words of length 5 over 0,…,6. Every pair must have a coordinate with cyclic distance at least 2. Maximize the set size.', '选择由 0 至 6 组成的五元组。每一对元组至少有一位的循环距离不小于 2。最大化集合规模。', 'Independent-set size', '独立集规模'),
'T057': ('Sum–difference sets', '和差集合', 'Choose 2–512 distinct integers in [−10⁶,10⁶]. Maximize log(|A+A|/|A|) / log(|A−A|/|A|), with |A+A| > |A−A| > |A|.', '在 [−10⁶,10⁶] 内选择 2 至 512 个不同整数。最大化 log(|A+A|/|A|) / log(|A−A|/|A|)，且 |A+A| > |A−A| > |A|。', 'Logarithmic ratio', '对数比'),
'T073': ('Low-autocorrelation sequences', '低自相关二元序列', 'Choose L signs, each −1 or +1. Minimize the sum of squared aperiodic autocorrelations over all nonzero lags.', '选择 L 个 −1 或 +1。最小化全部非零延迟下非周期自相关的平方和。', 'Autocorrelation energy', '自相关能量'),
'T079': ('Autoconvolution · AC1', '自卷积 · AC1', 'Choose 208 nonnegative steps on [−¼,¼]. After unit-integral normalization, minimize the peak of their full autoconvolution.', '在 [−¼,¼] 上选择 208 个非负阶梯值。归一化至积分为 1 后，最小化完整自卷积的峰值。', 'Normalized peak', '归一化峰值'),
'T080': ('Autoconvolution · AC2', '自卷积 · AC2', 'Choose 20 nonnegative steps. Maximize (2Σb² + Σbᵢbᵢ₊₁) / (3 max(b)(Σa)²), where b = a∗a.', '选择 20 个非负阶梯值。令 b = a∗a，最大化 (2Σb² + Σbᵢbᵢ₊₁) / (3 max(b)(Σa)²)。', 'AC2 ratio', 'AC2 比值'),
'T081': ('Signed autoconvolution · AC3', '有符号自卷积 · AC3', 'Choose 208 steps on [−¼,¼], allowing negative values and nonzero mass. Normalize to unit integral. Minimize the absolute autoconvolution peak.', '在 [−¼,¼] 上选择 208 个阶梯值，允许负值，总质量不能为零。归一化至积分为 1。最小化自卷积的绝对峰值。', 'Absolute normalized peak', '绝对归一化峰值'),
'T082': ('Erdős minimum overlap', 'Erdős 最小重叠', 'Choose 51 steps for f on [0,2], with 0≤f≤1 and integral 1. Minimize the largest overlap of f with a shifted 1−f, over all real shifts.', '在 [0,2] 上选择 51 个阶梯值，满足 0≤f≤1 且积分为 1。最小化 f 与平移后的 1−f 在全部实数位移中的最大重叠。', 'Maximum overlap', '最大重叠'),
'T089': ('Maximum determinant', '最大行列式', 'Construct a 29×29 matrix with entries −1 or +1. Maximize the absolute value of its determinant.', '构造元素为 −1 或 +1 的 29×29 矩阵。最大化行列式的绝对值。', 'Absolute determinant', '行列式绝对值'),
'T099': ('Admissible prime tuples', '可容许素数元组', 'Choose 343 distinct integers that miss a residue class for every prime. Minimize their span. Only primes up to 343 need checking.', '选择 343 个不同整数。对每个素数，至少缺少一个余数类。最小化跨度。只需检查不超过 343 的素数。', 'Tuple diameter', '元组跨度'),
'T097': ('Shortest addition chains', '最短加法链', 'Start at 1 and reach the configured integer. Each new term is the sum of two earlier terms; repeated summands are allowed. Minimize additions.', '从 1 出发达到指定整数。每个新项是两个已有项之和，允许同一项相加。最小化加法次数。', 'Additions', '加法次数'),
}
CATEGORIES = dict(zip(['几何装填与覆盖','加法组合与离散构造','序列与平坦多项式','数论与算术构造','极值分析','极值图与超图','球面与极值点集','矩阵、格与代数极值','组合设计','编码理论'], ['Packing & covering','Additive combinatorics','Sequences','Number theory','Extremal analysis','Extremal graphs','Spherical & planar points','Matrices & algebra','Combinatorial designs','Coding theory']))


def number(x):
    if isinstance(x, (int,float)): return float(x)
    s=x.replace(' ', '').replace('sqrt(2)','sqrt2')
    if 'sqrt2' not in s: return float(Fraction(s))
    terms=re.findall(r'[+-]?[^+-]+',s)
    return sum(float(Fraction(t.replace('*sqrt2','').replace('sqrt2','') or '1'))*math.sqrt(2) if 'sqrt2' in t else float(Fraction(t)) for t in terms)


def asset(data, kind='json'):
    content = json.dumps(data,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode() if kind=='json' else data
    digest=hashlib.sha256(content).hexdigest()
    name=f'assets/{digest}.{kind}'
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)
    return 'data/'+name


def visual(tid,s,p):
    if tid=='T001': return dict(kind='packing',circles=[[number(x),number(y),number(s['radius'])] for x,y in s['centers']],bounds=[0,0,1,1])
    if tid=='T005': return dict(kind='packing',circles=[[number(c[k]) for k in ['x','y','r']] for c in s['circles']],bounds=[0,0,1,1])
    if tid=='T002':
        polygons=[]
        for q in s['squares']:
            x,y,t=[number(q[k]) for k in ['x','y','t']];c=(1-t*t)/(1+t*t);a=2*t/(1+t*t)
            polygons.append([[x+i*c/2-j*a/2,y+i*a/2+j*c/2] for i,j in [(-1,-1),(1,-1),(1,1),(-1,1)]])
        xs=[v[0] for poly in polygons for v in poly];ys=[v[1] for poly in polygons for v in poly];side=max(max(xs)-min(xs),max(ys)-min(ys))
        return dict(kind='packing',polygons=polygons,bounds=[min(xs),min(ys),side,side])
    if tid=='T009':
        points=[[number(x) for x in q] for q in s['points']];points=[[x/math.sqrt(sum(v*v for v in q)) for x in q] for q in points]
        i,j=min(((i,j) for i in range(len(points)) for j in range(i)),key=lambda ij:sum((a-b)**2 for a,b in zip(points[ij[0]],points[ij[1]])))
        return dict(kind='sphere',points=points,pair=[i,j])
    if tid=='T014':
        pts=[[number(x) for x in q] for q in s['points']]
        tri=min(((i,j,k) for i in range(len(pts)) for j in range(i) for k in range(j)),key=lambda ijk:abs((pts[ijk[1]][0]-pts[ijk[0]][0])*(pts[ijk[2]][1]-pts[ijk[0]][1])-(pts[ijk[2]][0]-pts[ijk[0]][0])*(pts[ijk[1]][1]-pts[ijk[0]][1])))
        return dict(kind='points',points=pts,triangle=tri)
    if tid=='T035': return dict(kind='graph',vertices=s['vertices'],edges=s['edges'])
    if tid=='T044':
        marks=sorted(s['marks']);return dict(kind='ruler',marks=marks,matrix=[[abs(a-b) for b in marks] for a in marks])
    if tid=='T060': return dict(kind='covering',matrix=[[int(i in b) for i in range(p['v'])] for b in s['blocks']],blocks=s['blocks'],v=p['v'],t=p['t'])
    if tid=='T066':
        rows=s['generator_matrix']; packed=[sum(b<<i for i,b in enumerate(row)) for row in rows];hist=[0]*(p['n']+1);word=0;hist[0]=1
        for i in range(1,1<<len(rows)):
            word^=packed[(i & -i).bit_length()-1];hist[word.bit_count()]+=1
        return dict(kind='code',matrix=rows,distribution=hist,distribution_type='weight')
    if tid=='T067':
        rows=[w if isinstance(w,list) else [int(b) for b in f'{w:0{p["n"]}b}'] for w in s['codewords']];hist=[0]*(p['n']+1)
        for row in rows:hist[sum(row)]+=1
        return dict(kind='code',matrix=rows,distribution=hist,distribution_type='weight')
    if tid=='N001':
        rows=s['words'];return dict(kind='words',matrix=rows,distribution=[[sum(row[c]==v for row in rows) for v in range(p['q'])] for c in range(p['power'])])
    if tid=='T057':
        a=s['set'];return dict(kind='sets',sets=[sorted(a),sorted({x+y for x in a for y in a}),sorted({x-y for x in a for y in a})])
    if tid=='T073':
        a=s['sequence'];return dict(kind='sequence',sequence=a,correlation=[sum(a[i]*a[i+k] for i in range(len(a)-k)) for k in range(1,len(a))])
    if tid in ['T079','T080','T081']:
        a=[number(x) for x in s['coefficients']];n=len(a);scale=2*n/sum(a);profile=[x*scale for x in a]
        conv=[sum(a[i]*a[k-i] for i in range(max(0,k-n+1),min(k,n-1)+1))*scale*scale/(2*n) for k in range(2*n-1)]
        # Zero at support boundaries; linear interpolation between bin-sum knots.
        return dict(kind='function',profile=profile,domain=[-.25,.25],curve=[0]+conv+[0],curve_domain=[-.5,.5],curve_type='autoconvolution')
    if tid=='T082':
        a=[number(x) for x in s['heights']];n=len(a);curve=[sum(a[i]*(1-a[i+k]) for i in range(max(0,-k),min(n,n-k)))*2/n for k in range(-n,n+1)]
        return dict(kind='function',profile=a,domain=[0,2],curve=curve,curve_domain=[-2,2],curve_type='overlap')
    if tid=='T089':return dict(kind='matrix',matrix=s['matrix'])
    if tid=='T099':
        a=sorted(s['tuple']);span=a[-1]-a[0];primes=[i for i in range(2,344) if all(i%d for d in range(2,math.isqrt(i)+1))]
        return dict(kind='tuple',positions=[float(Fraction(x-a[0],span)) for x in a],exact=[str(x) for x in a],gap_bits=[(a[i+1]-a[i]).bit_length() for i in range(len(a)-1)],residues={str(p):[sum(x%p==r for x in a) for r in range(p)] for p in primes})
    if tid=='T097':
        a=s['chain'];previous={};deps=[]
        for i,x in enumerate(a):
            pair=next(([j,previous[x-y]] for j,y in enumerate(a[:i]) if x-y in previous),[])
            deps.append(pair);previous[x]=i
        return dict(kind='chain',bits=[x.bit_length() for x in a],exact=[str(x) for x in a],dependencies=deps)
    raise ValueError(tid)


def safe_integers(value):
    if type(value) is int and abs(value)>2**53-1: return str(value)
    if isinstance(value,list): return [safe_integers(x) for x in value]
    if isinstance(value,dict): return {k:safe_integers(v) for k,v in value.items()}
    return value


def export():
    report=json.loads((ROOT/'reports/acceptance.json').read_text());OUT.mkdir(parents=True,exist_ok=True)
    sota_path=ROOT/'reports/sota_acceptance.json'
    sota_report=json.loads(sota_path.read_text()) if sota_path.exists() else {'configurations':{}}
    own_path=ROOT/'reports/own_results.json'
    own_report=json.loads(own_path.read_text()) if own_path.exists() else {'configurations':{}}
    index={'version':report['version'],'date':report['date'],'counts':{'tasks':report['task_count'],'configurations':report['configuration_count'],'runs':report['strict_program_runs'],'categories':report['category_count']},'tasks':[],'limitations':report['limitations'],'full_llm_experiments':False}
    if sota_report.get('date'):
        index['historical_acceptance_date']=report['date']
        index['date']=sota_report['date']
    rows=[]
    if own_report.get('date'):
        index['date']=max(index['date'],own_report['date'])
    index['own_result_count']=len(own_report['configurations'])
    for t in report['tasks']:
        tid=t['task_id'];folder=ROOT/'tasks'/tid.lower();records=json.loads((folder/'records.json').read_text());en,zh,de,dz,me,mz=CATALOG[tid]
        summary=dict(id=tid,name={'en':en,'zh':zh},description={'en':de,'zh':dz},metric={'en':me,'zh':mz},category={'en':CATEGORIES[t['category']],'zh':t['category']},configurations=[])
        for c in t['configurations']:
            cid=c['id'];cr=records.get('configuration_records',{}).get(cid,records)
            payload=dict(id=cid,task_id=tid,parameters=c['parameters'],direction=c['direction'],human_reference=str(c['human_reference']),records=cr,runs=[],instruction=(folder/'instruction.txt').read_text(),task_readme=(folder/'README.md').read_text())
            for r in [r for r in t['runs'] if r['config_id']==cid]:
                assert r['validity']==1 and r['strict']
                w=ROOT/'reports/witnesses'/tid/cid/r['program']/'solution.json';s=json.loads(w.read_text());v=visual(tid,s,c['parameters'])
                run={k:r[k] for k in ['program','objective','combined_score','verification_status','generation_time','verification_time','seed','budget','environment','details']}
                run['objective']=str(r['objective'])
                try: run['objective_approx']=float(Fraction(run['objective']))
                except ValueError:
                    import sympy
                    run['objective_approx']=float(sympy.sympify(run['objective'],locals={'sqrt2':sympy.sqrt(2)}).evalf())
                run['witness']=asset(w.read_bytes(),'jsonraw');run['visual']=asset(v);run['result']=asset(r)
                payload['runs'].append(run)
                rows.append(dict(task_id=tid,configuration=cid,program=r['program'],direction=c['direction'],objective=str(r['objective']),score=r['combined_score'],verification=r['verification_status']))
            path=f'data/configurations/{cid}.json';out=OUT/'configurations'/f'{cid}.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(safe_integers(payload),ensure_ascii=False,indent=2)+'\n')
            human=next(r for r in payload['runs'] if r['program']=='human')
            evidence=sota_report['configurations'].get(cid,{})
            sota=dict(status=evidence.get('status','pending_source_review'),record=evidence.get('record',{}),run=None)
            if sota['record'].get('public_value') is not None:
                try: sota['public_value_approx']=number(str(sota['record']['public_value']))
                except (ValueError, TypeError): sota['public_value_approx']=evidence.get('public_value_approx',sota['record'].get('public_value_approx'))
            if sota['status'] in ('reproduced','conservative_reproduction','best_reproducible'):
                r=evidence['run'];w=ROOT/evidence['witness'];s=json.loads(w.read_text())
                assert r['validity']==1 and r['strict'] and r['verification_status'] in ('exact','certified')
                sota['run']=dict(program='sota',objective=str(r['objective']),objective_approx=number(str(r.get('objective_value',r['objective']))),verification_status=r['verification_status'],witness=asset(w.read_bytes(),'jsonraw'),visual=asset(visual(tid,s,c['parameters'])),result=asset(r))
                if sota['status']=='conservative_reproduction':
                    try: gap=str(Fraction(sota['run']['objective'])-Fraction(sota['record']['public_value']))
                    except (ValueError, TypeError): gap=evidence.get('replay_minus_public')
                    if gap is not None:
                        sota['replay_minus_public']=gap
                        sota['gap_approx']=float(Fraction(gap))
            payload['sota']=sota
            own=own_report['configurations'].get(cid)
            payload['own']=None
            if own:
                r=own['run'];w=ROOT/own['witness']
                assert own['status']=='accepted_by_sol' and r['validity']==1 and r['strict']
                assert r['verification_status'] in ('exact','certified')
                assert hashlib.sha256(w.read_bytes()).hexdigest()==own['witness_sha256']
                assert r['objective']==own['replay']['objective']==own['independent_audit']['objective']
                payload['own']=dict(program='own',objective=str(r['objective']),objective_approx=number(str(r['objective'])),verification_status=r['verification_status'],witness=asset(w.read_bytes(),'jsonraw'),visual=asset(visual(tid,json.loads(w.read_text()),c['parameters'])),result=asset(r),evidence=asset(own))
            out.write_text(json.dumps(safe_integers(payload),ensure_ascii=False,indent=2)+'\n')
            summary['configurations'].append(dict(id=cid,parameters=c['parameters'],direction=c['direction'],asset=path,human_visual=human['visual'],gallery_visual=(sota['run'] or human)['visual'],sota=sota,own=payload['own'],runs=[{k:r[k] for k in ['program','objective','objective_approx','combined_score','verification_status']} for r in payload['runs']]))
        index['tasks'].append(summary)
    (OUT/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
    (OUT/'acceptance.json').write_bytes((ROOT/'reports/acceptance.json').read_bytes())
    if sota_path.exists(): (OUT/'sota_acceptance.json').write_bytes(sota_path.read_bytes())
    if own_path.exists(): (OUT/'own_results.json').write_bytes(own_path.read_bytes())
    s=io.StringIO();writer=csv.DictWriter(s,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows);(OUT/'results.csv').write_text(s.getvalue())
    manifest={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    assert len(index['tasks'])==20 and sum(len(t['configurations']) for t in index['tasks'])==35 and len(rows)==140
    print(f'Exported 20 tasks, 35 configurations, 140 runs; {len(manifest)} evidence files.')

if __name__=='__main__':export()
