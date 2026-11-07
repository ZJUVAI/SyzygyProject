# T024：41 点无四环图

## 中文

固定 41 个顶点，提交简单无向图。图中不能有长度为 4 的环，目标是最大化边数。无四环等价于任意两个不同顶点最多有一个共同邻居。检查器精确检查该条件并重算边数。

Afzaly–McKay 公开表在 41 点行给出 `≥132` 条边和三个图。表格说明中，边数前的 `≥` 表示作者尚未证明更多边不可能。38 点行的 117 前没有 `≥`，因此38点配置已有精确最优值，已排除。本任务采用仍开放的41点配置。

任务数据保存原始 sparse6 文件、首条记录解码后的邻接表及 SHA-256。复算结果为41点、132边，所有顶点对的共同邻居数至多为1。该构造证明下界，不证明最优性。

公开表给出40点精确值127。删去41点图的任意一个顶点，所得40点诱导子图至多有127条边。对41种删点结果求边数总和，每条原边恰被计入39次，因此 `39m ≤ 41×127`，从而 `m ≤ 133`。当前可证明区间为 `132 ≤ ex(41,C4) ≤ 133`。

状态：已通过 Sol 验收（2026-11-06）。

## English

The fixed graph has 41 vertices. It is simple and undirected, and it must contain no cycle of length four. The objective is to maximize the number of edges. A graph is C4-free exactly when every pair of distinct vertices has at most one common neighbor. The checker tests this condition exactly and recomputes the edge count.

The Afzaly–McKay public table lists at least 132 edges and three graphs at order 41. Its notes say that a `>=` prefix means that a larger edge count has not been ruled out. The 38-vertex entry 117 has no such prefix, so that solved order was excluded. This task uses the open 41-vertex instance.

Task data includes the original sparse6 file, the decoded adjacency list for its first record, and a SHA-256 digest. Recalculation gives 41 vertices and 132 edges, with at most one common neighbor for every vertex pair. This construction proves a lower bound, not optimality.

The public table gives the exact value 127 at order 40. Deleting any vertex from a 41-vertex graph gives a 40-vertex induced subgraph with at most 127 edges. Summing over all 41 deletions counts each original edge 39 times. Thus `39m <= 41*127`, so `m <= 133`. The proved interval is `132 <= ex(41,C4) <= 133`.

Status: accepted by Sol on 2026-11-06.
