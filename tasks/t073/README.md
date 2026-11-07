# T073: Minimum equal-weight spherical 5-design on S³

## Definition

Find a finite set `X` of distinct points on the unit sphere `S³ ⊂ R⁴`. It is a spherical 5-design when, for every polynomial `P` of total degree at most five, the average of `P` over `X` equals its average over the uniform sphere measure. Minimize the number of points.

The exact checker verifies the four-coordinate unit norm of every point and all 126 monomials of total degree at most five. Odd sphere moments are zero. For even exponents `2k₁,...,2k₄`, the normalized sphere moment is

```text
product((2*k_i - 1)!!) / product(4 + 2*j for j=0..sum(k_i)-1).
```

The checker accepts coordinates as rational polynomials in one real algebraic number `α`. Input gives a primitive irreducible integer polynomial for `α`, a rational interval containing exactly one real root, and four rational coefficient arrays per point. The checker reduces all expressions exactly in the selected field. It has no arbitrary degree or coefficient-size limit; shared output, time, and memory limits apply.

This coordinate format preserves the continuous `S³` problem. For every fixed finite point count, the sphere equations, moment equations, and distinctness inequalities form a semialgebraic system over `Q`. If it has a real solution, real-closed-field transfer gives a solution with real algebraic coordinates. A finite set of such coordinates belongs to a common real algebraic number field.

## Human construction

The D₄ root system gives a 24-point spherical 5-design: the eight signed coordinate-axis points and the sixteen points with coordinates `(±1/2, ±1/2, ±1/2, ±1/2)`. All coordinates are rational. The task rebuilds this construction and checks it exactly.

## Current bounds and open status

Bondarenko, Radchenko, and Viazovska state `22 ≤ N(3,5) ≤ 24` and identify the 24 minimal D₄ vectors as a 5-design. The lower bound leaves 22 and 23 points open. A 2025 paper calls the 24-point 5-design “putatively” optimal, so it does not close this finite case.

Recent adjacent results do not settle this configuration. The 2026 proof that the minimum spherical 4-design on `S²` has 12 points concerns a different sphere and strength. A 2026 construction paper gives designs in odd dimensions, including `S³`, but no lower bound matching 24 for strength five. Status was checked on 2026-11-06.

## Search entries

The initial program returns the 96-point signed-permutation orbit of `(1,1,2,0)/sqrt(6)`. The traditional baseline enumerates small integer coordinate patterns in a seed-shuffled order and tests the exact moment identity `2*sum(v_i^4)=(sum(v_i^2))^2`; the signed-permutation orbit of `(1,1,0,0)/sqrt(2)` gives 24 points. Neither search entry reads the human or reference witness.

## Sources

