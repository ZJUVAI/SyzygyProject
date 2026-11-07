# T061: minimum-edge C6-saturated graph on 100 vertices

## Definition

The fixed graph has 100 labeled vertices `0,...,99`. It must be a simple undirected graph with no simple cycle of length 6. For each nonedge `uv`, there must be a simple path of exactly 5 edges from `u` to `v`. Adding `uv` then completes a simple C6. The objective is to minimize the number of edges.

The checker enumerates simple 5-edge paths, using a visited-vertex bit mask. If a path's endpoints are already joined by an edge, it detects a C6. For every nonedge, it requires the endpoints in the path set. This checks paths with six distinct vertices; repeated-vertex walks cannot pass.

## Published construction and current bounds

Lan, Shi, Wang, and Zhang prove for `n >= 9` that

`4n/3 - 2 <= sat(n,C6) <= 4n/3 + epsilon^2/2 - 5epsilon/6`,

where `epsilon` is the residue of `n` modulo 3. For `n=100`, `epsilon=1`, so the integer edge count lies between 132 and 133. The theorem gives a 133-edge construction. The exact value is not determined by these bounds.

The paper's construction at `n=3t+1` starts with the nine-vertex, twelve-edge graph `H` in Figure 1(a), adds `t-3` paths `a_i-b_i-c_i` with edges `x_1a_i` and `x_2c_i`, and attaches one leaf to `y_4`. For this task, `t=33`, so it adds 30 paths and one leaf. The total is `12 + 30*4 + 1 = 133` edges.

The nine-vertex core was decoded from the vector drawing in the arXiv v3 PDF and cross-checked against the proof paths in Section 2. Its vertices are `x1,x2,y1,y2,y3,y4,a0,b0,c0`; its 12 edges are:

- `x1-x2`, `x1-y1`, `x1-y2`, `x1-a0`;
- `x2-y3`, `x2-y4`, `x2-c0`;
- `y2-y1`, `y2-y3`, `y2-y4`;
- `a0-b0`, `b0-c0`.

`human.py` rebuilds the theorem construction. `reference.py` reads the frozen JSON copy from `data/reference/`. Exact local validation confirms 133 edges, no simple C6, and a simple five-edge path for each of the 4817 nonedges.

Sources checked 2026-11-06:

- Lan, Shi, Wang, and Zhang, [The saturation number of C6](https://doi.org/10.1016/j.disc.2025.114504), Theorem 1.5 and Figure 1. The version used for decoding was [arXiv:2108.03910v3](https://arxiv.org/html/2108.03910v3), dated 2023-11-07. The downloaded PDF SHA-256 is recorded in `IMPLEMENTATION.md`.
- The 2026 paper [Minimizing the number of edges in C[4,6]-saturated graphs](https://arxiv.org/abs/2608.18551) studies graphs saturated with respect to the family of cycle lengths 4 through 6. That is a different constraint from saturation for C6 alone and does not close this parameter.

The checked C6 sources leave a one-edge interval, 132–133, at `n=100`. The literature check is not exhaustive.

## Programs and limits

- `init_program.py` scans all possible edges in a fixed order. It adds an edge only if no simple five-edge path already joins its endpoints. The final graph is C6-free and saturated by monotonicity. It does not read comparison data.
- `baseline.py` runs four fixed-seed randomized edge orders through the same greedy rule and keeps the smallest graph. It reads no human or reference witness.
- `human.py` rebuilds the published 133-edge construction.
- `reference.py` replays the frozen 133-edge construction.
- `evaluator.py` uses the shared runner. Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread.

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t061/test_task.py -q
.venv/bin/python -m json.tool tasks/t061/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t061/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t061/records.json > /dev/null
```

## 定义

固定图有 100 个标记顶点 `0,...,99`。图是简单无向图，不含长度为 6 的简单环。对每个非边 `uv`，图中必须存在从 `u` 到 `v`、恰有 5 条边的简单路径。加入 `uv` 后会形成简单 C6。目标是最小化边数。

检查器用访问顶点位掩码枚举简单 5 边路径。如果路径端点已有边，就发现一个 C6。每个非边的两个端点都必须出现在路径端点集合中。这样检查的路径有 6 个不同顶点；重复顶点的游走不能通过。

## 已发表构造和当前界限

Lan、Shi、Wang 和 Zhang 对 `n>=9` 证明

`4n/3 - 2 <= sat(n,C6) <= 4n/3 + epsilon^2/2 - 5epsilon/6`，

其中 `epsilon` 是 `n` 模 3 的余数。`n=100` 时 `epsilon=1`，所以整数边数在 132 和 133 之间。论文给出 133 边构造。该界限尚未确定精确值。

论文在 `n=3t+1` 时的构造以 Figure 1(a) 的九点、12 边图 `H` 开始，再加 `t-3` 条 `a_i-b_i-c_i` 路径，并添加 `x_1a_i` 和 `x_2c_i`。最后在 `y_4` 接一个叶子。本配置 `t=33`，因此加 30 条路径和一个叶子。总边数为 `12 + 30*4 + 1 = 133`。

九点核心图从 arXiv v3 PDF 的矢量图解码，并与第 2 节证明中的路径核对。顶点为 `x1,x2,y1,y2,y3,y4,a0,b0,c0`，12 条边在上方英文列出。`human.py` 按定理重建构造。`reference.py` 读取 `data/reference/` 中冻结的 JSON。精确验证确认 133 条边、无简单 C6，且 4817 条非边均有简单五边路径。

上方英文列出了核查日期和来源。检查到的 C6 界限在 `n=100` 时仍相差一条边。任务状态为已通过 Sol 验收（2026-11-06）。
