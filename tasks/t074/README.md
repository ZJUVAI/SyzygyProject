# T074: 自由凸域的 12 点 Heilbronn 问题

## 数学目标

在平面上选取恰好 12 个互不相同的有理点，且任意三点不共线。坐标没有范围限制，也没有固定外容器。目标是最大化

\[
\frac{\text{所有三点三角形中的最小面积}}{\text{12 点凸包面积}}.
\]

该比值不随整体平移、旋转或缩放变化。任务固定为 `T074-C01`。检查器使用精确有理数，验证全部 220 个三点组合，并用精确单调链算法计算凸包面积。

## 有理数与实数配置

正式输入使用任意大小的有理坐标。这个选择保留了与实坐标连续问题相同的上确界。对任一可行实数配置，220 个三角形面积都严格为正。足够小的坐标扰动仍保持每个行列式非零。可以用有理数逐点逼近原坐标；三角形面积、凸包面积和它们的比值连续变化。因此有理配置在所有可行实配置中稠密，实数配置的上确界等于有理配置的上确界。该论证不表示任一实数最优配置本身一定具有有理坐标。

## 公开记录及重建链

当前记录档案页列出自由凸域、12 点的值为 `2/51`，并把发现归于 David Cantrell，日期为 2007 年 6 月。档案说明此项在 2026 年由后来提交的坐标资料重新核验；来源记录提到一份 2007 Mathematica notebook，于 2026 年 9 月收到。我们不把下述有理点称为 Cantrell 的原始坐标。

本任务保存档案中的原始十进制 JSON 及 SHA-256。`human.py` 将这些十进制字面值按精确十进制有理数读取，把前三点仿射归一化到 `(0,0),(1,0),(0,1)`，再将各坐标重构为分母不超过 100 的有理数。重建结果另存为参考见证，并由本任务检查器精确复核，得到最小三角形面积 `1/4`、凸包面积 `51/8`、比值 `2/51`。所以公开分数、档案重建和本地有理数重建的来源步骤彼此可区分。

档案当前将 `2/51` 列为 12 点自由凸域记录。检查到的页面没有给出该参数的最优性证明。它是已复现的可行记录，不是最优性证明。档案所列 2026 年自由凸域 `n=3…8` 证明不涉及 `n=12`。

## 运行

```sh
.venv/bin/python -m tasks.t074.init_program
.venv/bin/python -m tasks.t074.baseline
.venv/bin/python -m tasks.t074.evolution
.venv/bin/python -m tasks.t074.human
.venv/bin/python -m tasks.t074.reference
.venv/bin/python -m pytest tasks/t074 -q
```

初始程序返回抛物线上的 `(i,i²)` 点，`i=0,…,11`。传统搜索和演化搜索从同一简单起点开始，只自行尝试整数坐标替换，不读取记录数据。搜索默认在 `[-40,40]` 内提议替换坐标；这是搜索策略范围，不是任务约束。检查器不限制坐标范围或分母。

全部五个程序都实现 `run_code()`。默认生成预算为 300 秒，验证预算为 60 秒，内存上限 4 GiB，单线程。当前状态：`accepted_by_sol`。

---

# T074: Free-convex-domain Heilbronn problem for 12 points

## Objective

Choose exactly 12 distinct rational points in the plane, with no three collinear. Coordinates have no bounds and there is no fixed outer container. Maximize

\[
\frac{\text{smallest area of a triangle formed by three points}}{\text{area of the convex hull of all points}}.
\]

The ratio is invariant under translation, rotation, and uniform scaling. The fixed configuration is `T074-C01`. The checker uses exact rational arithmetic, tests all 220 triples, and computes the convex hull with an exact monotone-chain algorithm.

## Rational and real configurations

Inputs use rational coordinates of any size. The supremum is the same as over real configurations. In any feasible real configuration, every one of its 220 triangle determinants is nonzero. A sufficiently small perturbation preserves all these nonzero determinants. Rational coordinates are dense, and the triangle areas, convex-hull area, and ratio vary continuously under such perturbations. Thus rational configurations are dense in the feasible real configurations, and both suprema agree. This does not imply that every real maximizer has rational coordinates.

## Public record and reconstruction chain

The current record archive lists `2/51` for the 12-point free-convex problem and credits David Cantrell, June 2007. The archive says that coordinate material was re-verified later; its source note refers to a 2007 Mathematica notebook received in September 2026. We do not label the rational points below as Cantrell's original coordinates.

This task stores the archived decimal JSON and its SHA-256. `human.py` reads those decimal literals as exact decimal rationals, applies an affine normalization that maps the first three points to `(0,0),(1,0),(0,1)`, and reconstructs each coordinate as a rational with denominator at most 100. The resulting points are stored separately as the fixed reference witness and checked exactly: the smallest triangle area is `1/4`, the convex-hull area is `51/8`, and the ratio is `2/51`. The reported value, archive reconstruction, and local rational reconstruction remain distinct steps in the provenance record.

The current archive lists `2/51` as its n=12 free-convex record. The checked page gives no proof of optimality for this parameter. This is a reproduced feasible record, not an optimality proof. The archive's 2026 proofs for free-convex n=3 through n=8 do not settle n=12.

## Run

```sh
.venv/bin/python -m tasks.t074.init_program
.venv/bin/python -m tasks.t074.baseline
.venv/bin/python -m tasks.t074.evolution
.venv/bin/python -m tasks.t074.human
.venv/bin/python -m tasks.t074.reference
.venv/bin/python -m pytest tasks/t074 -q
```

The initial program returns `(i,i²)` for `i=0,...,11`. Traditional and evolutionary search start from this simple seed and try their own integer-coordinate replacements; they do not read comparison data. By default, search proposes replacement coordinates in `[-40,40]`. This is a search strategy range, not a task constraint. The checker has no coordinate or denominator bound.

All five programs expose `run_code()`. Default generation and verification limits are 300 and 60 seconds, with 4 GiB memory and one thread. Status: `accepted_by_sol`.
