# T036：K28 直线交叉数

## 中文

本任务固定 28 个点和完全图 K28。点须互异，且任意三点不共线。每一对不共享端点的边若内部相交，计为一次交叉。目标是最小化交叉对数。评测器用精确有理数逐个检查 3,276 个三元组，并检查 61,425 个不相交边对。坐标可为整数，也可用规范分数字符串表示，例如 `"3/7"`。浮点数、布尔值及非规范分数会被拒绝。候选声明的分数不参与计算。

弱人类基线取 28 个抛物线点 `(i, i²)`，其中 `i=0,...,27`。严格凸位置下，每四点构成凸四边形，恰有一对对角线相交。因此交叉数为 `C(28,4)=20,475`。这是从经典凸四边形方法重建的构造，并非从论文下载的坐标见证。Lovász、Vesztergombi、Wagner 与 Welzl 2003 年论文引言说明了凸位置四点组与交叉数的关系。本任务独立生成坐标并精确复算该值。

公开来源报告的 K28 值为 7,234，且报告下界为 7,233；这里没有取得或重放该 7,234 点集。因此 records 将公开报告和本地重建的弱基线分开记载。Abrego、Fernández-Merchant 与 Salazar 的综述指出 28、29 阶仍开放，而 27 与 30 阶已解决。2024 年离散数学论文仍将 28 阶列为未解。MathWorld 引用 Schaefer 2026 年综述第 86 页，仍称 K28 是最小未解情形，且值为 7,233 或 7,234。来源检查日期为 2026-11-06。此任务状态为已通过 Sol 验收（2026-11-06）。

传统搜索从固定种子的随机整数一般位置点集开始，执行 80 次单点替换贪心搜索，只接受仍满足一般位置且交叉数不增的替换。它不读取人类或公开见证。seed 0 搜索运行 80 次并接受 16 次替换，得到 12,516 次交叉。构造、复算结果、预算和可重放命令保存在 `best/`。默认运行器预算为生成 300 秒、验证 60 秒、4 GiB 内存和一个 CPU 线程。

## English

This task fixes 28 points and the complete graph K28. The points must be distinct, and no three points may be collinear. Each pair of edges with no shared endpoint counts once when their relative interiors intersect. The objective is to minimize this number. The checker uses exact rational arithmetic. It checks all 3,276 triples and all 61,425 pairings of disjoint edges. Coordinates may be integers or canonical rational strings such as `"3/7"`. Floats, booleans, and non-canonical fractions are rejected. The checker ignores candidate score claims.

The weak human baseline uses the 28 points `(i, i²)` for `i=0,...,27`. Every four points in this strictly convex set form a convex quadrilateral, with one crossing pair of diagonals. The crossing count is therefore `C(28,4)=20,475`. This is a reconstructed construction from the classical convex quadrilateral method. It is not a coordinate witness downloaded from the paper. The 2003 paper by Lovász, Vesztergombi, Wagner, and Welzl explains the relation between four-point convex sets and crossings in its introduction. This task generates the points and recomputes the count exactly.

Public sources report 7,234 crossings for K28 and a lower bound of 7,233. This task did not obtain or replay the 7,234-point-set witness. The records keep that report separate from the weaker locally reconstructed baseline. The survey by Abrego, Fernández-Merchant, and Salazar says that orders 28 and 29 remain open, while orders 27 and 30 are solved. A 2024 discrete mathematics paper and 2026 reference material still list order 28 as open. Sources were checked on 2026-11-06. Status: accepted by Sol on 2026-11-06.

The traditional search starts from a seeded random integer point set in general position. It makes 80 greedy single-point replacement attempts. It accepts only replacements that preserve general position and do not increase the crossing count. It does not read human or public witnesses. The seed 0 run completed 80 attempts and accepted 16 replacements. It found 12,516 crossings. The construction, exact result, budget, and replay command are saved under `best/`. Default runner limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one CPU thread.

Main source correction: the retrieved 2011 survey has Table 1, no Table 3. It supports open status, while the numeric7233–7234 interval is attributed to Bernardo M. Abrego’s first-party comment at https://oeis.org/A014540/internal . The current crossingconstants page concerns asymptotic constants and is not cited as a K28 table. FrozenH20475 is a reconstructed weak convex-position formula; reported besthuman7234 remains unverified locally.
