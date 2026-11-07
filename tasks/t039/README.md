# T039：差分三角集

## 中文

### 定义与配置

差分三角集由多行整数标记组成。每行内部形成正差值；所有行的正差值必须互不相同。配置 `T039-C01` 固定为 7 行、每行 6 个互异非负整数。按论文记号这是 `(n,k)=(7,5)`，因为 `k` 表示每行间隔数，标记数为 `k+1`。

目标是最小化所有行内最大正差值。等价地，对每行计算最大标记减最小标记，再取这些跨度的最大值。行内整体平移不改变差值；不同的行可以使用相同标记。评测器精确检查 105 个差值，不读取候选声明的分数。

### 人类与公开基线

Shehadeh、Kingsford 与 Kschischang 的 2026 年论文报告 `(7,5)` 差分三角集上界 112，改进先前的 113。附录列出构造。仓库提交 `2ccff8e767c3fe6390fd3af056dfda11847011fc` 的压缩档案保存在 `data/`，并在 2026-11-06 核对为 GitHub `main` 的当前提交。`human.py` 和 `reference.py` 从固定数据文件重放 7 行、每行 6 个数的见证。见证 SHA-256 为 `9ad412af0b33d51190956b866398bfdd42e6a6e0a894e59f531d28be949e4d1f`。独立评测器确认 105 个差值全部不同，目标值为 112。论文称其来自 FPGA 搜索；论文没有说明是否使用 AI，因此不称为手工构造或无 AI 结果。

Shearer 的 LP 下界为 `M(I,5) ≥ (91I+6)/6`。代入 `I=7` 得 `643/6=107.166...`，所以整数目标至少为 108。与上界 112 合并，区间是 108 至 112，包含五个整数值。论文将 112 报告为上界，不是最优性证明。

冻结对照为 `H=112`，兼容分数为 `H/J`，其中 `J` 是评测器重算出的有效整数目标。分数大于 1 只表示优于此对照。当前没有最优性结论。

### 程序与验证

`init_program.py` 使用不相交的 3 的幂指数构造合法初始集。两个幂的差可写成 `3^a(3^b-1)`。差值中 3 的幂次给出较小指数，除去该幂后可恢复指数间距；单个幂也有唯一的 3-adic 指数。因此，不同的指数区间给出互异差值。该简单构造的跨度很大，仅用于起点。`baseline.py` 从该构造开始，使用固定种子、固定100次随机贪心重启尝试缩小跨度。它不读取对照见证。`evolution.py` 提供搜索入口。

**状态：已通过 Sol 验收（2026-11-06）。**

## English

### Definition and configuration

A difference triangle set is a collection of rows of integer marks. Form positive differences within each row. All such differences across all rows must be distinct. Configuration `T039-C01` has 7 rows and 6 distinct nonnegative integer marks per row. In the paper's notation this is `(n,k)=(7,5)`, since `k` is the number of intervals per row and each row has `k+1` marks.

The objective is to minimize the largest positive within-row difference. Equivalently, find each row's span, `max(mark)-min(mark)`, and minimize the largest span. Translation of a row does not change its differences. Marks may repeat across different rows. The checker evaluates all 105 differences exactly and ignores any score claimed by the candidate.

### Human and public baseline

The 2026 paper by Shehadeh, Kingsford, and Kschischang reports 112 as an upper bound for `(7,5)`, improving the prior value 113. Appendix A lists the construction. The archive for repository commit `2ccff8e767c3fe6390fd3af056dfda11847011fc` is saved in `data/`; on 2026-11-06 this was the current GitHub `main` commit. `human.py` and `reference.py` replay the exact witness: 7 rows of 6 marks. Its SHA-256 is `9ad412af0b33d51190956b866398bfdd42e6a6e0a894e59f531d28be949e4d1f`. The independent checker confirms 105 distinct differences and objective 112. The paper attributes the result to FPGA search. It does not report AI use, so this record is not described as a hand construction or as AI-free.

Shearer's LP bound is `M(I,5) >= (91I+6)/6`. At `I=7`, this is `643/6 = 107.166...`, so the integer objective is at least 108. Together with the upper bound 112, the interval contains five integer values: 108 through 112. The paper reports 112 as an upper bound, not as an optimality proof.

The frozen comparator is `H=112`; the compatibility score is `H/J`, where `J` is the valid integer objective recomputed by the checker. A score above 1 means only that a candidate improves on this comparator. No optimality claim is made.

### Programs and validation

`init_program.py` builds a valid seed from disjoint exponent ranges of powers of three. A difference between two powers has the unique form `3^a(3^b-1)`. Its 3-adic exponent gives the smaller exponent, and division by that power gives the exponent gap. A single power has its own unique 3-adic exponent. Disjoint exponent ranges therefore give distinct differences. This simple construction has a large span and serves only as the starting point. `baseline.py` starts from it and attempts to reduce the span with 100 seeded randomized greedy restarts. It does not read comparison witnesses. `evolution.py` provides the search entry point.

**Status: accepted by Sol on 2026-11-06.**
