# T081: Twelve planar points with a small distance spread

## Definition

Choose 12 distinct points in `R²`. For each pair, compute the squared
Euclidean distance. Minimize

\[
J(P)=\frac{\max_{i<j}\|p_i-p_j\|^2}
           {\min_{i<j}\|p_i-p_j\|^2}.
\]

This is the square of the maximum-to-minimum distance ratio used by Friedman.
The square is monotone, and the source reports `r²` directly. The input uses
exact rational coordinates without a bounding box. It has no non-collinearity
constraint.

Rational coordinates preserve the infimum over all real configurations. For
any 12 distinct real points, the minimum distance is positive, and the ratio
is continuous in the coordinates near that configuration. Rational points are
dense in `R²`, so rational configurations approximate every real score
arbitrarily closely. Thus the rational search domain has the same infimum as
the full real-plane problem, even if an irrational configuration attains the
infimum while no rational configuration does.

The checker accepts integer or fraction-string coordinates, such as `"3/2"`.
It rejects floats, duplicate points, and malformed coordinates. It computes
all 66 squared distances with exact fractions. It imposes no coordinate or
coefficient bound.

## Public construction and exact reconstruction

Friedman's [max/min distance page](https://erich-friedman.github.io/packing/maxmin/)
lists, for `n=12`, the smallest known squared ratio
`5 + 2√3 = 8.464...`, credited to Ingo Rechenberg (2006). The page gives a
diagram, not coordinate strings. The diagram is frozen as `data/source/mm12.gif`;
the page HTML is `data/source/index.html`.

An independent exact reconstruction of that diagram uses `r=√3` and the
following points, in order:

```text
(0,0), (1,0), (1/2,r/2), (1/2,1+r/2),
(1/2-r/2,1/2+r/2), (1/2+r/2,1/2+r/2),
(-r/2,1/2), (-r/2,-1/2), (0,-1), (1,-1),
(1+r/2,-1/2), (1+r/2,1/2).
```

Exact arithmetic in `Q(√3)` verifies that the minimum squared distance is 1,
the maximum is `5+2√3`, and 21 pairs attain the minimum. This proves the
score of the reconstructed algebraic pattern. The local rational witness
substitutes

```text
r = floor(10^63 √3) / 10^63
```

where the floor is computed by `isqrt(3·10^126)`. The checker reports its full
exact rational objective separately. That rational score is slightly larger
than `5+2√3`, so the reference is conservative and the local coordinate list
is not presented as Rechenberg's original coordinate file. The frozen
`human_reference` is the positive JSON number `8.464101615137755`, rounded up
from the exact rational reconstruction for the compatibility score.

