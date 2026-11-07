# T022：Ramsey 数下界图

## 中文

固定参数为禁止 5 阶团和 5 阶独立集。程序提交一个简单无向图。目标是最大化顶点数。检查器会精确检查图及其补图中是否含 5 阶团，并按顶点数计分。Exoo 的 1989 年论文建立了 42 点构造对应的下界；档案中用于复现的具体图行未单独注明发现者。由此得到 $R(5,5)\ge43$。目前的公开界为 $43\le R(5,5)\le46$，所以该参数仍未解决。Angeltveit 和 McKay 证明 $R(5,5)\le46$，所以检查器采用 45 个顶点上限。该上限由已发表上界推出，不会排除可行改进。

McKay 的公开数据档案 `r55_42some.g6` 提供人类见证。任务数据保存第一条 graph6 编码及其展开的邻接表。它有 42 个顶点、425 条边，检查器重算了全部禁形条件。传统基线从一个 5 环开始，以固定随机种子逐点尝试扩展；它不读取人类或参考见证。

实现状态：已通过 Sol 验收（2026-11-06）。

## English

The fixed parameters forbid a clique of order 5 and an independent set of order 5. A candidate is a simple undirected graph. The objective is to maximize its number of vertices. The checker verifies the graph and its complement exactly, then scores the vertex count. Exoo’s 1989 paper establishes the lower bound from a 42-vertex construction. The specific archive row used here is not individually attributed. The published construction establishes $R(5,5)\ge43$. The current public bounds are $43\le R(5,5)\le46$, so this instance remains open. Angeltveit and McKay prove $R(5,5)\le46$, so the checker has a 45-vertex limit derived from this published bound. It does not exclude a feasible improvement.

The public McKay archive `r55_42some.g6` supplies the human witness. Task data stores its first graph6 line and expanded adjacency list. It has 42 vertices and 425 edges. The checker recomputes both forbidden-subgraph conditions. The classical baseline starts from a 5-cycle and tries seeded vertex extensions. It does not read the human or reference witness.

Implementation status: accepted by Sol on 2026-11-06.
