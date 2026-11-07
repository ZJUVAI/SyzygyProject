# T072: 32 元正整数的和积集

## 数学目标

选取恰好 32 个互不相同的正整数。元素没有上界。令

\[
A+A=\{a+b:a,b\in A\},\qquad AA=\{ab:a,b\in A\}.
\]

最小化 \(\max(|A+A|,|AA|)\)。有序对和对角项都参与生成；相同结果只计一次。

固定配置为 `T072-C01`。输出为含 `elements` 数组的对象。检查器使用任意精度整数重新计算两个集合大小。

## 人类方法与公开记录

O’Bryant 的论文 arXiv:2411.08139v2 表 2 给出 32 元集合
\(\Psi_{35}^{5}\setminus\{75,81,100\}\)，并报告和集、积集大小均为 154。
论文说明这些表中结果尚未证明最优。论文第 2 节介绍了传统计算搜索方法，主要使用 Mathematica 14，部分步骤使用 Julia 1.10。论文没有讨论生成式 AI 的使用，本任务不对未披露的工作流程作推断。

作者网站的数据文件完整快照有 1,163,592 行，SHA-256 记录在
`data/source/source_notes.json`。论文 v2 报告的旧数据集数量为 1,162,868；两个数字对应不同快照。本任务只保存第 1,005,722 行及其哈希，没有复制完整数据文件。该行经精确复算得到 154 个不同的和及 154 个不同的积。

论文明确说数据集不完整，表中 32 元结果不知是否最优。检查到的 2026 年小基数论文 arXiv:2601.21828 证明的是基数 10 和 11，不涉及本配置的基数 32。因此 154 是已复现的可行值，不是最优性证明。

## 运行

```sh
.venv/bin/python -m tasks.t072.init_program
.venv/bin/python -m tasks.t072.baseline
.venv/bin/python -m tasks.t072.evolution
.venv/bin/python -m tasks.t072.human
.venv/bin/python -m tasks.t072.reference
.venv/bin/python -m pytest tasks/t072 -q
```

默认生成预算为 300 秒，验证预算为 60 秒，内存上限 4 GiB，单线程。传统搜索和演化搜索从简单集合 `{1,...,32}` 开始。它们默认只提议不超过 4096 的搜索值；这是搜索启发式范围，不是任务或检查器的约束。可用 `MATHBENCH_SEARCH_INTEGER_LIMIT` 调整该提议范围。

所有五个程序均实现 `run_code()`。初始程序、传统搜索及演化搜索不读取对照数据。人类和固定参考程序只重放任务目录中的已存见证。当前状态：`accepted_by_sol`。

See the English summary below.

---

# T072: Sum-product sets of 32 positive integers

## Objective

Choose exactly 32 distinct positive integers, with no upper bound on their values. Define

\[
A+A=\{a+b:a,b\in A\},\qquad AA=\{ab:a,b\in A\}.
\]

Minimize \(\max(|A+A|,|AA|)\). Ordered pairs and diagonal pairs are included. Each resulting value is counted once.

The fixed configuration is `T072-C01`. A solution is an object with an `elements` array. The checker recomputes both set sizes with arbitrary-precision integer arithmetic.

## Human method and public record

Table 2 of O’Bryant's paper, arXiv:2411.08139v2, gives the set
\(\Psi_{35}^{5}\setminus\{75,81,100\}\) for cardinality 32. It reports 154 sums and 154 products. The paper states that the table entries are not known to be optimal. Section 2 describes traditional computer searches, mainly with Mathematica 14 and with Julia 1.10 for some speed-critical steps. The checked paper does not discuss generative-AI use, so this task makes no claim about any workflow that it does not report.

The retrieved author-dataset snapshot has 1,163,592 lines. Its SHA-256 is recorded in `data/source/source_notes.json`. The paper's v2 count of 1,162,868 refers to its older snapshot. This task stores only line 1,005,722 and its hash, not the full dataset. Exact recomputation gives 154 distinct sums and 154 distinct products.

The paper says its dataset is incomplete and that its 32-element table entry may not be optimal. The checked 2026 small-set paper, arXiv:2601.21828, proves exact values for cardinalities 10 and 11; it does not settle cardinality 32. Thus 154 is a reproduced feasible value, not an optimality proof.

## Run

```sh
.venv/bin/python -m tasks.t072.init_program
.venv/bin/python -m tasks.t072.baseline
.venv/bin/python -m tasks.t072.evolution
.venv/bin/python -m tasks.t072.human
.venv/bin/python -m tasks.t072.reference
.venv/bin/python -m pytest tasks/t072 -q
```

Default generation and verification limits are 300 and 60 seconds, with 4 GiB memory and one thread. The initial, traditional-search, and evolutionary programs start from the simple set `{1,...,32}` and do not read comparison data. By default, search proposes replacement values up to 4096. This is only a search heuristic; the task and checker have no value bound. Set `MATHBENCH_SEARCH_INTEGER_LIMIT` to change this proposal range.

All five programs expose `run_code()`. Human and fixed-reference programs replay the saved witness. Status: `accepted_by_sol`.
