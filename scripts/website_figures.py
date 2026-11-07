"""Project verified witnesses into small, labelled drawings for the Atlas."""
from collections import Counter
from fractions import Fraction
from functools import cache
from math import cos, pi, sin, sqrt


def num(value):
    return float(Fraction(value))


def label(en, zh):
    return {'en': en, 'zh': zh}


def grid(rows, en, zh, *, categorical=False):
    return {'kind': 'heatmap', 'rows': [list(map(num, row)) for row in rows[:96]],
            'row_count': len(rows), 'categorical': categorical, 'label': label(en, zh)}


def series(values, en, zh, *, bars=False):
    values = list(map(num, values))
    if len(values) > 2048:
        step = (len(values)+399)//400
        spans = [(min(values[i:i+step]),max(values[i:i+step]))
                 for i in range(0,len(values),step)]
        return {'kind':'envelope','spans':spans,'count':len(values),'label':label(en,zh)}
    return {'kind': 'series', 'values': values, 'bars': bars, 'label': label(en, zh)}


def symbols(values, en, zh, width=48):
    counts = sorted(Counter(values).items())
    rows = [list(values[i:i+width]) for i in range(0, min(len(values), 96*width), width)]
    return grid(rows, en, zh, categorical=True) | {
        'symbol_count': len(values), 'shown': sum(map(len, rows)), 'counts': counts[:128],
    }


def layout(en, zh, **geometry):
    return {'kind': 'layout', 'label': label(en, zh), **geometry}


def graph(n, edges):
    return {'kind': 'graph', 'vertices': n, 'edges': list(edges)}


def bits(value, n):
    if isinstance(value, str):
        return [int(d) for d in value]
    if isinstance(value, list):
        return value
    return [(value >> i) & 1 for i in range(n)]


def horner(coefs, x):
    result = 0
    for c in reversed(coefs):
        result = result*x+c
    return result


def algebraic(descriptor):
    poly = [Fraction(x) for x in descriptor['minimal_polynomial']]
    lo, hi = map(Fraction, descriptor['isolating_interval'])
    if len(poly) == 2:
        root = -poly[0]/poly[1]
    else:
        sign = horner(poly, lo) > 0
        for _ in range(55):
            mid = (lo+hi)/2
            if (horner(poly, mid) > 0) == sign:
                lo = mid
            else:
                hi = mid
        root = (lo+hi)/2
    return lambda x: float(horner([Fraction(a) for a in x], root)) if isinstance(x, list) else num(x)


def sphere_point(p):
    if len(p) == 3:
        return list(p)
    x, y = p
    r = x*x+y*y
    return [2*x/(1+r), 2*y/(1+r), (1-r)/(1+r)]


def squares(rows):
    return [[[x, y], [x+s, y], [x+s, y+s], [x, y+s]] for x,y,s in rows]


@cache
def instance(task):
    if task == 57:
        from tasks.t057.instance import load_instance
        return load_instance()['coordinates']
    if task == 64:
        from tasks.t064.check import _instance
        return _instance()[1]
    if task == 69:
        from tasks.t069.check import load_points
        return load_points()
    if task == 93:
        from tasks.t093.instance import load_instance
        return load_instance()
    if task == 95:
        from tasks.t095.check import load_points
        return load_points()
    if task == 99:
        from tasks.t099.check import _shape, _oriented
        return [_oriented(_shape(), i) for i in range(8)]
    raise ValueError(task)


