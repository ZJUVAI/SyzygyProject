# T100：固定规模图的最少三角形

## English

The graph has the fixed vertex set `0,...,49` and exactly 700 distinct undirected edges. It has no loops. The objective is to minimize its number of triangles. The checker considers every simple graph on these vertices. It does not restrict candidates to a multipartite family.

Liu, Pikhurko, and Staden define a construction `H*` for each `(n,e)` in Definition 1.1 of their 2020 paper. At `(50,700)`, it has part sizes `(23,23,4)`. The complete tripartite graph has 713 edges and 2,116 triangles. Remove 13 edges from one vertex in the part of size 4 to distinct vertices in one part of size 23. This leaves 700 edges and `2,116 - 13*23 = 1,817` triangles. The published construction is a feasible upper bound. It is not a proof of the finite optimum.

The 2020 theorem proves the conjectured answer for sufficiently large `n` in its stated density range, with an unspecified threshold. It does not certify this `n=50` instance. The authors state the all-finite claim as Conjecture 1.11. The current problem-pack snapshot also labels this row “no; conjectured.” The later Liu–Pikhurko note (arXiv v2 last revised 2024-10-07; journal version 2025) discusses the amended conjecture for clique sizes `r>=4`; it does not settle this triangle instance. Searches checked on 2026-11-07 found no fixed-parameter proof for `(50,700)`. This is a bounded source check, not proof that no result exists.

The asymptotic density theorem and blow-up bound give `g_3(50,700) >= 49000/27`, so integrality gives a lower bound of 1,815. This leaves a gap of two below the 1,817 construction. Near-Mantel supersaturation does not close it: the excess above Mantel is 75, while its quoted range requires `q < n/2 = 25`.

The frozen reference is an exact local reconstruction of the published `H*` formula. The input problem pack supplied the parameter row and its status; its API snapshot is stored under the ignored `runs/` directory with a SHA-256 hash. The witness itself is generated from the paper's formula and checked locally.

## 中文

图的顶点固定为 `0,...,49`，并且恰有 700 条不同的无向边。图中没有自环。目标是最小化三角形数量。检查器接受这些顶点上的任意简单图，不限制为完全多部图。

Liu、Pikhurko 和 Staden 在 2020 年论文定义 1.1 中为每个 `(n,e)` 给出构造 `H*`。在 `(50,700)` 时，三部大小为 `(23,23,4)`。对应的完全三部图有 713 条边和 2,116 个三角形。从大小为 4 的一部中取一个顶点，删除它与大小为 23 的一部中 13 个不同顶点相连的边。所得图有 700 条边和 `2,116 - 13*23 = 1,817` 个三角形。论文构造给出可行上界，不能证明该有限参数的最优值。

2020 年论文的定理只在其指定密度范围内、对充分大的 `n` 证明猜想答案，门槛没有给出。它不自动证明 `n=50`。作者把所有有限参数的结论列为猜想 1.11。当前问题包快照也将这一行标为“no; conjectured”。Liu 和 Pikhurko 后续论文的 arXiv v2 最后修订于 2024-10-07，期刊版发表于 2025 年；该文讨论 `r>=4` 的修订猜想，没有解决本三角形配置。截至 2026-11-07 的来源核查没有找到 `(50,700)` 的固定参数证明。这是有限来源范围的核查，不等于证明不存在其他结果。

渐近密度定理及其放大下界给出 `g_3(50,700) >= 49000/27`，由整数性得到下界 1,815。与 1,817 的构造相差 2。近 Mantel 超饱和定理不能闭合此差距：超过 Mantel 界的边数为 75，而引用定理要求 `q < n/2 = 25`。

冻结参考是按论文 `H*` 公式精确重建的构造。输入问题包提供了参数行及其状态。API 快照及 SHA-256 保存在忽略的 `runs/` 目录中。见证由论文公式生成，并由本地检查器复核。

## 运行

```sh
.venv/bin/python -m pytest tasks/t100/test_task.py -q
.venv/bin/python -m json.tool tasks/t100/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t100/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t100/records.json > /dev/null
```
