# T066: Orchard problem for 17 points

## Definition

Choose 17 distinct points in the Euclidean plane. Count each distinct straight line that contains exactly three of the 17 points. A line with four or more input points does not count. Maximize this count. The fixed configuration is `T066-C01`.

The input uses a common real algebraic number field. It gives an irreducible integer polynomial, a rational interval isolating one real root, and each point's x and y coordinates as rational coefficient arrays in that root. This representation covers every attainable finite incidence pattern of real points: the pattern is specified by finitely many polynomial equalities and non-equalities with rational coefficients. If it has a real solution, real closed field quantifier elimination gives an algebraic solution, whose finitely many coordinates lie in one number field. The checker validates the irreducible polynomial and root interval, then performs exact field arithmetic.

## Reproduced construction

Ed Pegg's 2018 Wolfram Blog page is public evidence for a same-parameter construction with 40 lines. The frozen coordinates here are an independent exact reconstruction using the classical cubic-curve method; we do not claim that they are the coordinates shown in Pegg's figure. Let

`alpha = tan(pi/17)`

and let `t_k = tan(k*pi/17)` for `k=0,...,16`. Place

`P_k = (t_k, t_k^3/(1+t_k^2))`.

This is the acnodal-cubic subgroup construction made explicit by Green and Tao. Their §2, Theorem 2.5 gives the parametrization of `Y^2 Z = X^2(X-Z)` by `t=cot(pi*x)`, and Proposition 2.6 gives `floor(n(n-3)/6)+1` three-point lines for a subgroup of order n. Take `x=k/17`, for `k=0,...,16`, so the parameters form a subgroup of order 17. The source coordinates are `[sin(theta), cos(theta), sin(theta)^3]` in homogeneous coordinates, where `theta=k*pi/17`. Swap the last two homogeneous coordinates and use the resulting affine chart. Since `cos(k*pi/17)` never vanishes for these indices, this gives finite points

`P_k = (tan(theta), sin(theta)^3/cos(theta)) = (t_k, t_k^3/(1+t_k^2))`.

The curve in this chart is `y(1+x^2)-x^3=0`. It has no line component: `1+x^2` and `x^3` are coprime, so this primitive polynomial of degree one in `y` is irreducible. For three parameters `a,b,c`, the determinant for the three points factors as

`(a-b)(a-c)(b-c)(abc-a-b-c) / ((1+a^2)(1+b^2)(1+c^2))`.

The last numerator is zero exactly when the three angles sum to a multiple of pi. Therefore distinct `P_i,P_j,P_k` are collinear exactly when `i+j+k = 0 (mod 17)`. There are 40 unordered triples with that property. The curve has no line component, so a line cannot contain four distinct points of it. Thus these are 40 distinct lines, each containing exactly three points.

For exact coordinates, `alpha` is the root in `(9/50,19/100)` of

`x^16 - 136*x^14 + 2380*x^12 - 12376*x^10 + 24310*x^8 - 19448*x^6 + 6188*x^4 - 680*x^2 + 17`.

The recurrence `t_(k+1)=(t_k+alpha)/(1-alpha*t_k)`, starting at `t_0=0`, builds each coordinate in `Q(alpha)`. All arithmetic and incidence checks use rational polynomial remainders, not floating-point tests.

## Current bounds and status

The current OEIS A003035 comment and Erich Friedman's table give `a(17) in {40,41,42}`. The 40-line construction supplies the lower bound. The table supplies upper bound 42. The checked sources do not close this interval as of 2026-11-06.

Burr, Grünbaum, and Sloane give a cubic-curve construction with `1+floor(n(n-3)/6)` three-point lines. At `n=17` this gives 40. Green and Tao prove the corresponding bound is exact for all sufficiently large n. Their asymptotic result does not by itself settle n=17.

## Sources