def project(task_id, w, params):
    t = int(task_id[1:])
    if t in (21, 40):
        points = [sphere_point(tuple(map(num,p))) for p in w.get('stereographic', w.get('points'))]
        result = {'kind': 'sphere', 'points': points}
        if t == 40:
            from scipy.spatial import ConvexHull
            facets = ConvexHull(points).simplices.tolist()
            result['edges'] = sorted({tuple(sorted((a,b))) for i,j,k in facets for a,b in ((i,j),(j,k),(k,i))})
            result['label'] = label('Orthographic projection of the convex hull','凸包的正交投影')
        return result
    if t in (22, 24):
        adj = w['adjacency']
        return graph(len(adj), ((i,j) for i,row in enumerate(adj) for j in row if i<j))
    if t in (44, 61, 100):
        return graph(w.get('n',w.get('vertices')), w['edges'])
    if t in (23, 32):
        return grid(w.get('array',w.get('matrix')), 'Binary entries · dark = 1', '二元矩阵 · 深色为 1')
    if t in (25, 37):
        return grid(w.get('points',w.get('directions')), 'Point coordinates by row', '每行表示一个点的坐标')
    if t in (26, 30, 33, 34, 55):
        values = w.get('colors',w.get('labels',w.get('assignment')))
        en,zh = {33:('Vertex partition by index','按编号显示顶点分区'),
                 55:('Boolean assignment by variable','按变量编号显示布尔赋值')}.get(t,('Colors by index','按编号显示颜色'))
        return symbols(values,en,zh)
    if t in (27, 28, 45, 88):
        return series(w.get('permutation',w.get('ordering')), 'Index at each position', '排列各位置上的编号', bars=True)
    if t == 29:
        return grid([sum((a[k] for k in ('alpha','beta','gamma')),[]) for a in w['terms']],
                    'Tensor terms · α, β, γ coefficients', '张量各项 · α、β、γ 系数')
    if t == 31:
        return symbols(list(map(int,w['word'])), 'Symbols in the superpermutation', '超排列中的符号')
    if t in (35, 36, 49, 65, 66, 73, 74, 81):
        convert = algebraic(w) if 'minimal_polynomial' in w else num
        points = [[convert(x) for x in ([p['x'],p['y']] if isinstance(p,dict) else p)] for p in w['points']]
        if t == 73:
            return {'kind':'sphere','points':[p[:3] for p in points],
                    'label':label('Projection onto three coordinates of the 4D points','四维点在前三个坐标上的投影')}
        edges = [[points[i],points[j]] for i in range(len(points)) for j in range(i)] if t==36 else []
        return layout('Planar points and edges' if edges else 'Planar point set',
                      '平面点和连边' if edges else '平面点集', points=points, segments=edges)
    if t == 38:
        return grid([sum(rows,[]) for rows in zip(*w['squares'])],
                    'Latin squares side by side', '并排显示拉丁方', categorical=True)
    if t == 39:
        return {'kind':'marks','rows':w['rows'],'label':label('Marks on each ruler','各行标尺上的刻度')}
    if t == 41:
        from tasks.t041.check import _corners, _square
        polygons = [[list(map(float,p)) for p in _corners(_square(s))] for s in w['squares']]
        return layout('Squares in the unit square','单位正方形内的正方形', polygons=polygons,
                      outline=[[0,0],[1,0],[1,1],[0,1]])
    if t in (42,47,59,62,72,76,77,80,84):
        values = w.get('elements',w.get('basis',w.get('vertices',w.get('set'))))
        lo,hi=min(values),max(values)
        bins = [0]*360
        for value in values:
            bins[int((value-lo)*359/max(hi-lo,1))]+=1
        if len(values)>360:
            return series(bins,'Set elements per equal-width bin','等宽区间中的集合元素数',bars=True)
        return {'kind':'marks','rows':[values],'label':label('Set elements on a number line','数轴上的集合元素')}
    if t in (43,52,67,68,71,91):
        rows=w.get('codewords',w.get('rows'))
        if t==43:
            return grid([sum((bits(v,7) for v in row),[]) for row in rows[:96]],
                        'Three binary basis vectors per row','每行是三个二元基向量') | {'row_count':len(rows)}
        if t==52:
            return grid(rows,'Permutation codewords','排列码字',categorical=True)
        n=params.get('length',params.get('columns'))
        return grid([bits(row,n) for row in rows[:96]],'Binary words · dark = 1','二元字 · 深色为 1') | {'row_count':len(rows)}
    if t in (46,63,89,92):
        return series(w.get('coefficients',w.get('coefficients_ascending')),
                      'Coefficients in stored order','按存储顺序显示系数',bars=True)
    if t == 48:
        n=params.get('n',params.get('inputs',params.get('input_count')))
        return {'kind':'network','comparators':w['comparators'],'inputs':n}
    if t == 50:
        flips=[(a^b).bit_length()-1 for a,b in zip(w['vertices'],w['vertices'][1:])]
        if not flips:
            return grid([bits(w["vertices"][0], params["dimension"])], "Single hypercube vertex", "单个超立方体顶点")
        return symbols(flips,'Coordinate flipped at each path step','路径每一步翻转的坐标')
    if t == 51:
        running=[];total=0
        for x in w['sequence']:
            total+=x;running.append(total)
        return series(running,'Running sum of the sequence','序列的前缀和')
    if t == 53:
        factors=w['factors']
        lo,hi=min(factors),max(factors)
        bins=[0]*360
        for x in factors:
            bins[(x-lo)*359//max(1,hi-lo)]+=1
        return series(bins,'Factor count by equal-width interval','各等宽区间中的因子数量',bars=True) | {'range':[lo,hi]}
    if t in (54,90):
        a=w['sequence'];n=len(a)
        corr=[sum(a[i]*a[(i+k)%n] for i in range(n if t==90 else n-k)) for k in range(1,n)]
        return {'kind':'sequence','sequence':a,'correlation':corr,'periodic':t==90}
    if t == 56:
        from tasks.t056.check import _topology, load_instance
        ops=load_instance()
        duration,starts,finishes,_,_=_topology(w['machine_orders'],ops)
        bars=[[machine,starts[j*len(route)+k],finishes[j*len(route)+k],j]
              for j,route in enumerate(ops) for k,(machine,_) in enumerate(route)]
        return {'kind':'schedule','bars':bars,'machines':len(w['machine_orders']),'duration':duration}
    if t == 57:
        points=instance(t)
        return layout('Vehicle routes from the depot','从仓库出发的车辆路线',
                      paths=[[points[i] for i in [1,*r,1]] for r in w['routes']],points=[points[1]])
    if t == 58:
        rows=[]
        for round_ in w['rounds']:
            row=[0]*sum(map(len,round_))
            for i,group in enumerate(round_):
                for player in group:row[player]=i
            rows.append(row)
        return grid(rows,'Group of each player in each round','每轮中各选手所在的小组',categorical=True)
    if t == 60:
        tokens=[{'1':1,'+':2,'*':3,'(':4,')':5}[x] for x in w['expression'] if x in '1+*()']
        return symbols(tokens,'Expression tokens · 1, +, ×, (, )','表达式记号 · 1、+、×、(、)')
    if t == 64:
        points=[list(map(num,p)) for p in instance(t)]
        points.extend([num(x),num(y)] for x,y in zip(w['steiner_points_x'],w['steiner_points_y']))
        return layout('Triangulation edges','三角剖分的边',segments=[[points[a],points[b]] for a,b in w['edges']])
    if t == 69:
        points=instance(t);tour=w['tour']
        step=max(1,len(tour)//4500)
        segments=[[points[tour[i]],points[tour[(i+1)%len(tour)]]] for i in range(0,len(tour),step)]
        return layout('Tour edges, evenly sampled along the tour','沿巡回路线均匀抽取的边',segments=segments)
    if t in (70,98):
        return layout('Square dissection','正方形剖分',polygons=squares(w['squares']))
    if t == 75:
        if not w['edges']:
            n=params['n']
            return layout('All vertices · no hyperedges','全部顶点 · 暂无超边',
                          points=[[cos(2*pi*i/n),sin(2*pi*i/n)] for i in range(n)])
        return grid(w['edges'],'Vertex indices in each hyperedge','各超边所含的顶点编号',categorical=True)
    if t == 78:
        return grid(w['gram'],'Gram matrix entries','格的 Gram 矩阵')
    if t == 79:
        counts=Counter(tuple(x['direction']) for x in w['lines'])
        return series([counts[d] for d in sorted(counts)],'Lines per projective direction','各射影方向的直线数',bars=True)
    if t == 82:
        return layout('Positions of the two queen armies','两色皇后的位置',groups=[w['white'],w['black']],
                      outline=[[-.5,-.5],[29.5,-.5],[29.5,29.5],[-.5,29.5]],board=30)
    if t == 83:
        from tasks.t083.check import _triangle
        polygons=[[[float(q.a)+sqrt(3)*float(q.b) for q in p] for p in _triangle(a)] for a in w['triangles']]
        side=w['side']
        length=num(side[0])+sqrt(3)*num(side[1]) if isinstance(side,list) else num(side)
        return layout('Unit triangles inside a square','正方形内的单位等边三角形',polygons=polygons,
                      outline=[[0,0],[length,0],[length,length],[0,length]])
    if t == 85:
        circles=[[*map(num,p),1] for p in w['centers']]
        return layout('Unit disks and the covered disk','单位圆盘与被覆盖圆盘',circles=circles,
                      boundary_circle=[0,0,num(w['radius'])])
    if t == 86:
        def q(x):
            return num(x[0]) if isinstance(x,list) else num(x)
        return grid([[q(x) for row in a for x in row] for a in w['matrices']],
                    'Matrix entries · one flattened matrix per row','矩阵元素 · 每行展开一个矩阵')
    if t == 87:
        return series(w['heights'],'Step-function heights','阶梯函数各段的高度',bars=True)
    if t == 93:
        data=instance(t)
        polygons=[[[x+dx,y+dy] for x,y in data['items'][i]['polygon']]
                  for i,dx,dy in zip(w['item_indices'],w['x_translations'],w['y_translations'])]
        return layout('Packed polygons inside the container','容器内的多边形装填',outline=data['container'],polygons=polygons)
    if t in (94,95):
        n=params.get('n',120)
        points=[[cos(2*pi*i/n),sin(2*pi*i/n)] for i in range(n)] if t==94 else instance(t)
        edges=[(e['i'],e['j']) if isinstance(e,dict) else e for e in w['edges']]
        return layout('Edges of the subdivision','剖分的边',segments=[[points[a],points[b]] for a,b in edges])
    if t == 96:
        rho=w['rho']
        def evaluate(theta):
            return num(rho['constant'])+sum(num(a)*cos((i+1)*theta)+num(b)*sin((i+1)*theta)
                    for i,(a,b) in enumerate(zip(rho['cos'],rho['sin'])))
        return series([evaluate(2*pi*i/359) for i in range(360)],'Curvature-radius profile over one period','一个周期内的曲率半径')
    if t == 97:
        convert=algebraic(w['algebraic_field'])
        return layout('Convex pieces of the cover','覆盖区域的凸多边形',
                      polygons=[[[convert(x),convert(y)] for x,y in p] for p in w['polygons']])
    if t == 99:
        oriented=instance(t)
        cells=[(x+p['x'],y+p['y'],i) for i,p in enumerate(w['placements'])
               for x,y in oriented[p['orientation']]]
        return {'kind':'tiling','cells':cells,'width':w['width'],'height':w['height']}
    raise ValueError(f'No construction projection for {task_id}')
