# T040: Maximum-volume polytope on the sphere

## 中文

在三维单位球面 (S^2) 上选 11 个不同点，最大化这些点的凸包体积。唯一配置为 T040-C01。体积单位为半径为 1 的长度单位的立方。每个不同的球面点都是其凸包的极点，所以 11 个互异点自动给出 11 个顶点。

候选程序可返回 11 个精确有理笛卡尔坐标，也可返回 11 对立体投影参数 ((u,v))。检查器用公式

\[
(x,y,z)=\left(\frac{2u}{1+u^2+v^2},\frac{2v}{1+u^2+v^2},\frac{1-u^2-v^2}{1+u^2+v^2}\right)
\]

精确构造单位球面点。该参数化遗漏北极；把整个多面体旋转后可避开坐标图奇点，旋转不改变体积。浮点输入按其精确二进制有理值解释，须精确满足单位范数。

正式体积由纯有理数算法重算。算法枚举 165 个点三元组，筛出支撑平面，以标准整数四元组合并同一平面，再对共面点作精确二维凸包，并按面扇形三角剖分。它不会重复计算共面多边形面。浮点凸包只可用于搜索反馈。

人类构造与公开报告值来自 Hardin、Sloane、Smith 的 1994 年资料。其结果表列出 11 点体积 `2.354634495069`，坐标档案为 `data/maxvol.3.11.txt`。程序把每个舍入小数视为精确有理数，再按其立体投影参数重构单位球面点。因此输出是对公开舍入坐标的有理重构，**不是**原始未舍入坐标，也不能复现来源的未舍入分数。重构见证与分数由本任务独立计算，保存在 `data/reference/sloane11_rational_stereographic.json`。复算值为 `2.3546344950686153`，与来源报告值在其显示精度内一致。

Hoehner 与 Ledford 的 2026 年论文解决了 9 点情形，并在引言中列出 10、11 及所有至少 13 点的情形仍未解决。作者说明 10 点另有一篇即将发表的论文。故本任务选择 11 点。检查日期 2026-11-06 时，arXiv 记录仍为 2026-08-05 提交的 v1；本任务没有找到 11 点闭合证明。该坐标只给出可行下界，不证明全局最优。

## English

Choose 11 distinct points on the unit sphere (S^2) in three dimensions. Maximize the volume of their convex hull. T040-C01 is the only configuration. Volume is measured in cubed unit-radius length units. Each distinct sphere point is an extreme point of its convex hull, so 11 distinct points give 11 vertices.

A candidate may return 11 exact rational Cartesian triples or 11 stereographic pairs ((u,v)). The checker maps each pair to the sphere with the formula above. This chart omits the south pole. A rotation of the whole polytope avoids the chart singularity and preserves volume. A floating-point coordinate is treated as its exact binary rational value, so it must have norm exactly one.

The official volume is recomputed with rational arithmetic. The checker enumerates all 165 point triples, finds supporting planes, merges coplanar triples by a canonical integer plane, builds the exact two-dimensional hull of each face, and triangulates each polygon once. Floating-point hulls may guide search, but they do not certify a score.

The human construction and reported value come from the 1994 Hardin, Sloane, and Smith results. Their table lists volume `2.354634495069` for 11 points. The coordinate archive is `data/maxvol.3.11.txt`. The program reads each displayed decimal as an exact rational and reconstructs a point on the unit sphere from its stereographic parameters. This is a rational reconstruction from rounded public coordinates. It is not the original unrounded witness or its unrounded score. The reconstructed witness and exact score are saved in `data/reference/sloane11_rational_stereographic.json`. The recomputed value is `2.3546344950686153`, which agrees at the source's reported precision.

Hoehner and Ledford solved the 9-point case in a 2026 paper. Its introduction lists 10, 11, and every case from 13 onward as open, and says a separate paper by the first author handles 10. On 2026-11-06, the arXiv record still showed the version submitted on 2026-08-05. No proof closing the 11-point case was found for this implementation. The archived coordinates give a feasible lower bound, not a proof of global optimality.

## Sources

- [Hardin, Sloane, and Smith, maximum-volume spherical codes page](https://neilsloane.com/maxvolumes/index.html). It attributes the results to the authors, labels them putatively optimal, and reports volume `2.354634495069` for dimension 3 and 11 points. The page identifies the summary as copyright February 1994.
- [Hardin, Sloane, and Smith, 11-point coordinate archive](https://neilsloane.com/maxvolumes/dim3/maxvol.3.11.txt). SHA-256: `5add684454391c037f97c1d1dd05374387fd3c7b3a12cf13708ebbc7808727e3`.
- [Hoehner and Ledford, arXiv:2608.04392v1](https://arxiv.org/abs/2608.04392v1), submitted 2026-08-05, Section 1 and Table 1.
- [Mutoh, “The Polyhedra of Maximal Volume Inscribed in the Unit Sphere,” 2003 proceedings version](https://doi.org/10.1007/978-3-540-44400-8_22), which reports a weaker numerical local candidate, volume `2.35462915`, for 11 vertices.

## Reproduction and limits

Run the checker with the saved witness using `.venv/bin/python`. The exact rational volume is the reproduced baseline. The literature's rounded reported value is stored separately in `records.json` and `sota.json`. Mutoh's weaker local candidate is retained as a historical result, not as the highest reported value. The rounded archive does not retain the original unrounded coordinates.


## Additional sizes

C02 has 13 points and C03 has 15 points. The Hardin–Sloane–Smith author table reports volumes 2.612834152060 and 2.804379381835. Its displayed decimal coordinates are saved locally. The human and fixed reference programs use exact rational stereographic points reconstructed from these archives. The checker verifies the sphere equation, distinct points, and exact supporting-plane volume. The author table treats these volumes as putative optima. The new configurations are accepted by Sol on 2026-11-07.

新增 C02 为13点，C03 为15点。公开报告体积分别为2.612834152060和2.804379381835。用存档坐标重建有理球面点，再精确计算凸包体积。公开报告与精确复算分开记录。新增配置已通过 Sol 验收（2026-11-07）。