- Ed Pegg Jr., [Cultivating New Solutions for the Orchard-Planting Problem](https://blog.wolfram.com/2018/02/02/cultivating-new-solutions-for-the-orchard-planting-problem/), 2018; figure caption “17 points on 40 lines” and the linked downloadable Mathematica notebook.
- Ben Green and Terence Tao, [On sets defining few ordinary lines](https://arxiv.org/abs/1208.4714v3), §2 Theorem 2.5 and Proposition 2.6 (2013): acnodal-cubic group parametrization and the exact 3-rich-line count for a finite subgroup.
- S. A. Burr, B. Grünbaum, and N. J. A. Sloane, [The Orchard Problem](https://doi.org/10.1007/BF00147569), *Geometriae Dedicata* 2 (1974), 397–424. The copy linked from OEIS is [here](https://neilsloane.com/doc/ORCHARD/orchard.html).
- [OEIS A003035](https://oeis.org/A003035), current comment on the n=17 range and recorded extensions.
- [Erich Friedman, Tree Planting Problems](https://erich-friedman.github.io/packing/trees/), current table, 3-point lines at n=17.
- Ben Green and Terence Tao, [On sets defining few ordinary lines](https://arxiv.org/abs/1208.4714), arXiv:1208.4714v3 (2013), orchard result for sufficiently large n.

## Reproduction

Run the five entries with `MATHBENCH_CONFIG_ID=T066-C01`. Run the tests with:

```sh
.venv/bin/python -m pytest tasks/t066/test_task.py -q
```

The fixed witness is in `data/reference/`. The simple initial program and grid search do not read it.

---

# T066：17 点 Orchard 问题

## 定义

在欧氏平面中选择 17 个互异点。统计包含恰好三个输入点的不同直线；包含四个或更多输入点的直线不计。最大化此数量。固定配置为 `T066-C01`。

输入使用同一个实代数数域：给出不可约整数多项式、恰好隔离一个实根的有理区间，以及每个点的 x、y 坐标在该根上的有理系数多项式。有限的点重合与共线模式由有理系数多项式等式和不等式描述。实闭域量词消去保证：若该模式有实数解，也有实代数数解；有限个坐标可放进同一个数域。检查器会验证不可约性和隔离区间，并执行精确域运算。

## 已复现构造

Ed Pegg 2018 年的 Wolfram Blog 页面为同参数的 40 条直线构造提供公开基线证据。冻结坐标是按经典三次曲线方法独立精确重建的；不声称它们与 Pegg 图中的坐标完全相同。令

`alpha = tan(pi/17)`，`t_k = tan(k*pi/17)`，其中 `k=0,...,16`，并取

`P_k = (t_k, t_k^3/(1+t_k^2))`。

这是 Green–Tao 明确写出的 acnodal 三次曲线子群构造。该文第 2 节定理 2.5 给出曲线 `Y^2 Z = X^2(X-Z)` 的 `t=cot(pi*x)` 参数化；命题 2.6 给出阶为 n 的子群所确定的三点直线数 `floor(n(n-3)/6)+1`。取 `x=k/17`，`k=0,...,16`，得到阶为 17 的子群。齐次坐标为 `[sin(theta), cos(theta), sin(theta)^3]`，其中 `theta=k*pi/17`。交换后两个齐次坐标并使用对应仿射图。此处 `cos(k*pi/17)` 均非零，所以产生有限点

`P_k = (tan(theta), sin(theta)^3/cos(theta)) = (t_k, t_k^3/(1+t_k^2))`。

该图下的曲线是 `y(1+x^2)-x^3=0`。`1+x^2` 与 `x^3` 互素，因此此关于 y 一次的本原多项式不可约，曲线上没有直线分支。三点参数为 `a,b,c` 时，行列式因子分解为

`(a-b)(a-c)(b-c)(abc-a-b-c) / ((1+a^2)(1+b^2)(1+c^2))`。

最后一个分子恰在三个角度之和为 π 的整数倍时为零。因此三个不同点共线，当且仅当 `i+j+k = 0 (mod 17)`。满足条件的无序三元组有 40 个。该曲线没有直线分支，所以任何直线最多包含其中三个不同点。故这给出 40 条各含恰好三点的直线。

精确坐标中，`alpha` 是下列 16 次多项式在 `(9/50,19/100)` 内的根：

`x^16 - 136*x^14 + 2380*x^12 - 12376*x^10 + 24310*x^8 - 19448*x^6 + 6188*x^4 - 680*x^2 + 17`。

从 `t_0=0` 开始用 `t_(k+1)=(t_k+alpha)/(1-alpha*t_k)` 递推。所有运算和共线检查均使用有理多项式余数，不使用浮点容差。

## 当前界与状态

当前 OEIS A003035 注释和 Erich Friedman 表给出 `a(17) 属于 {40,41,42}`。40 点线构造给出下界 40，表中上界为 42。截至 2026-11-06 检查的来源没有闭合这个区间。

Burr、Grünbaum 和 Sloane 给出三次曲线构造，下界为 `1+floor(n(n-3)/6)`。取 `n=17` 得到 40。Green–Tao 证明充分大的 n 上该界精确；渐近结论本身没有解决 n=17。

## 来源

- Ed Pegg Jr.，[Cultivating New Solutions for the Orchard-Planting Problem](https://blog.wolfram.com/2018/02/02/cultivating-new-solutions-for-the-orchard-planting-problem/)，2018；页面图题为“17 points on 40 lines”，并链接 Mathematica notebook。
- S. A. Burr、B. Grünbaum、N. J. A. Sloane，[The Orchard Problem](https://doi.org/10.1007/BF00147569)，*Geometriae Dedicata* 2 (1974), 397–424。OEIS 链接的原文副本[见此](https://neilsloane.com/doc/ORCHARD/orchard.html)。
- [OEIS A003035](https://oeis.org/A003035)，当前 n=17 范围说明和记录更新。
- [Erich Friedman, Tree Planting Problems](https://erich-friedman.github.io/packing/trees/)，当前 3 点直线表，n=17。
- Ben Green 和 Terence Tao，[On sets defining few ordinary lines](https://arxiv.org/abs/1208.4714v3)，第 2 节定理 2.5 和命题 2.6 (2013)：acnodal 曲线群参数化以及有限子群的精确三点直线数。
- S. A. Burr、B. Grünbaum、N. J. A. Sloane，[The Orchard Problem](https://doi.org/10.1007/BF00147569)，*Geometriae Dedicata* 2 (1974), 397–424。OEIS 链接的原文副本[见此](https://neilsloane.com/doc/ORCHARD/orchard.html)。

## 复现

五个程序使用 `MATHBENCH_CONFIG_ID=T066-C01`。测试命令：

```sh
.venv/bin/python -m pytest tasks/t066/test_task.py -q
```

冻结见证位于 `data/reference/`。初始程序与整数格搜索不读取该文件。
