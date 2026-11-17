# T101: Largest isosceles-free subset of the 100 by 100 grid

## English

Configuration `T101-C01` uses the 10,000 integer points `(x,y)` with `0 <= x,y < 100`. Maximize `point_count`. Every three distinct selected points must have three pairwise different squared side lengths. This forbids ordinary and collinear isosceles triangles. Squared integer distances give an exact check.

The reproducible human-method baseline has 16 points on one row. Its x-coordinates are `1 + sum(e_i 3^i)` for four digits `e_i` in `{0,1}`. This is the classical ternary construction with no three-term arithmetic progression. For collinear points, an isosceles triple requires a three-term progression, so this set is feasible. It is deliberately weak and is not presented as the best human result.

The public reference has 164 points. Georgiev, Gomez-Serrano, Tao, and Wagner report this AlphaEvolve construction for the 100 by 100 grid. The saved coordinates are replayed by `reference.py` and checked independently. The paper says the construction is likely not optimal. The reported PatternBoost construction has 160 points; it is AI-assisted and is recorded separately from the human-method baseline. The exact optimum is not known from the sources checked for this task.

Sources: [AlphaEvolve paper, arXiv:2511.02864](https://arxiv.org/abs/2511.02864), Appendix “Subsets of the grid with no isosceles triangles”; [Google DeepMind problem 59](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/59.html); [PatternBoost, arXiv:2411.00566](https://arxiv.org/abs/2411.00566). The public repository also has an October 2026 discussion that reports newer 58-point constructions for the 32 by 32 grid; it does not displace the 164-point 100-grid witness.

## 中文

配置 `T101-C01` 使用 `0 <= x,y < 100` 的 10,000 个整数格点。目标是最大化 `point_count`。任意三个不同格点的三条边长平方必须两两不同。此规则也排除共线等腰三点。验证器使用整数精确计算。

可复现的人类方法基线有 16 个点，全部位于同一行。横坐标为 `1 + sum(e_i 3^i)`，其中四个数字 `e_i` 各为 0 或 1。这是经典的三进制无三项等差构造。共线三点构成等腰图形时必形成三项等差数列，所以该构造有效。此基线较弱，不代表最好的人类成绩。

公开参考构造有 164 个点。Georgiev、Gomez-Serrano、Tao 和 Wagner 在 AlphaEvolve 论文中报告了这个 100 阶方格构造。保存的坐标由 `reference.py` 重放，并由本任务独立检查。论文指出该构造可能不是最优。PatternBoost 报告的 160 点构造使用了 AI 辅助，记录时与人类方法基线分开。根据本任务检查的来源，精确最优值仍未知。

来源见英文部分。公开仓库在 2026 年 10 月另有讨论，报告了 32 阶方格的 58 点构造；这不改变 100 阶方格的 164 点记录。
