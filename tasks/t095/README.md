# T095: 固定 500 点集的最少凸分割

## 定义

本配置使用 CG:SHOP 2020 固定实例 uniform-0000500-1。实例含 500 个平面整数点。分割由输入点之间的直线段组成。每个输入点都是图顶点。凸包内部被若干空凸多边形覆盖，多边形内部互不相交。目标是最小化有界面数。

这里的“空”表示多边形内部不含输入点。检查器也拒绝边穿过非端点输入点。所有输入坐标从官方 JSON 以十进制精确解析为整数，不用浮点容差。

检查器核对边端点、重复边、自环、穿点、交叉、图连通性、顶点度、凸包边界、所有有界面和面积覆盖。它从平面嵌入的有向边精确遍历面。每个有界面必须是简单凸多边形且内部无输入点。有界面面积和必须与凸包面积相等。成绩是独立重算的有界面数。

## 构造与公开结果

固定公开解文件含 770 条边。精确检查得 271 个有界凸面。Euler 公式也给出 (770-500+1=271)。归档只记录时间，不写算法、求解者或 AI 贡献，因此这些来源信息标为未披露。271 是可行解，不是最优性证明。

冻结的人类方法基线采用 SoCG 2020 论文第 2.2 节记载的传统方法：先做 Delaunay 三角剖分，再随机删除仍保持凸面的边。本地版本由 AI 协助实现，使用确定性次序合并凸并集，得到 384 个面。它不是论文代码或论文成绩的逐字复现，也不是公开纪录。

Hadrien Cambazard 的项目页面称 100 点实例可解到最优，并说明模型下界可计算到 300 点。页面没有给这个 500 点实例的最优性证明。来源检查截止 2026-11-06。

## 来源与文件

- [CG:SHOP 2020 输入实例](https://cgshop.ibr.cs.tu-bs.de/static/competitions/cgshop_2020/instances_01.zip)
- [CG:SHOP 2020 最佳解归档](https://cgshop.ibr.cs.tu-bs.de/static/competitions/cgshop_2020/best_solutions.zip)
- [Eder, Held, de Lorenzo, and Palfrader, SoCG 2020](https://doi.org/10.4230/LIPIcs.SoCG.2020.85), section 2.2
- [Cambazard, Minimum convex partition problem](https://pagesperso.g-scop.grenoble-inp.fr/~cambazah/convexpartition/minconvex.html)

原始实例与 770 边解分别保存在 data/source 和 data/reference；SHA-256 与来源状态保存在 data/source/source_notes.json。

## 运行

使用 .venv/bin/python。init_program.py、baseline.py、human.py、reference.py 和 evolution.py 都提供 run_code()。默认生成预算 300 秒，验证预算 60 秒，内存 4 GiB，单线程。

# T095: Minimum convex partition of a fixed set of 500 points

## Definition

This configuration uses the fixed CG:SHOP 2020 instance uniform-0000500-1. It has 500 integer points in the plane. A partition uses straight segments between input points. Every input point is a graph vertex. Empty convex polygons cover the convex hull with pairwise disjoint interiors. The objective is to minimize the number of bounded faces.

Empty means that no input point lies in a polygon interior. The checker also rejects an edge that passes through an input point that is not one of its endpoints. It reads the official coordinate literals as exact decimals and converts them to integers. It uses no floating-point tolerance.

The checker validates endpoint ids, repeated edges, self-loops, points on edges, crossings, graph connectivity, vertex degree, hull boundary edges, every bounded face, and total area. It traverses the planar embedding using directed edges. Each bounded face must be a simple convex polygon with no input point in its interior. The sum of face areas must equal the convex-hull area. The checker recomputes the bounded-face count.

## Constructions and public result

The pinned public solution has 770 edges. Exact checking gives 271 bounded convex faces. Euler's formula also gives 770-500+1=271. The archive records a timestamp but gives no solver, method, or AI provenance. These details are marked undisclosed. The value 271 is feasible; it is not an optimality proof.

The frozen human-method baseline follows the traditional method described in section 2.2 of the SoCG 2020 paper: start with a Delaunay triangulation, then remove edges while preserving convexity. The local implementation was built with AI assistance and uses deterministic ordering to merge convex unions. It gives 384 faces. This is not the authors' code or reported score, and it is not a published record.

Hadrien Cambazard's project page states that 100-point data sets can be solved to optimality and reports lower bounds up to 300 points. It gives no proof of optimality for this 500-point instance. The source check is dated 2026-11-06.

## Sources and data

- [CG:SHOP 2020 input instances](https://cgshop.ibr.cs.tu-bs.de/static/competitions/cgshop_2020/instances_01.zip)
- [CG:SHOP 2020 best-solution archive](https://cgshop.ibr.cs.tu-bs.de/static/competitions/cgshop_2020/best_solutions.zip)
- [Eder, Held, de Lorenzo, and Palfrader, SoCG 2020](https://doi.org/10.4230/LIPIcs.SoCG.2020.85), section 2.2
- [Cambazard, Minimum convex partition problem](https://pagesperso.g-scop.grenoble-inp.fr/~cambazah/convexpartition/minconvex.html)

The original instance and the 770-edge solution are saved under data/source and data/reference. Their SHA-256 hashes and source status are in data/source/source_notes.json.

## Run

Use .venv/bin/python. init_program.py, baseline.py, human.py, reference.py, and evolution.py expose run_code(). Default budgets are 300 seconds for generation and 60 seconds for verification, 4 GiB of memory, and one thread.
