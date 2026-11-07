# T088：arc130 图的最小割宽

## 定义与配置

给定固定的无向简单图 arc130.mtx.rnd。构造是 130 个顶点的一个排列。对每个非空真前缀，计算一端在前缀内、另一端在前缀外的边数。目标是最小化这些边数中的最大值。该指标称为割宽。它不同于边跨度总和，也不同于最大单边跨度。

配置 T088-C01 固定 130 个顶点和 715 条边。图文件来自 Optsicom 的 cutwidth 实例库，原始文件保存在 `data/source/arc130.mtx.rnd`，SHA-256 为 `be272e3c2b11280c2c8335ae966c3d14ecef94fb4cb8fc2b049ecd7d676734a8`。源文件使用 1 起始的顶点编号。

## 已知结果与来源

Martí、Pantrigo、Duarte 和 Pardo 的 2013 年论文附录表 9 对 arc130 报告下界 62、上界 202。论文研究分支定界算法，并用 GRASP 方法产生初始解。Optsicom 当前实例页仍链接到这组历史结果。2026-11-06 检查时没有找到该固定图最优值已闭合的后续证明。此结论限于所查来源，不代表穷尽全部文献。

论文：[A Branch and Bound Algorithm for the Cutwidth Minimization Problem](https://www.uv.es/rmarti/paper/docs/other15.pdf)，DOI [10.1016/j.cor.2012.05.016](https://doi.org/10.1016/j.cor.2012.05.016)。实例页：[Optsicom Cutwidth Minimization Problem](https://grafo.etsii.urjc.es/optsicom/cutwidth.html)。公开报告的 202 上界没有随本任务恢复其原始顶点顺序。

冻结的人类方法基线是对论文中 GRASP 构造加插入局部搜索方法的独立重建：三次固定种子的随机化构造，每次随后对八个随机顶点尝试插入位置。它得到割宽 229。该结果是可重放的传统方法基线，不声称复现论文的 202 顺序。`human_reference` 和兼容评分使用 229；公开报告的 202 单独保留。

## 精确验证

评测器先检查排列恰为 1 到 130。对每条边，将其在排列中的两个位置记为 `lo < hi`。该边跨越切口 `lo` 到 `hi-1`。差分数组累加后得到全部 129 个前缀割边数，目标为其最大值。计算只用整数。

初始程序返回自然顺序。传统搜索和演化入口只读取公开图输入，不读人类或参考见证。搜索用固定随机种子与固定试次数；可用 `MATHBENCH_SEARCH_SECONDS` 显式设定探索时间。参考程序读取单独保存的重建见证。

默认按共享契约，每次生成最多 300 秒，独立验证最多 60 秒，4 GiB 内存和一个计算线程。输出保存在 `best/` 的搜索结果应由检查器重新评分。该配置仍已通过 Sol 验收（2026-11-06）。

## English

### Definition

For the fixed undirected simple graph `arc130.mtx.rnd`, a solution is a permutation of its 130 vertices. For each nonempty proper prefix, count the edges with one endpoint inside and one outside. The objective is to minimize the largest such count. This is cutwidth. It differs from the sum of edge spans and from the largest single edge span.

Configuration T088-C01 fixes 130 vertices and 715 edges. The input is from the Optsicom cutwidth instance collection. The original file is stored at `data/source/arc130.mtx.rnd`; its SHA-256 is `be272e3c2b11280c2c8335ae966c3d14ecef94fb4cb8fc2b049ecd7d676734a8`. Source labels start at 1.

### Results and sources

Appendix Table 9 of the 2013 paper by Martí, Pantrigo, Duarte, and Pardo reports a lower bound of 62 and an upper bound of 202 for arc130. The paper studies branch and bound and uses GRASP to obtain initial solutions. The current Optsicom instance page still links to these historical results. The source check on 2026-11-06 found no later proof closing this fixed instance. This statement is limited to the sources checked.

The frozen human-method baseline is an independent reconstruction of the paper's GRASP construction and insertion local-search method family. It runs three seeded constructions, then tries insertion positions for eight shuffled vertices in each. It obtains cutwidth 229. This is a reproducible traditional-method baseline; it does not claim to reproduce the paper's ordering of 202. The value 229 is the frozen human reference. The reported public upper bound 202 is recorded separately.

The checker verifies the full permutation and computes all 129 cut sizes with integer difference-array arithmetic. The initial program returns natural order. Search entries read only the public graph. They do not read comparison witnesses. The reference program reads a separately stored reconstructed witness. The task is accepted by Sol on 2026-11-06.
