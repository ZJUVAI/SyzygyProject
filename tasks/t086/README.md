# T086: Duchi 范数在求和内的矩阵比值

## 配置和目标

固定 4 个复 Hermitian 正半定 `3×3` 矩阵 `A1,...,A4`，使用 Schatten 2 范数，也就是 Frobenius 范数。最小化

\[
\frac{\frac1{4^4}\sum_{i_1,i_2,i_3,i_4=1}^4\|A_{i_1}A_{i_2}A_{i_3}A_{i_4}\|_F}
{\frac1{4!}\sum_{(i_1,i_2,i_3,i_4)\in S_4}\|A_{i_1}A_{i_2}A_{i_3}A_{i_4}\|_F}.
\]

分子有 256 个允许重复的有序元组。分母有 24 个不重复索引的有序排列。分母必须为正。此处每项的范数先计算，再取平均；它不同于先把矩阵乘积相加、再对和取范数的 Recht–Ré 问题。

## 来源和开放状态

Duchi 2012 的[评论](https://citeseerx.ist.psu.edu/document?doi=619325d9c18b896b94f4de0bd5be63a749a1f21c&repid=rep1&type=pdf)提出了“乘积的范数在求和内”的版本。AlphaEvolve 论文 [arXiv:2511.02864v1 §6.47](https://arxiv.org/html/2511.02864v1) 将其记为 Problem 6.47，指出 `m≥4` 仍开放，并测试了 `(n,m,d)=(4,4,3)`、Schatten 2 等配置；论文报告没有找到低于 1 的反例。Recht–Ré 的[原问题](https://proceedings.mlr.press/v23/recht12.html)把范数置于求和外。2020 年针对 Recht–Ré 的[反例](https://proceedings.mlr.press/v119/lai20a.html)，以及 2026 Evidence Press 的[低长度 Recht–Ré 候选结果](https://www.evidencepress.org/releases/exact-low-length-recht-re-inequalities/)，均针对另一个“范数在求和外”的命题；不能据此宣称本配置已解决。后者标明为未经同行评审的候选稿，也没有外部独立复验记录。

同参人类基线取 `A1=A2=A3=A4=I3`。每个长度 4 乘积均为 `I3`，两边的 Frobenius 均值相同，分数精确为 1。源论文也明确以所有矩阵取恒等矩阵说明 `C6.47≤1`。此见证重建了传统上界例，不是最优性证明。

## 精确检查和输入格式

每个复数矩阵元素写作 `[实部,虚部]`。分量只能是整数或精确有理数字符串，如 `"-3/7"`；浮点数不接受。检查器精确验证 Hermitian 对称性和全部主子式非负，从而验证 `3×3` Hermitian 矩阵半正定。它使用有理复数乘出所有 280 个矩阵积，以整数平方根构造每个 Frobenius 范数的保守有理区间，再合成比值区间。最小化分数使用区间上端。

只限制候选系数为有理数不会改变下确界。对任意半正定 Hermitian 矩阵 `A`，`A+εI` 正定；正定性在足够小的 Hermitian 扰动下保持，而复有理 Hermitian 矩阵稠密。因此可用有理正定矩阵任意逼近 `A`。目标在分母为正的区域连续；对分母为正的任意输入，足够接近的正定有理矩阵也保持分母为正。因此有理输入上的下确界等于原复半正定域上的下确界。

## 搜索与运行

初始解和人类基线都是四个 `I3`。传统与演化搜索从这个简单起点开始，只在四个正对角矩阵构成的子族中尝试整数对角项；检查器仍接受一般复有理 Hermitian PSD 矩阵。搜索不读取人类或参考文件。

```sh
.venv/bin/python -m tasks.t086.init_program
.venv/bin/python -m tasks.t086.baseline
.venv/bin/python -m tasks.t086.evolution
.venv/bin/python -m tasks.t086.human
.venv/bin/python -m tasks.t086.reference
.venv/bin/python -m pytest tasks/t086 -q
```

默认 seed 为 0，传统搜索 250 步，演化 50 代、6 个体。生成限时 300 秒，验证限时 60 秒，4 GiB、单线程。状态：`accepted_by_sol`。

---

# T086: Duchi's inside-sum matrix ratio

## Configuration and objective

Fix four complex Hermitian positive-semidefinite `3×3` matrices `A1,...,A4` and the Schatten 2 norm, which is the Frobenius norm. Minimize

\[
\frac{\frac1{4^4}\sum_{i_1,i_2,i_3,i_4=1}^4\|A_{i_1}A_{i_2}A_{i_3}A_{i_4}\|_F}
{\frac1{4!}\sum_{(i_1,i_2,i_3,i_4)\in S_4}\|A_{i_1}A_{i_2}A_{i_3}A_{i_4}\|_F}.
\]

The numerator has 256 ordered tuples with repetition. The denominator has 24 ordered permutations of distinct indices. The denominator must be positive. Each product norm is computed before summation. This differs from the Recht–Ré problem, where the norm is outside the sum.

## Source and open status

Duchi's [2012 commentary](https://citeseerx.ist.psu.edu/document?doi=619325d9c18b896b94f4de0bd5be63a749a1f21c&repid=rep1&type=pdf) proposes the version with each product norm inside the sum. AlphaEvolve paper [arXiv:2511.02864v1, §6.47](https://arxiv.org/html/2511.02864v1) calls it Problem 6.47, states that `m>=4` is open, and tests `(n,m,d)=(4,4,3)` with Schatten 2 among other settings. It reports no counterexample below 1. The original [Recht–Ré statement](https://proceedings.mlr.press/v23/recht12.html) places the norm outside the sum. The [2020 Recht–Ré counterexample](https://proceedings.mlr.press/v119/lai20a.html) and the 2026 Evidence Press [low-length Recht–Ré candidate](https://www.evidencepress.org/releases/exact-low-length-recht-re-inequalities/) address that different statement; they do not resolve this task. The latter is marked as an unrefereed candidate and reports no unaffiliated rerun.

The same-parameter human baseline is `A1=A2=A3=A4=I3`. Every length-four product is `I3`, so both Frobenius means agree and the ratio is exactly 1. The cited paper also uses the all-identity choice to show `C6.47<=1`. This reproduces the traditional upper-bound example; it does not prove optimality.

## Exact checking and input format

Each complex matrix entry is `[real,imaginary]`. Components must be integers or exact rational strings such as `"-3/7"`; floating-point input is rejected. The checker verifies Hermitian symmetry and every principal minor exactly. For a `3×3` Hermitian matrix, this certifies positive semidefiniteness. It multiplies all 280 matrix products over rational complex numbers, then uses integer-square-root bounds to enclose each Frobenius norm and the ratio. The upper interval endpoint is returned for minimization.

Restricting candidates to rational entries does not change the infimum. For any Hermitian PSD matrix `A`, `A+εI` is positive definite. Positive definiteness persists under sufficiently small Hermitian perturbations, and complex rational Hermitian matrices are dense. Thus rational positive-definite matrices approximate every PSD matrix. The objective is continuous wherever the denominator is positive, and sufficiently close approximants keep that denominator positive. Therefore both domains have the same infimum.

## Search and commands

The initial solution and human baseline use four identity matrices. Traditional and evolutionary searches start from this simple point and vary integer diagonal entries within the positive diagonal subfamily. The checker accepts general complex rational Hermitian PSD matrices. Search programs do not read comparison files.

```sh
.venv/bin/python -m tasks.t086.init_program
.venv/bin/python -m tasks.t086.baseline
.venv/bin/python -m tasks.t086.evolution
.venv/bin/python -m tasks.t086.human
.venv/bin/python -m tasks.t086.reference
.venv/bin/python -m pytest tasks/t086 -q
```

Defaults use seed 0, 250 baseline steps, 50 evolutionary generations, and population 6. Limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread. Status: `accepted_by_sol`.
