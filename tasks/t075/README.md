# T075：K4⁻-free 三元超图的最大边数

## 目标

在固定顶点集 `{0,…,35}` 上选择尽可能多的三元边。每个四点子集最多含两条所选三元边。这等价于不含由四个顶点及其中任意三条三元边组成的 `K4⁻` 子超图。约束按普通子图定义，不要求诱导子图完全相同。

配置 `T075-C01` 固定 `n=36`、边大小为 3，目标是最大化边数。校验器枚举全部 58,905 个四点子集，并重新计算边数。

## 已知构造与界

Frankl–Füredi 的 `H6` 有 6 个顶点和 10 条边。将顶点分成六个大小为 6 的部分：先按每条 `H6` 边加入跨三部分的全部 `6³` 条边，再在每个部分中放入一个 `H6`。所得构造有 `10×6³+6×10=2,220` 条边。精确见证保存在 `data/human/h6_iterated_blowup_n36.json`；`human.py` 从公开模板独立重建。

Falgas-Ravry、Pikhurko、Vaughan 与 Volec 在 2023 年论文第 6.3 节给出 `H6` 的边集，并说明它的 blow-up 和迭代 blow-up 都是 `K4⁻`-free。该论文还指出普通 `K4⁻` Turán 密度未知，`2/7` 是猜想值。这里的固定 `n=36` 目标是普通有限边数问题。论文中的 codegree 结果及 2026 年关于 `K4^(3)` 完全四面体的 uniform Turán 结果都不等同于本配置。

无需文献即可验证的上界为 3,570：每条三元边属于 33 个四点集，每个四点集至多容纳两条边，所以 `33|E|≤2×C(36,4)`。因此本配置的已核实界为 `2,220≤ex(36,K4⁻)≤3,570`。截至 2026-11-06 的来源检索没有发现将此有限规模上界降至 2,220 的证明；这是一项有范围的来源检索结论。

## 人类基线与搜索

`human.py` 重建上述公开的迭代 `H6` 构造，边数 2,220。原论文没有说明是否使用 AI 工具。

`init_program.py` 返回空超图作为简单冷启动。`baseline.py` 和 `evolution.py` 都从空边集开始，以不同种子随机排列全部三元候选边；若加入该边后没有四点集超过两条边，就接受它们。两者只使用任务规则和顶点标签，不读取人类或参考见证。

`reference.py` 返回冻结的 2,220 边 `H6` 见证。没有发现更强的公开有限 `n=36` 构造或精确最优性证明。

## English summary

Choose as many 3-element edges as possible on the fixed vertex set `{0,…,35}`. Every 4-vertex set may contain at most two selected triples. This forbids `K4^-`, the 3-uniform hypergraph with three triples on four vertices, as an ordinary non-induced subhypergraph.

Configuration `T075-C01` maximizes the edge count for `n=36`. The checker enumerates all 58,905 four-vertex sets and recomputes the edge count.

Frankl and Füredi's `H6` has six vertices and ten edges. Partition the 36 vertices into six sets of size six. For every `H6` edge, add all `6³` cross-part triples; then place one `H6` inside each part. This iterated blow-up has `10×6³+6×10=2,220` edges. The exact witness is saved in `data/reference/`; `human.py` rebuilds it from the public template.

Section 6.3 of the 2023 paper by Falgas-Ravry, Pikhurko, Vaughan, and Volec gives the `H6` edge list and states that its blow-ups and iterated blow-ups are `K4^-`-free. The paper also states that the ordinary `K4^-` Turán density is unknown and conjectured to be `2/7`. The finite `n=36` task is the ordinary edge-count problem. Its result is distinct from codegree results and from the 2026 uniform Turán result for the complete tetrahedron `K4^(3)`.

A direct double count gives the verified upper bound 3,570: each triple lies in 33 four-sets, and each four-set contains at most two selected triples, so `33|E|≤2×C(36,4)`. The verified range is `2,220≤ex(36,K4^-)≤3,570`. The source review through 2026-11-06 found no proof closing this finite gap. This is a bounded literature review, not an exhaustive claim.

`human.py` rebuilds the published iterated `H6` construction and obtains 2,220 edges. The paper does not state whether AI tools were used. `init_program.py` returns the empty hypergraph. The baseline and evolution programs start from the empty set and use seeded random greedy additions. They read no human or reference witness. `reference.py` returns the frozen 2,220-edge witness.
