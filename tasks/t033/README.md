# T033: Gset G70 maximum cut

## English

This task uses the public Gset G70 graph. It has 10,000 vertices and 9,999 undirected edges. Each edge has weight +1. A construction assigns each vertex to side 0 or side 1. The score is the number of edges whose endpoints have different sides. The evaluator reads the fixed graph and recomputes the integer score.

The graph is stored in `data/instance.json`. The byte-exact source is archived at `data/source/G70`, from [Stanford G70](https://web.stanford.edu/~yyye/yyye/Gset/G70), with SHA-256 `0d965a2ff1444cc71d7740824b5b3a5e09fc1843cbf6d90691b52d5221987061`. The candidate returns only a 10,000-element `labels` list. It must not provide a graph or a score.

The 2024 LPI paper reports 9,594 on its G70 test instance and 9,595 as a calibration value. Cosm v4 (revised 2026-10-11) reports a heuristic score of 9,595. LPI reports 9,594 on its G70 test instance and 9,595 as a calibration value. No public assignment was replayed here. A paper reports numerical SDP value 9,683; this task has not certified it as an upper bound, so the 88-point difference is not a certified optimality gap. The checked sources do not prove 9,595 optimal. See `sota.json` for the evidence and its limits.

The reproduced traditional-method baseline is steepest single-vertex FLIP local search. It uses four random starts, default seed 0, and up to 10,000 flips per start. The saved witness at `data/human_g70_1flip.json` has cut 8,616 and records its actual flips per restart. This is a task-local reproduction of the published FLIP neighborhood. It is not the G70 result from the BLS paper and does not read a public witness.

The cold start assigns every vertex to side 0. The search baseline and evolution entry use seeded 1-flip local search. They do not read the external comparison witness in `data/`. The task is accepted by Sol on 2026-11-06.

## 中文

本任务使用公开的 Gset G70 图。图有 10,000 个顶点和 9,999 条无向边。每条边的权重为 +1。构造须把每个顶点分到 0 或 1 侧。目标是最大化两端位于不同侧的边权和。评测器从固定图读取边，并精确重算整数成绩。

图保存在 `data/instance.json`。来源是 [Stanford G70 实例](https://web.stanford.edu/~yyye/yyye/Gset/G70)。原始文件的 SHA-256 为 `0d965a2ff1444cc71d7740824b5b3a5e09fc1843cbf6d90691b52d5221987061`。候选程序只返回含 10,000 个整数的 `labels` 列表。候选不能提供图或声明成绩。

2024 年 LPI 论文在 G70 测试实例上报告 9,594，并将 9,595 列为校准值。Cosm v4（2026-10-11 修订）报告启发式分数 9,595。LPI 在 G70 测试实例上报告 9,594，并将 9,595 列为校准值。此处没有复算公开见证。论文报告的 SDP 数值为 9,683；本任务未认证它是上界，因此两数相差 88 不构成已认证的最优性差距。来源和限制见 `sota.json`。

已复现的传统方法基线采用陡降单顶点 FLIP 局部搜索。它使用 4 个随机起点，默认随机种子为 0，每个起点最多翻转 10,000 次。保存于 `data/human_g70_1flip.json` 的见证割值为 8,616，并记录每次重启的实际翻转次数。这是本任务对已发表 FLIP 邻域的本地复现，不是 BLS 论文报告的 G70 成绩，也不读取公开见证。

冷启动将所有顶点放在 0 侧。搜索基线和进化入口使用固定种子的 1-flip 局部搜索，不读取 `data/` 中的外部对照见证。任务状态为已通过 Sol 验收（2026-11-06）。
