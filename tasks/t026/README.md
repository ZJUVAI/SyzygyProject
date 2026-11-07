# T026：六色 Schur 下界染色

## 中文

### 定义与配置

给正整数的连续前缀 `[1,N]` 使用至多六种颜色。若不存在同色的 `x`、`y` 和 `x+y`，则染色有效。允许 `x=y`；因此也检查 `2x=z`。目标是最大化有效前缀长度 `N`。成绩只表示 `S(6) ≥ N`，不表示 Schur 数已经确定。

配置 `T026-C01` 固定颜色数上限为 6。候选 JSON 可用颜色数组 `{"n": N, "colors": [c_1, ..., c_N]}`，位置 `i` 对应整数 `i`，颜色标签为 0 至 5；也可用互不重叠的颜色类 `{"n": N, "classes": [[...], ...]}`。第二种格式必须恰好覆盖 `[1,N]`。检查器拒绝空缺、越界、重复的类成员、布尔数、非整数颜色、NaN、无穷大和任何同色 Schur 三元组。检查器不读取候选声明的分数。

### 人类基线与公开结果

Fredricksen 与 Sweet 在 2000 年论文中列出 `[1,536]` 的六色对称无和分区。`human.py` 按论文列出的半集及模 537 配对规则重建完整颜色数组。论文允许特殊元素 179 与 358 异色。本地检查器逐项复算分区覆盖，并精确检查所有 `x ≤ y`，包括 `x=y`。该人类对照为 536。

Chen、Zhu 与 Long 于 2026-10-22 发布 arXiv v1，给出 `[1,537]` 的六色分区。仓库主证书从公开仓库固定提交 `92a9d5f1336a5a064b2bfe6597d967f59191e365` 获取，且 SHA-256 与该提交中的 `SHA256SUMS` 相同。`reference.py` 重放证书；本任务自己的检查器重新计算成绩。论文说明这些分区由搜索找到，但没有披露是否使用 AI 或大语言模型，所以来源标为未披露。该预印本明确不声称 `S(6)` 精确值或 538 不可染色。查验日期为 2026-11-06。

兼容分数冻结为 `J/H`，其中 `J` 是重新计算的有效 `N`，`H=536` 是复现的人类对照。分数大于 1 只表示超过冻结对照。它不表示突破 537 的公开结果，更不表示证明了精确值。

### 程序与验证

`init_program.py` 返回一个简单的四项有效染色，不读取参考数据。`baseline.py` 用固定随机种子执行有界的随机贪心扩展，并记录步数、重启数和预算。`human.py` 重建人类基线。`reference.py` 只重放固定的 537 公开证书。

**状态：已通过 Sol 验收（2026-11-06）。** 精确 Schur 数是否为 537 或更大仍未解决；本任务只验收下界构造。

## English

### Definition and configuration

Color a consecutive prefix `[1,N]` of the positive integers with at most six colors. A coloring is valid when no same-color `x`, `y`, and `x+y` exist. The terms may be equal, so the checker also tests `2x=z`. The objective is to maximize the valid prefix length `N`. A result gives only the lower bound `S(6) ≥ N`; it does not determine the Schur number.

Configuration `T026-C01` fixes an upper limit of six colors. A candidate may use the color-array form `{"n": N, "colors": [c_1, ..., c_N]}`, where position `i` gives the color of integer `i` and labels are 0 through 5. It may also use disjoint color classes: `{"n": N, "classes": [[...], ...]}`. The classes must cover `[1,N]` exactly. The checker rejects gaps, out-of-range values, duplicate class members, booleans, non-integer colors, NaN, infinity, and every monochromatic Schur triple. It ignores any score claimed by the candidate.

### Human baseline and public result

Fredricksen and Sweet list a six-color symmetric sum-free partition of `[1,536]` in their 2000 paper. `human.py` rebuilds the full coloring from the listed half-sets and the paper's pairing rule modulo 537. The paper allows the exceptional elements 179 and 358 to have different colors. The local checker recomputes exact coverage and checks every pair `x ≤ y`, including `x=y`. This is the human baseline at 536.

Chen, Zhu, and Long posted arXiv v1 on 2026-10-22 with a six-color partition of `[1,537]`. The public main certificate is pinned to repository commit `92a9d5f1336a5a064b2bfe6597d967f59191e365`; its SHA-256 matches that commit's `SHA256SUMS`. `reference.py` replays the certificate, and this task's checker independently recomputes its score. The paper says the partitions were found by search but does not disclose AI or LLM use, so their provenance is recorded as undisclosed. The preprint does not claim the exact value of `S(6)` or impossibility at 538. Checked on 2026-11-06.

The frozen compatibility score is `J/H`, where `J` is the recomputed valid `N` and `H=536` is the reproduced human reference. A score above 1 means only that the construction exceeds the frozen comparator. It does not mean that it exceeds the public 537 result or proves the exact value.

### Programs and validation

`init_program.py` returns a simple valid coloring of length four and does not read reference data. `baseline.py` performs seeded, bounded randomized greedy extension and records its steps, restarts, and budget. `human.py` rebuilds the human baseline. `reference.py` replays only the pinned public 537 certificate.

**Status: accepted by Sol on 2026-11-06.** The exact value of `S(6)` remains unresolved; this task scores lower-bound constructions only.
