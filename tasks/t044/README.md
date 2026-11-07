# T044: 最大度 3、直径至多 5 的图

## 中文

配置 T044-C01 研究简单无向连通图。每个顶点的度至多为 3，任意两点间最短路径长度至多为 5。标量目标是顶点数 `n`，单位为个顶点，方向为最大化。程序以 `n` 和无向边列表提交图。检查器逐边检查无向简单图约束，并从每个顶点运行精确 BFS，重新计算连通性、最大度和直径。它不使用候选程序声明的分数。

Comellas 的当前度直径表在 `(3,5)` 项列出 70。该项没有加粗，表示表未标为最优。Moore 上界为 94。因此当前证据是 `70 ≤ n_3(5) ≤ 94`，精确最大值仍未解决。详情页最后修改时间为 2026-10-14；主表截至 2026-11-06 仍显示 70。历史来源列出 von Conta (1983) 与 Alegre、Fiol、Yebra (1986)。任务保存并分别验证了来源页提供的 70 点邻接表。

人类基线程序读取 Alegre–Fiol–Yebra 原始邻接列表，并重建 70 点图。固定参考程序读取 Comellas 2024 年从 28 点 Coxeter 图构造出的另一份 70 点邻接列表。两份数据的原始 SHA-256、来源位置和复算结果均保存在 `records.json`。它们都精确通过本任务的度数和直径检查。主表注明网站内容（若干 SageMath 脚本除外）不使用 AI；历史图归于1983/1986年来源。

初始程序返回单点图。传统搜索从小图开始，用固定随机种子按配置模型抽取三正则图，拒绝自环、重边、不连通图和直径超过 5 的图。它不读取两份比较见证。默认尝试 384 次；可用 `MATHBENCH_SEARCH_SECONDS` 设置按时间截断的探索。

共享运行器默认给生成 300 秒，给验证 60 秒，内存 4 GiB，一个 CPU 线程。此配置仍为“已通过 Sol 验收（2026-11-06）”。Moore 上界用于限制候选输入规模，不用作精确最优性证明。

## English

Configuration T044-C01 studies simple undirected connected graphs. Every vertex has degree at most 3, and every pair of vertices has distance at most 5. The scalar objective is the order `n`, measured in vertices and maximized. A candidate returns `n` and an undirected edge list. The checker validates every edge and runs exact breadth-first search from every vertex to recompute connectivity, maximum degree, and diameter. It ignores candidate score claims.

Comellas's current degree-diameter table lists 70 for `(3,5)`. The entry is not bold, so the table does not mark it optimal. The Moore bound is 94. The checked range is therefore `70 <= n_3(5) <= 94`, and the exact maximum remains open. The detail page was last modified on 2026-10-14. The main table still listed 70 on 2026-11-06. The historical source row cites von Conta (1983) and Alegre, Fiol, and Yebra (1986). This task saves and checks the 70-vertex adjacency list from that source page.

The human baseline reads and rebuilds the original Alegre–Fiol–Yebra adjacency list. The fixed reference program reads a second 70-vertex adjacency list for Comellas's 2024 construction from the 28-vertex Coxeter graph. The raw file hashes, source locations, and exact check results are recorded in `records.json`. Both graphs pass the task's degree and diameter checks. The source page states that its contents are AI-free except for some SageMath scripts; it attributes the historical graph to the 1983/1986 sources.

The initial program returns a one-vertex graph. The traditional search starts from small graphs and uses a fixed random seed to sample cubic graphs with the configuration model. It rejects loops, repeated edges, disconnected graphs, and graphs with diameter above 5. It does not read either comparison witness. The default budget is 384 attempts. `MATHBENCH_SEARCH_SECONDS` enables a wall-clock exploration cutoff.

The shared runner allows 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one CPU thread by default. This configuration is accepted by Sol on 2026-11-06. The Moore bound limits candidate input size; it is not used as a proof of the exact optimum.

## Sources

- [Current degree-diameter table](https://web.mat.upc.edu/francesc.comellas/delta-d/table_degree_diameter.html), checked 2026-11-06.
- [Details for degree 3, diameter 5](https://web.mat.upc.edu/francesc.comellas/delta-d/desc_g/desc_g5.html), last modified 2026-10-14. It reports order 70, Moore bound 94, the vC/AFY references, the original adjacency file, and the Comellas 2024 Coxeter construction.
- von Conta (1983), “Torus and other networks as communication networks with up to some hundred points,” *IEEE Transactions on Computers* 32, 657–666; and Alegre, Fiol, and Yebra (1986), “Some large graphs with given degree and diameter,” *Journal of Graph Theory* 10, 219–224, [DOI](https://doi.org/10.1002/jgt.3190100211).
