# T078: Minimum determinant for a 10-dimensional lattice

## Definition

Choose a symmetric positive definite 10×10 Gram matrix `G` with
exact rational entries. Require

\[
z^T G z \ge 4\qquad\text{for every }z\in\mathbb Z^{10}\setminus\{0\}.
\]

Minimize `det(G)`. The entries are exact integers or rational strings such as
`"3/2"`. Floating-point entries are rejected. A Gram matrix with minimum
squared norm 4 gives a lattice packing with sphere radius 1; its fundamental
volume is `sqrt(det(G))`. Minimizing the determinant is therefore the same
fixed-scale lattice-packing objective.

This task is restricted to lattice packings represented by a Gram matrix. It
does not optimize over arbitrary packings. Cohn and Kumar reported in 2009
that the nonlattice packing `P_10c` was denser than known lattice packings in
dimension 10.

The rational input domain does not remove an optimum. A densest lattice is an
extreme form, hence perfect by Voronoi's criterion. Its minimal vectors satisfy
linear equations `z^T G z = 4` with integer coefficients. Perfection means
these equations determine the form, so the unique solution has rational
entries. The 2026 dimension-9 Voronoi enumeration states this finite perfect
form principle and closes dimension 9; it does not close dimension 10.

## Exact checker

The checker parses rational values without a coefficient cap. It verifies
symmetry and positive definiteness with exact LDL decomposition. It then
enumerates every integer vector with squared norm below 4. The LDL ellipsoid
gives each coordinate range from exact rational bounds. The search uses no
fixed coordinate box. It rejects a form as soon as it finds a nonzero vector
with norm below 4. The determinant is the exact product of the LDL diagonal
entries. Large or highly skewed forms may use the full verification budget;
the runner reports a timeout instead of treating a partial search as a proof.

## Public and human construction

Gabriele Nebe and Neil J. A. Sloane's [LAMBDA10 catalogue entry](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/LAMBDA10.html)
lists a 10-dimensional Gram matrix with determinant 768, minimum norm 4, and
kissing number 336. The raw HTML was downloaded on 2026-11-06 and frozen at
`data/source/lambda10.html` (SHA-256
`10a1fa86d38c92c30d4df0f95169d0fee64e3584bc7316e35b19d0c325229c1a`).
`human.py` rebuilds the matrix from its `GRAM` section. `reference.py` reads a
separate frozen transcription. Both return the same exact public lattice.

Independent exact enumeration finds 336 nonzero vectors with norm at most 4;
all have norm exactly 4. The local shortest-vector list is in
`data/human/lambda10_minimal_vectors.json`. It supports the kissing-number
check, while the checker independently establishes that no shorter vector
exists.

