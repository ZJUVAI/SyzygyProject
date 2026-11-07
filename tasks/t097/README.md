# T097 — Minimum convex cover of `socg_fixed92`

## English

### Problem

Cover the fixed `socg_fixed92` region with the fewest convex polygons. Each cover polygon must stay inside the region. The cover pieces may overlap. The score is the number of pieces, and lower is better.

The official input is a simple polygon with 92 boundary vertices and no holes. Its exact bytes are stored in `data/source/socg_fixed92.instance.json` and checked by SHA256. The full mathematical problem allows arbitrary real coordinates. A solution encodes its finite coordinate tuple in one real algebraic number field `Q(alpha)`: an irreducible integer polynomial for `alpha`, a rational isolating interval, and rational polynomials in `alpha` for each x and y coordinate. This representation does not cap algebraic degree or coefficient size. It covers the full optimization domain because the finite-piece feasibility statement is a first-order formula over the reals with rational input; if a real-coordinate cover exists, real-closed-field transfer gives an algebraic-coordinate cover of the same size.

The exact checker validates the field, convexity, and equality of regions. It builds the arrangement of every input and cover edge, decomposes the plane into vertical cells, and checks each open cell with exact algebraic arithmetic. The sets are closed, so equality of the interiors gives equality of the regions. It does not rely on sampling or floating-point tolerances.

### Fixed evidence

The Shadoks CG:SHOP 2023 viewer reports 15 pieces for `socg_fixed92`. Its archived SVG rounds the displayed coordinates. We inverse-transform them and infer nearby integer coordinates, each within 0.000356 of the displayed value. The rounded SVG does not identify the original submitted coordinates uniquely. The inferred integer polygons form a feasible 15-piece cover and pass exact vertical-decomposition validation. A separate audit by the main reviewer also triangulated the region and checked containment and uncovered area with exact fractions.

The viewer's `Optimal` CPLEX status refers to a set-cover model over its generated candidate collection. It is not a proof that 15 pieces is optimal over all convex polygons. The official CG:SHOP ranking is an aggregate team ranking; it does not publish each team's value for this instance. The viewer is therefore recorded as a public 15-piece result, but the checked public-record inventory for this instance is incomplete. No global optimum proof for this instance was found in the sources checked on 2026-11-06. In particular, the 2026 rotten-potato paper gives an approximation algorithm; it does not close this fixed instance.

The Shadoks and official challenge sources do not state whether AI tools were used to produce this witness. Its provenance is recorded as undisclosed. The contest itself only accepted rational solution coordinates. This task extends the mathematical domain to all real-coordinate covers; the rational 15-piece witness remains valid in that domain.

### Programs and evidence

- `init_program.py` starts from an exact ear-clipping triangulation. It uses only the public input file.
- `baseline.py` applies seeded greedy convex-hull merges to that triangulation.
- `evolution.py` runs two seeded greedy-merge restarts. Neither search reads the human or reference witness.
- `human.py` rebuilds the feasible integer cover inferred from the rounded Shadoks viewer.
- `reference.py` decodes the same published polygons from the archived viewer HTML.
- `check.py` recomputes the piece count after exact full-region validation.

Use `.venv/bin/python -m pytest tasks/t097 -q` to run the task tests. The task is `accepted_by_sol`.

### Sources

- [CG:SHOP 2023 official competition and ranking](https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2023/)
- [Shadoks 2023 solution viewer](https://pageperso.lis-lab.fr/guilherme.fonseca/cgshop23view/)
- [Shadoks Approach to Convex Covering, SoCG 2023](https://doi.org/10.4230/LIPIcs.SoCG.2023.67)
- [CG:SHOP Challenge 2023 overview, 2026](https://doi.org/10.57717/cgt.v5i4.115)
- [Covering Polygons is Even Harder](https://arxiv.org/abs/2106.02335)
- [Peeling Rotten Potatoes for a Faster Approximation of Convex Cover](https://arxiv.org/abs/2604.17983)
- [An Overview of Minimum Convex Cover and Maximum Hidden Set, v2](https://arxiv.org/abs/2403.01354v2)

## 中文

### 问题

用尽量少的凸多边形覆盖固定区域 `socg_fixed92`。每个覆盖片必须位于输入区域内。覆盖片之间允许重叠。目标是多边形数量，越少越好。

官方输入是一个有 92 个边界顶点、没有洞的简单多边形。精确输入保存在 `data/source/socg_fixed92.instance.json`，检查器会核对 SHA256。数学目标允许任意实坐标。解用一个实代数数域 `Q(alpha)` 编码全部坐标：给出 `alpha` 的不可约整数多项式、有理隔离区间，以及每个坐标关于 `alpha` 的有理系数多项式。表示没有代数次数或系数大小上限。这个表示覆盖完整优化域：有限个凸片的可行性可写为有理输入上的实数一阶公式。若实坐标解存在，实闭域转移给出同数量的代数坐标解。

精确检查器验证数域、凸性和区域相等。它为输入边和覆盖边建立完整排列，用竖直分解形成所有开单元，再用精确代数运算检查每个单元。区域和覆盖片都是闭集，因此内部相等可推出区域相等。检查器不使用采样或浮点容差。

### 固定证据

Shadoks 的 CG:SHOP 2023 查看器报告 `socg_fixed92` 可用 15 个凸片覆盖。存档 SVG 会舍入显示坐标。我们逆变换坐标并推断附近的整数坐标，误差小于 0.000356。舍入后的 SVG 不能唯一确定原始提交坐标。推断得到的整数多边形构成可行的 15 片覆盖，并通过精确竖直分解验证。主审还用另一种精确分数方法对区域三角化，并核对包含关系和未覆盖面积。

查看器里的 CPLEX `Optimal` 只表示在它生成的候选集合上，集合覆盖模型达到最优。它不能证明所有凸多边形组成的区域覆盖全局最优。官方 CG:SHOP 排名是各队总分，不公开每队在这个实例上的数量。因此我们把查看器中的 15 记录为公开结果，但注明该实例的公开纪录清单不完整。截至 2026-11-06 所检查来源，没有找到此实例的全局最优证明。2026 年的 rotten-potato 论文给出近似算法，没有解决这个固定实例。

Shadoks 与竞赛来源没有说明该见证是否使用 AI 工具，故 AI 来源记为未披露。竞赛只接受有理坐标；本任务采用完整实坐标目标。有理坐标的 15 片见证在完整目标中仍然可行。

### 程序和记录

- `init_program.py` 从精确耳切三角化开始，只读取公开输入。
- `baseline.py` 对三角化结果进行带种子的贪心凸包合并。
- `evolution.py` 从三角化运行两次带种子的贪心搜索。搜索不读取人类见证或参考见证。
- `human.py` 重建从 Shadoks 舍入图中推断出的可行整数坐标覆盖。
- `reference.py` 从存档网页解析并重建同一公开构造。
- `check.py` 在完整精确验证后重算凸片数量。

运行 `.venv/bin/python -m pytest tasks/t097 -q` 可执行任务测试。当前状态为 `accepted_by_sol`。
