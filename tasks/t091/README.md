# T091：63 列二元强度 4 正交阵最少行数

## 定义

求最小行数 \(N\)，使得二元正交阵有 63 列、强度 4。对每组 4 列，16 种二进制模式都必须恰好出现 \(N/16\) 次。允许重复行。固定配置 `T091-C01`。

Rao 界为
\[
N\ge 1+\binom{63}{1}+\binom{63}{2}=2017.
\]
强度 4 要求 \(16\mid N\)，所以 \(N\ge2032\)。此界与已知 2048 行构造之间尚有差距。

## 检查方法

每列编码为长度 \(N\) 的整数位集。对 1 至 4 列的每个非空子集，检查按位异或后的 1 数恰为 \(N/2\)。在每个 4 列集合上，这等价于其所有非平凡奇偶特征均平衡；二元 Fourier 反演给出 16 个模式的计数都为 \(N/16\)。检查器会检查 637,392 个奇偶条件。它接受重复行，不会把重复行误判为无效。

## 初始程序、基线与来源

模型起点使用 F₂¹⁴ 上的通用随机贪心法选择 63 个标签，再枚举全部 16384 个线性形式，得到 16384 行且互异的有效阵列。它不读取 BCH 对照。传统搜索独立在 F₂¹³ 上运行相同的通用选择规则，得到 8192 行，并执行固定次数的 16 行删除尝试。


Carlet、Kiss、Nagy 的论文 Remark 5 给出双纠错 BCH 码对偶构造的正交阵。取 \(m=6\) 并删去一列，可重建 4096 行、63 列、强度 4 的正交阵。本任务以这个公式作为人类基线和固定参考，并对全部条件重新计算。论文 Proposition 10 与 Remark 11 给出 Kerdock 构造的 2048 行同参上界；作者明确说最优性尚未确定。该公开见证未在本任务中重建，因此区分为未复现纪录。

- Carlet, Kiss, Nagy, *Simplicity conditions for binary orthogonal arrays*, DOI [10.1007/s10623-022-01105-4](https://doi.org/10.1007/s10623-022-01105-4)。论文副本在 `data/source/`。
- Sloane 的 orthogonal array directory：[neilsloane.com/oadir](https://neilsloane.com/oadir/index.html)。

2026-11-06 检索未发现 63 列同参最优性证明。公开 2048 构造与 2032 下界之间仍有 16 行缺口。

## English

The standalone start uses a generic random-greedy selection of 63 labels in F₂¹⁴ and enumerates all 16384 linear forms. It produces 16384 distinct rows and does not read the BCH comparator. The traditional search independently builds an F₂¹³ array with 8192 rows and tests fixed 16-row deletions.

Find the smallest row count \(N\) for a binary orthogonal array with 63 columns and strength 4. Every 4-column projection must contain each of the 16 binary patterns exactly \(N/16\) times. Duplicate rows are allowed. Configuration `T091-C01` fixes these parameters.

Rao's bound gives \(N\ge2017\). Since \(16\mid N\), the lower bound rounds up to 2032. A public Kerdock construction gives 2048 rows, so the finite optimum is open in the reviewed sources.

The checker packs every column into an N-bit integer and checks all nonempty parity characters on subsets of 1 to 4 columns. Binary Fourier inversion makes these checks equivalent to uniform 4-column pattern counts. It performs 637,392 exact parity checks and allows repeated rows.

The standalone initializer uses a generic random-greedy set of 63 labels in F₂¹⁴ and enumerates all linear forms, producing 16384 distinct rows. The traditional search independently builds an F₂¹³ seed with 8192 rows and tries fixed 16-row deletions. Neither program reads the BCH witness.

The human baseline rebuilds a 4096-row OA from the dual of a double-error-correcting BCH code, as described by Carlet, Kiss, and Nagy. Their paper also reports a 2048-row Kerdock construction and states that optimality is unknown. We do not claim to reproduce that stronger public witness.
