# T082: Erdős minimum overlap, 51 steps

## English

Choose 51 rational heights in `[0,1]` for an equal-bin step function `f` on `[0,2]`. Its integral must be exactly 1. Define `g=1-f` on `[0,2]`; set both `f` and `g` to zero outside that interval. Minimize `sup_t integral f(x)g(x+t) dx` over both shift directions.

The exact checker evaluates every grid lag. Between adjacent grid lags the cross-correlation is linear, so this gives its full real-shift maximum. It checks all height and mass constraints. It verifies feasibility and does not prove optimality.

The reproduced human witness is Jan Kristian Haugland's printed 51-step construction from 2016 ([paper](https://arxiv.org/abs/1609.08000)). The printed decimals are represented as exact decimal rationals, with no mass adjustment; this gives mass exactly 1. The exact maximum is `64757565083624785688821235069923/170000000000000000000000000000000` (`0.38092685343308696`). This is a feasible upper-bound witness, not a claim that the limiting constant or this fixed 51-step problem is optimal.

## 中文

为区间 `[0,2]` 上的等宽分段函数 `f` 选择 51 个有理数高度。每个高度都必须在 `[0,1]` 内，且积分必须精确等于 1。定义 `g=1-f`，但只在 `[0,2]` 内定义；区间外的 `f` 和 `g` 都为零。目标是对正、负两个方向的所有位移 `t`，最小化 `integral f(x)g(x+t) dx` 的上确界。

精确检查器计算所有网格位移。相邻网格位移之间的互相关函数是线性的，因此这些值给出所有实数位移上的最大值。检查器验证每个高度和积分约束。它验证可行见证，但不证明最优性。

复现的人类见证来自 Jan Kristian Haugland 于 2016 年发表的 51 段构造（[论文](https://arxiv.org/abs/1609.08000)）。我们把论文中的印刷小数作为精确十进制有理数；不需要调整质量，积分正好为 1。精确最大值为 `64757565083624785688821235069923/170000000000000000000000000000000`（`0.38092685343308696`）。这是可行的上界见证，不表示已证明极限常数或本题的 51 段问题达到最优。

## Full-domain certificate

Both functions are constant on bins of width2/51 and vanish outside[0,2]. Their overlap integral is linear between shifts that are integer multiples of2/51. Its maximum is at a knot or at the zero exterior. The complete finite lag check certifies the supremum over every real shift.
