# T059：DIMACS C2000.9 最大团

## 中文

配置 `T059-C01` 固定为 C2000.9 无向简单图，含 2000 个顶点和 1,799,532 条边。目标是最大化两两相邻的不同顶点数。checker 从原始 DIMACS 文件重建邻接位集，并精确检查候选团的每一对顶点。

公开人类构造是 Grosso、Locatelli 与 Pullan 报告的 80 顶点团。论文先给出 79 顶点团，并说明更长运行得到 80 顶点团。完整零基顶点集已保存并逐边验证。该数值是已知可行团大小，不代表已证明最大。

Krpan 与 Povh 在 2026 年论文中报告 C2000.9 的整数上界 168，并称此前的 177 改进为 168。方法组合了核心约简与 Lovász theta 上界。论文说明该次运行耗时 17 天 18 小时，并使用 192 线程。这个上界单独记录为作者报告的结果；本任务未重新运行 SDP，也未独立重放其上界计算。论文把该实例列为最优值未知。

原 DIMACS 文件以 gzip 保存，解压后的 SHA-256 为 `aa4b1d7d…d164f16`。checker 解压时重算该哈希，检查 DIMACS 头为 2000 顶点、1,799,532 条边。简单初始程序返回单顶点。传统搜索使用种子化贪心团与一换二局部改进。搜索代码不读取人类或参考见证。

## English

Configuration `T059-C01` fixes the undirected simple graph C2000.9, with 2,000 vertices and 1,799,532 edges. The objective is to maximize the number of distinct pairwise adjacent vertices. The checker rebuilds adjacency bitsets from the pinned DIMACS file and checks every candidate pair exactly.

The public human construction is the 80-vertex clique reported by Grosso, Locatelli, and Pullan. Their paper first gives a 79-vertex clique and then states that a longer run found an 80-vertex clique. The full zero-based vertex list is saved and checked against every edge. This is a feasible clique size, not a proof of maximality.

A 2026 paper by Krpan and Povh reports an integer upper bound of 168 for C2000.9, improving the earlier 177. Their method combines core reductions with the Lovász theta upper bound. The paper says that this run took 17 days and 18 hours on 192 threads. This is recorded as an author-reported result. This task does not rerun the SDP or independently replay the upper-bound computation. The paper states that the optimum is unknown.

The original DIMACS file is stored with gzip compression. Its uncompressed SHA-256 is `aa4b1d7d…d164f16`. The checker recomputes this hash while loading and confirms the 2,000-vertex, 1,799,532-edge header. The simple initial program returns one vertex. The traditional search uses seeded greedy clique construction and one-for-two local improvement. Search code does not read the human or reference witness.