- Andriy Bondarenko, Danylo Radchenko, and Maryna Viazovska, [Optimal asymptotic bounds for spherical designs](https://annals.math.princeton.edu/wp-content/uploads/annals-v178-n2-p02-p.pdf), *Annals of Mathematics* 178 (2013), 443–452, p. 444: `22 ≤ N(3,5) ≤ 24` and the D₄ construction.
- Ayodeji Lindblad, [Designs Related Through Projective and Hopf Maps](https://link.springer.com/article/10.1007/s00454-025-00805-7), published 2025-11-28, §3: calls the 24-point 5-design on `S³` putatively optimal.
- Shalender Singh and Vishnupriya Singh, [Finite-Defect Rigidity and the Minimum Spherical 4-Design on the Two-Sphere](https://arxiv.org/abs/2609.31689), 2026-09-16; different `S²`, strength-4 result.
- Konstantin Delchev and Boryan Yordanov, [Efficient lifts into odd dimensions of Spherical 5- and 7-designs with Balanced Halves](https://arxiv.org/abs/2610.12767), 2026-10-08; construction result, not a matching `N(3,5)` lower bound.

## Reproduction

Set `MATHBENCH_CONFIG_ID=T073-C01` and run one of the five `run_code()` entries. Test with:

```sh
.venv/bin/python -m pytest tasks/t073/test_task.py -q
```

---

# T073：S³ 上最少点的等权球面 5-design

## 定义

在单位球面 `S³ ⊂ R⁴` 上选取互异有限点集 `X`。若任意总次数不超过 5 的多项式 `P` 在 `X` 上的平均值等于其在均匀球面测度下的平均值，则 `X` 是球面 5-design。目标是最小化点数。

精确检查器验证每点四维坐标的单位范数，并检查总次数不超过 5 的全部 126 个单项式。奇数阶球面矩为零。对偶数指数 `2k₁,...,2k₄`，归一化球面矩为

```text
product((2*k_i - 1)!!) / product(4 + 2*j for j=0..sum(k_i)-1).
```

坐标以共同实代数数 `α` 的有理系数多项式表示。输入包括 `α` 的本原不可约整数多项式、唯一选定一个实根的有理隔离区间，以及每个点的四个有理系数数组。检查器在所选代数域中精确约化所有运算。它不设任意次数或系数长度上限；受共享输出、时限和内存限制约束。

这种坐标格式不改变连续 `S³` 问题。对任意固定点数，球面方程、矩条件和点互异不等式组成有理系数半代数系统。若其有实数解，实闭域传递定理保证它也有实代数数坐标解。有限个实代数坐标可放入一个共同实代数数域。

## 人类构造

D₄ 根系给出 24 点球面 5-design：八个带符号坐标轴点，以及坐标均为 `±1/2` 的 16 个点。所有坐标都是有理数。任务按此构造生成点并精确校验。

## 当前界与开放状态

Bondarenko、Radchenko 和 Viazovska 给出 `22 ≤ N(3,5) ≤ 24`，并指出 24 个 D₄ 最短向量构成 5-design。22 和 23 点是否可行仍未解决。2025 年论文称 24 点设计“被认为可能最优”，未闭合该有限实例。

近期相邻结果没有解决本配置。2026 年证明 `S²` 上最少 12 点的球面 4-design 涉及不同球面和强度。2026 年构造论文给出包括 `S³` 在内的奇数维设计，但没有给出强度五、与 24 匹配的下界。来源检查日期为 2026-11-06。

## 搜索入口

初始程序返回 `(1,1,2,0)/sqrt(6)` 的 96 点符号置换轨道。传统基线按种子随机排列小整数坐标模式，并精确检查矩恒等式 `2*sum(v_i^4)=(sum(v_i^2))^2`；`(1,1,0,0)/sqrt(2)` 的符号置换轨道给出 24 点。两者均不读取人类或参考见证。

## 来源

- Andriy Bondarenko、Danylo Radchenko、Maryna Viazovska，[Optimal asymptotic bounds for spherical designs](https://annals.math.princeton.edu/wp-content/uploads/annals-v178-n2-p02-p.pdf)，*Annals of Mathematics* 178 (2013), 443–452，第 444 页：`22 ≤ N(3,5) ≤ 24` 及 D₄ 构造。
- Ayodeji Lindblad，[Designs Related Through Projective and Hopf Maps](https://link.springer.com/article/10.1007/s00454-025-00805-7)，2025-11-28 发表，第 3 节：称 `S³` 上 24 点 5-design 被认为可能最优。
- Shalender Singh、Vishnupriya Singh，[Finite-Defect Rigidity and the Minimum Spherical 4-Design on the Two-Sphere](https://arxiv.org/abs/2609.31689)，2026-09-16；内容为不同的 `S²` 强度 4 结果。
- Konstantin Delchev、Boryan Yordanov，[Efficient lifts into odd dimensions of Spherical 5- and 7-designs with Balanced Halves](https://arxiv.org/abs/2610.12767)，2026-10-08；属于构造结果，不是 `N(3,5)` 匹配下界。

## 复现

设置 `MATHBENCH_CONFIG_ID=T073-C01` 并运行五个 `run_code()` 入口之一。测试命令：

```sh
.venv/bin/python -m pytest tasks/t073/test_task.py -q
```
