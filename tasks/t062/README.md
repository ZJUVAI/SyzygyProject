# T062: Square-difference-free subset of [42025]

## Definition

Choose a set `B` contained in `{1,...,42025}`. For every two different elements `x,y` in `B`, require `|x-y|` not to be a positive perfect square. Maximize `|B|`. The fixed configuration is `T062-C01`.

The candidate format is `{"elements": [integer, ...]}`. The checker rejects duplicates, booleans, non-integers, and values outside the interval. It checks every possible square translation with exact integer arithmetic.

## Human construction and finite status

Mark Lewko's 2015 paper gives the 12 residues

`A = {7,21,50,64,76,83,106,120,139,182,193,199} (mod 205)`.

For this configuration, rebuild

`B = {1 + a + 205 b : a in A, 0 <= b < 205}`.

This produces 2460 elements from 8 through 42020. The modulus `205=5*41` is square-free. If two members use different residues, their difference modulo 205 is not a square residue, as checked from Lewko's table. If they use the same residue, their nonzero difference is `205(b-b')`, has absolute value below `205^2`, and cannot be a square: square-freeness of 205 would force a square multiple of 205 to be divisible by `205^2`.

The value 2460 is a verified feasible lower bound at this N. It is reconstructed from the published formula; Lewko's paper proves an asymptotic lower bound and does not state that 2460 is the exact finite optimum. Dean et al. report exact computation of `D(S,N)` through `N=300`; the OEIS entry also links a table through 410. We found no exact value for `N=42025` in the sources checked on 2026-11-06. This finite-parameter status is limited to those checked sources.

The 2026 literature improves asymptotic lower-bound exponents. Krachun's August 2026 preprint gives exponent `0.7527964558...`; Naslund's October 2026 computer-assisted preprint gives `0.7580758318008816...-o(1)`. These statements concern growth as N increases and do not give the exact optimum at `N=42025`.

Lewko's separate 14-residue construction modulo 91 concerns cube differences. It is not used for this square-difference configuration.

## Sources

- Mark Lewko, [An improved lower bound related to the Furstenberg-Sárközy theorem](https://doi.org/10.37236/4656), *Electronic Journal of Combinatorics* 22(1), 2015, Theorem 3 and Section 3.
- Christian Dean et al., [Notes and Computations on Forbidden Differences](https://alexricemath.com/wp-content/uploads/2025/08/ForbiddenDifferencesPaper4.pdf), abstract and Section 4; exact `D(S,N)` computations through `N<=300`.
- [OEIS A100719](https://oeis.org/A100719), definition of the finite maximum and linked table through `N=410`.
- Dmitry Krachun, [Square-Difference-Free Sets beyond the Three-Quarter Barrier](https://arxiv.org/abs/2608.01325), arXiv:2608.01325v1, 2026-08-02.
- Eric Naslund, [Square-difference-free sets of exponent 0.7580758](https://hexagonmath.org/search?advanced=1&subject=math.NT), hexagon:2610.00151v1, October 2026.

## Reproduction

Run the five entries with `MATHBENCH_CONFIG_ID=T062-C01`. Run the checker tests with:

```sh
.venv/bin/python -m pytest tasks/t062/test_task.py -q
```

The fixed reference witness is stored in `data/reference/`. The initial seed and greedy search do not read that file.

---

# T062：区间 [42025] 中的平方差自由子集

## 定义

选择 `{1,...,42025}` 的子集 `B`。任意两个不同元素 `x,y` 均须满足 `|x-y|` 不是正平方数。目标是最大化 `|B|`。固定配置为 `T062-C01`。

候选程序返回 `{"elements": [整数, ...]}`。检查器拒绝重复值、布尔值、非整数和区间外的值，并用整数运算检查所有平方位移。

## 人类构造与有限参数状态

Mark Lewko 2015 年论文给出模 205 的 12 个剩余类：

`A = {7,21,50,64,76,83,106,120,139,182,193,199}`。

对本配置展开为

`B = {1 + a + 205 b : a 属于 A，0 <= b < 205}`。

该构造有 2460 个元素，范围为 8 到 42020。模数 `205=5*41` 无平方因子。若两个元素来自不同剩余类，Lewko 的表证明其模 205 的差不是平方剩余。若来自同一剩余类，非零差为 `205(b-b')`，绝对值小于 `205^2`；若它是平方，205 无平方因子会推出差被 `205^2` 整除，矛盾。

2460 是该固定参数下经过验证的可行下界，来源是已发表公式的有限展开。Lewko 论文证明渐近下界，没有声称 2460 等于该有限参数的最优值。Dean 等人报告的精确计算覆盖 `N<=300`；OEIS 页面还链接到截至 410 的表。截至 2026-11-06 检查的来源中，没有找到 `N=42025` 的精确最优值。此状态仅限于已检查的来源。

2026 年文献改进了渐近下界指数。Krachun 2026 年 8 月预印本给出 `0.7527964558...`；Naslund 2026 年 10 月计算机辅助预印本给出 `0.7580758318008816...-o(1)`。这些结果描述 N 增大时的渐近增长，没有给出 `N=42025` 的精确最优值。

Lewko 另一个模 91 的 14 剩余类构造讨论的是立方差。本任务不使用它。

## 来源

- Mark Lewko，[An improved lower bound related to the Furstenberg-Sárközy theorem](https://doi.org/10.37236/4656)，*Electronic Journal of Combinatorics* 22(1)，2015，定理 3 和第 3 节。
- Christian Dean 等，[Notes and Computations on Forbidden Differences](https://alexricemath.com/wp-content/uploads/2025/08/ForbiddenDifferencesPaper4.pdf)，摘要和第 4 节；`D(S,N)` 精确计算到 `N<=300`。
- [OEIS A100719](https://oeis.org/A100719)，有限最大值定义，并链接到 `N=410` 的表。
- Dmitry Krachun，[Square-Difference-Free Sets beyond the Three-Quarter Barrier](https://arxiv.org/abs/2608.01325)，arXiv:2608.01325v1，2026-08-02。
- Eric Naslund，[Square-difference-free sets of exponent 0.7580758](https://hexagonmath.org/search?advanced=1&subject=math.NT)，hexagon:2610.00151v1，2026 年 10 月。

## 复现

五个程序均使用 `MATHBENCH_CONFIG_ID=T062-C01`。测试命令：

```sh
.venv/bin/python -m pytest tasks/t062/test_task.py -q
```

冻结参考见证保存在 `data/reference/`。简单起点和贪心搜索不读取该文件。
