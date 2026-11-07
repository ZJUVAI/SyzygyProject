# T045: Minimum linear arrangement on gd96a

## English

The graph `gd96a` has 1,096 vertices and 1,676 undirected edges. A solution is a permutation of vertex IDs 1 through 1,096. The objective is to minimize the sum of `|position(u) - position(v)|` over every edge `{u,v}`.

The official Petit MinLA experiment archive supplies the graph file. Its values match the published graph parameters. Caprara, Letchford, and Salazar-González report a heuristic value of 95,242, attributed to Rodriguez-Tello et al. (2008), and a stronger published lower bound of 77,860. We did not find the 95,242 ordering, so it remains a reported result. This task uses a reconstructed spectral-sequencing plus adjacent-swap baseline with a verified value of 147,653. The baseline does not claim the published record. See [IMPLEMENTATION.md](IMPLEMENTATION.md) for source hashes and current evidence.

## 中文

图 `gd96a` 有 1,096 个顶点和 1,676 条无向边。解是顶点 ID 1 至 1,096 的一个排列。目标是最小化每条边 `{u,v}` 的 `|position(u) - position(v)|` 之和。

Petit MinLA 官方实验归档提供了图文件，文件中的顶点数和边数与论文一致。Caprara、Letchford 和 Salazar-González 报告启发式结果 95,242，并将其归于 Rodriguez-Tello 等人 2008 年的工作；同篇论文给出 77,860 的更强下界。我们没有找到 95,242 对应的排列，因此只记录为文献报告值。本任务使用复现的谱排序加相邻交换方法，验证值为 147,653。该基线不声称达到文献纪录。来源哈希和当前证据见 [IMPLEMENTATION.md](IMPLEMENTATION.md)。