The 2026-11-06 Friedman page still lists the same n=12 value. AlphaEvolve's
[2025 paper, Problem 6.50](https://arxiv.org/html/2511.02864v1) lists exact
values through n=8 and describes later entries for n=9–30 as numerical
candidates. The n=12 value is a feasible reported upper bound; its optimality
is not proved in the sources checked.

## Programs and search

The simple initial program returns a 4 by 3 integer grid, with exact objective
13. The traditional baseline runs a fixed seeded simulated-annealing search
on a rational grid with denominator 64. It changes one coordinate at a time
and tracks the best exact ratio. It reads no human or reference data. The
seed-0 run and exact result are saved under `best/`.

## Sources

- Erich Friedman, [Minimizing the Ratio of Maximum to Minimum Distance](https://erich-friedman.github.io/packing/maxmin/), n=12 entry and diagram; page credits Rechenberg (2006).
- Ingo Rechenberg, “Point configurations with minimal distance ratio,” 2006, cited as reference [237] in the [AlphaEvolve paper](https://arxiv.org/html/2511.02864v1).
- Georgiev, Gómez-Serrano, Tao, and Wagner, [Mathematical exploration and discovery at scale](https://arxiv.org/abs/2511.02864), v1, Problem 6.50.

Run tests with:

```sh
.venv/bin/python -m pytest tasks/t081/test_task.py -q
```

Status: accepted by Sol on 2026-11-06.

---

# T081：十二个平面点的最大/最小距离比

## 定义

选择 `R²` 中 12 个互异点。计算每一对点的欧氏距离平方，并最小化

\[
J(P)=\frac{\max_{i<j}\|p_i-p_j\|^2}
           {\min_{i<j}\|p_i-p_j\|^2}.
\]

这是 Friedman 使用的最大距离/最小距离比的平方。平方函数保持大小顺序，来源页面也直接报告 `r²`。输入坐标为精确有理数，不设容器边界，也不限制共线。

有理坐标与任意实坐标的下确界相同。对任意 12 个互异实点，最小距离为正，且目标在该点组附近连续。有理点在 `R²` 中稠密，所以可用有理点组任意逼近实数构形的目标值。因此有理搜索域保留整个实平面问题的下确界。若最优构形使用无理数，有理域可能只逼近而不达到该值。

检查器接受整数坐标和有理数字符串，例如 `"3/2"`。它拒绝浮点数、重复点和格式错误的坐标。它以精确分数计算全部 66 个平方距离，不限制坐标或系数大小。

## 公开构造与精确重建

Friedman 的[最大/最小距离页面](https://erich-friedman.github.io/packing/maxmin/)在 `n=12` 行列出当前已知最小平方比 `5+2√3=8.464...`，并注明构造来自 Ingo Rechenberg（2006）。页面提供图形，没有坐标字符串。图形保存在 `data/source/mm12.gif`，页面 HTML 保存在 `data/source/index.html`。

根据该图独立精确重建的坐标使用 `r=√3`：

```text
(0,0), (1,0), (1/2,r/2), (1/2,1+r/2),
(1/2-r/2,1/2+r/2), (1/2+r/2,1/2+r/2),
(-r/2,1/2), (-r/2,-1/2), (0,-1), (1,-1),
(1+r/2,-1/2), (1+r/2,1/2)。
```

在 `Q(√3)` 中精确检查得到最小平方距离为 1、最大平方距离为 `5+2√3`，有 21 对点达到最小值。本地有理见证将 `r` 替换为 `floor(10^63√3)/10^63`，其中 floor 由 `isqrt(3·10^126)` 精确计算。检查器另行报告该有理见证的完整精确分数目标。该值略大于 `5+2√3`，所以重建有理见证略弱；本地坐标没有被说成 Rechenberg 的原始坐标文件。兼容分数使用冻结值 `8.464101615137755`，这是由有理重建值向上舍入的 JSON 数字。

截至 2026-11-06，Friedman 页面仍列出同一 n=12 数值。AlphaEvolve [2025 年论文第 6.50 题](https://arxiv.org/html/2511.02864v1)列出 n≤8 的精确值，并将 n=9 到 30 的后续结果称为数值候选。n=12 的构造是已报告可行上界；所查来源没有最优性证明。

## 程序和搜索

简单初始程序返回 4×3 整数网格，精确目标为 13。传统基线在分母为 64 的有理网格上运行固定步数的模拟退火，每次改变一个坐标，并保留精确比值最好的构造。它不读取人类或参考见证。种子 0 的结果及精确成绩保存在 `best/`。

## 来源

- Erich Friedman，[最大距离/最小距离比](https://erich-friedman.github.io/packing/maxmin/)，n=12 行与图形；页面注明 Rechenberg（2006）。
- Ingo Rechenberg, “Point configurations with minimal distance ratio,” 2006；列为 [AlphaEvolve 论文参考文献 237](https://arxiv.org/html/2511.02864v1)。
- Georgiev、Gómez-Serrano、Tao 与 Wagner，[Mathematical exploration and discovery at scale](https://arxiv.org/abs/2511.02864)，v1，第 6.50 题。

运行测试：

```sh
.venv/bin/python -m pytest tasks/t081/test_task.py -q
```

状态：已通过 Sol 验收（2026-11-06）。
