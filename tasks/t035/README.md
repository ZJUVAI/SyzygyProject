# T035: (4,10)-cage order

## 中文

构造一个连通简单图。每个顶点的度数必须为 4，最短圈长必须至少为 10。目标是减少顶点数。可行图只给出上界，不证明最优。

程序返回 `{"vertices": n, "edges": [[u, v], ...]}`。顶点编号从 0 到 n−1。不得有自环或重复无向边。可信校验器会检查顶点度数、连通性和围长。初始 seed 用 LPS 的 `X^(5,37)` 图构造，再删去两个生成元对应的完美匹配。它给出一个 50,616 顶点的可行图。它不读取320顶点人类见证。

人类复现基线是 Exoo、Goedgebeur、Jooken、Stubbe 和 Van den Eede 报告的 320 顶点图。论文称其为上界；对 n(4,10) 的最优值仍未知。仓库中的边表来自作者公开数据仓库 `genLifts/data/graphs/cage/n320_k4_g10.g6`，已转换为任务本地 JSON。来源：[论文 v2](https://arxiv.org/abs/2511.07247v2)、[作者数据仓库](https://github.com/AGT-Kulak/smallRegGirthGraphs)。

## English

Construct a connected simple graph. Every vertex must have degree 4, and the shortest cycle must have length at least 10. Minimize the number of vertices. A feasible graph gives an upper bound. It does not prove optimality.

Return `{"vertices": n, "edges": [[u, v], ...]}`. Label vertices from 0 to n−1. Do not use loops or duplicate undirected edges. The trusted checker verifies degrees, connectedness, and girth.

The reproduced human baseline is the 320-vertex graph reported by Exoo, Goedgebeur, Jooken, Stubbe, and Van den Eede. Their paper gives an upper bound; the minimum order n(4,10) remains unknown. The task-local JSON edge list was converted from `genLifts/data/graphs/cage/n320_k4_g10.g6` in the authors' public data repository. The starter uses the LPS graph `X^(5,37)` and deletes two generator matchings. It gives a feasible graph on 50,616 vertices and does not read the 320-vertex human witness. Sources: [paper v2](https://arxiv.org/abs/2511.07247v2), [authors' data repository](https://github.com/AGT-Kulak/smallRegGirthGraphs), [LPS paper](https://doi.org/10.1007/BF02126799).
