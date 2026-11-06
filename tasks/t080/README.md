# T080: Second autocorrelation inequality (AC2)

## English

Choose 20 nonnegative rational coefficients with positive sum. The coefficients give the heights of an equally spaced step function on the 20 equal bins of `[-1/4, 1/4]`. Scaling all coefficients by the same positive number does not change the objective, so normalization is optional.

For the discrete self-convolution `b = a * a`, maximize

`J = (2 sum(b_i^2) + sum(b_i b_(i+1))) / (3 max(b) (sum(a))^2)`.

The checker computes this ratio with exact rational arithmetic. It rejects invalid lengths, negative or non-rational coefficients, booleans, non-finite values, and zero mass. It verifies a feasible witness; it does not prove optimality.

The human witness is the 20-coefficient appendix construction of Mate Matolcsi and Carlos Vinuesa (2009), transcribed as exact decimal rationals and independently recomputed as `0.8892261730897966`. Source: [arXiv:0907.1379](https://arxiv.org/pdf/0907.1379). This is a reproduced historical construction, not a claim of optimality. The later report of `0.962694` is kept separately because its step count and matching witness were not established for this configuration.

## 中文

选择 20 个非负有理数系数，且系数和必须大于零。系数表示区间 `[-1/4, 1/4]` 上 20 个等宽区间的分段常数函数高度。所有系数同时乘以同一个正数不会改变目标值，因此可以不做归一化。

令 `b = a * a` 为离散自卷积。目标是最大化

`J = (2 sum(b_i^2) + sum(b_i b_(i+1))) / (3 max(b) (sum(a))^2)`。

检查器使用精确有理数运算计算该比值。它拒绝长度错误、负数、非有理数、布尔值、非有限值和零质量输入。它验证可行见证，不证明全局最优。

人类见证来自 Mate Matolcsi 与 Carlos Vinuesa 于 2009 年论文附录中的 20 个系数。我们将印刷小数视为精确十进制有理数，并独立重算得到 `0.8892261730897966`。来源：[arXiv:0907.1379](https://arxiv.org/pdf/0907.1379)。这是已复现的历史构造，不表示最优。后续报告的 `0.962694` 单独记录，因为其步数和对应见证尚未确认为本配置。

## Full-domain certificate

With bin width h=1/(2n) and b=a*a, the continuous autoconvolution is the linear interpolation of h*b at its knots. Exact integration of each linear segment gives integral((f*f)²)=h³(2Σb²+Σb[i]b[i+1])/3. Its maximum is h*max(b), and integral(f*f)=h²(sum(a))². The ratio is the exact formula in check.py.
