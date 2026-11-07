# T006: cage order

## 中文

按所选配置构造连通简单正则图，并减少顶点数。T006-C01 固定度数 4、围长至少 10。T006-C02 固定度数 4、围长至少 9。可行图只给出上界，不证明最优。

程序返回 `{"vertices": n, "edges": [[u, v], ...]}`。顶点编号从 0 到 n−1。不得有自环或重复无向边。可信校验器会检查配置指定的度数、连通性和围长。T006-C02 的初始程序复用 LPS 构造，其围长至少为 10，因此也满足配置的 9。初始 seed 用 LPS 的 `X^(5,37)` 图构造，再删去两个生成元对应的完美匹配。它给出一个 50,616 顶点的可行图。它不读取320顶点人类见证。

人类复现基线是 Exoo、Goedgebeur、Jooken、Stubbe 和 Van den Eede 报告的 320 顶点图。论文称其为上界；对 n(4,10) 的最优值仍未知。仓库中的边表来自作者公开数据仓库 `genLifts/data/graphs/cage/n320_k4_g10.g6`，已转换为任务本地 JSON。来源：[论文 v2](https://arxiv.org/abs/2511.07247v2)、[作者数据仓库](https://github.com/AGT-Kulak/smallRegGirthGraphs)。

## English

Construct a connected simple regular graph for the selected configuration and minimize its order. T006-C01 has degree 4 and girth at least 10. T006-C02 has degree 4 and girth at least 9. A feasible graph gives an upper bound. It does not prove optimality.

Return `{"vertices": n, "edges": [[u, v], ...]}`. Label vertices from 0 to n−1. Do not use loops or duplicate undirected edges. The trusted checker verifies the configured degree, connectedness, and girth.

The reproduced human baseline is the 320-vertex graph reported by Exoo, Goedgebeur, Jooken, Stubbe, and Van den Eede. Their paper gives an upper bound; the minimum order n(4,10) remains unknown. The task-local JSON edge list was converted from `genLifts/data/graphs/cage/n320_k4_g10.g6` in the authors' public data repository. For C01, the starter uses the LPS graph `X^(5,37)` and deletes two generator matchings. It gives a feasible graph on 50,616 vertices and does not read the 320-vertex human witness. Sources: [paper v2](https://arxiv.org/abs/2511.07247v2), [authors' data repository](https://github.com/AGT-Kulak/smallRegGirthGraphs), [LPS paper](https://doi.org/10.1007/BF02126799).


## T006-C02 source

The best public same-parameter upper bound is 270 vertices. The C02 human reference is the 270-vertex (4,9)-graph listed by House of Graphs. The local edge list was downloaded from [House of Graphs graph6 data](https://houseofgraphs.org/data/cages/k4_g9_n270.g6). Exoo, Goedgebeur, Jooken, Stubbe, and Van den Eede report this as an upper bound in [their paper](https://arxiv.org/abs/2511.07247). They do not prove that the graph has minimum order. This configuration is accepted by Sol on 2026-11-07.

For C02, the starter reuses the LPS (4,10)-graph. Its girth is at least 10, so it is also feasible for girth at least 9. It does not read the C02 reference witness. The official runner filters this configuration until Sol accepts it.