The exact dimension-10 optimum is open in sources checked on 2026-11-06. The
2026 paper [The lattice packing problem in dimension 9 by Voronoi's
algorithm](https://arxiv.org/html/2508.20719v2) proves the dimension-9 case.
A SIAM paper on dense generic lattices reports exact Hermite constants only
through dimensions 1–8 and 24. The old 2009 Cohn-Kumar paper also identifies
dimension 10 as unsettled at that time; it is retained as historical context,
not used alone as current evidence. Thus 768 is recorded as a feasible public
upper bound, not a proven minimum.

## Programs and search

The simple start is `4I`, with determinant 1,048,576. The traditional baseline
searches a fixed 32 seeded trials among scaled Cartan Gram forms for `A10`,
`D10`, and `E8+A2`, plus `4I`. These root-system candidates have minimum squared
norm 4 by construction. The seed-0 run returns the `E8+A2` form with
determinant 3,072. The search code reads no human or reference asset.

## Sources

- [LAMBDA10 catalogue entry](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/LAMBDA10.html), source matrix and reported determinant, minimum norm, and kissing number.
- Dutour Sikirić and van Woerden, [The lattice packing problem in dimension 9 by Voronoi's algorithm](https://arxiv.org/abs/2508.20719), v2 dated 2026-02-07.
- Dutour Sikirić et al., [Dense Generic Well-Rounded Lattices](https://epubs.siam.org/doi/10.1137/22M1532779), discussion of known exact Hermite constants.
- Cohn and Kumar, [Optimality and uniqueness of the Leech lattice among lattices](https://annals.math.princeton.edu/wp-content/uploads/annals-v170-n3-p01-p.pdf), 2009, §1, historical status of dimension 10.

Run the task tests with:

```sh
.venv/bin/python -m pytest tasks/t078/test_task.py -q
```

Status: accepted by Sol on 2026-11-06.

---

# T078：十维格的最小 Gram 行列式

## 定义

选择一个对称正定的 10×10 Gram 矩阵 (G)，矩阵元素为精确有理数。要求

\[
z^T G z \ge 4\qquad\text{对每个 }z\in\mathbb Z^{10}\setminus\{0\}.
\]

目标是最小化 `det(G)`。矩阵元素使用整数或有理数字符串，例如 `"3/2"`。检查器拒绝浮点数。最短向量平方长度为 4 时，格球半径为 1，基本胞体积为 `sqrt(det(G))`，所以最小化行列式等于固定尺度下的格点堆积目标。

本题只比较由 Gram 矩阵表示的格堆积，不优化所有球心配置。Cohn 与 Kumar 在 2009 年记载，十维非格堆积 `P_10c` 的密度高于当时已知的格堆积。

有理数输入不会排除最优格。最优格是 Voronoi 意义下的极值形式，因此是 perfect form。最短向量满足 `z^T G z = 4`，这是关于矩阵元素、系数为整数的线性方程。Perfect 性质保证这些方程唯一确定 Gram 矩阵，因此解为有理数。2026 年的九维 Voronoi 枚举论文陈述了有限 perfect-form 方法，并证明九维情形；它没有证明十维情形。

## 精确检查

检查器不限制有理数系数大小。它以精确 LDL 分解检查对称性和正定性，再枚举所有平方长度小于 4 的整数向量。每个坐标范围都由精确有理数椭球界导出。算法没有固定坐标盒。发现短于 4 的非零向量后立即拒绝。行列式由 LDL 对角元素的乘积精确计算。极端倾斜的矩阵可能耗尽验证预算；运行器会报告超时，不会把未完成的枚举当成证明。

## 公开构造与人类基线

Gabriele Nebe 与 Neil J. A. Sloane 的 [LAMBDA10 目录页](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/LAMBDA10.html)列出一个十维 Gram 矩阵，行列式为 768，最小范数为 4，紧密数为 336。原始 HTML 于 2026-11-06 下载并保存在 `data/source/lambda10.html`，SHA-256 为 `10a1fa86d38c92c30d4df0f95169d0fee64e3584bc7316e35b19d0c325229c1a`。`human.py` 从原页 `GRAM` 部分重建矩阵。`reference.py` 从单独冻结的转录文件读取矩阵。两个入口返回同一个公开格。

独立精确枚举得到 336 个范数不超过 4 的非零向量，且它们的范数全为 4。本地最短向量表在 `data/human/lambda10_minimal_vectors.json`。该表复核紧密数；主检查器会独立证明没有更短向量。

截至 2026-11-06 所查来源，十维精确最优值仍未闭合。2026 年的[九维 Voronoi 算法论文](https://arxiv.org/html/2508.20719v2)证明了九维结果。SIAM 的格点论文称精确 Hermite 常数已知于维数 1–8 和 24。Cohn-Kumar 2009 年论文也将十维列为当时未解；这里只把它作为历史材料，不单独用来证明当前状态。因此 768 记录为公开可行上界，不称为已证明最小值。

## 程序和搜索

简单起点为 `4I`，行列式 1,048,576。传统基线在固定 32 次带种子的搜索中枚举缩放后的 `A10`、`D10`、`E8+A2` Cartan 矩阵和 `4I`。这些根格候选按构造有最小平方范数 4。种子 0 返回 `E8+A2`，行列式为 3,072。搜索代码不读取人类或参考见证。

## 来源

- [LAMBDA10 格目录](https://www.math.rwth-aachen.de/~Gabriele.Nebe/LATTICES/LAMBDA10.html)：矩阵、行列式、最小范数和紧密数。
- Dutour Sikirić 与 van Woerden，[九维 Voronoi 格点堆积论文](https://arxiv.org/abs/2508.20719)，v2 日期为 2026-02-07。
- Dutour Sikirić 等，[Dense Generic Well-Rounded Lattices](https://epubs.siam.org/doi/10.1137/22M1532779)：已知 Hermite 常数范围的讨论。
- Cohn 与 Kumar，[Leech 格的最优性和唯一性](https://annals.math.princeton.edu/wp-content/uploads/annals-v170-n3-p01-p.pdf)，2009 年，第 1 节；用于十维问题的历史背景。

运行测试：

```sh
.venv/bin/python -m pytest tasks/t078/test_task.py -q
```

状态：已通过 Sol 验收（2026-11-06）。
