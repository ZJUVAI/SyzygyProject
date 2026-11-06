# T079: Nonnegative convolution extremum, 208 steps

## English

Return 208 nonnegative rational coefficients, with positive total mass. The support is `[-1/4, 1/4]`. The checker normalizes the coefficients to integral 1, then computes `J = 2 n max(convolution(a,a)) / (sum(a))^2` for `n=208`. It uses exact rational arithmetic over the full convolution array. Since all coefficients are nonnegative, the maximum absolute value equals the maximum value. The checker verifies a feasible score; it does not prove optimality.

The local historical witness comes from Matolcsi and Vinuesa (2009), arXiv:0907.1379. Its 208 coefficients were extracted, rationalized as decimal fractions, and its score was independently recomputed as `1.5097201507458786`. This is a historical construction, not a current-record or optimality claim. The baseline starts from seeded random positive coefficients, then makes nonnegative local edits. It does not read the human witness.

## 中文

返回 208 个非负有理数系数，且系数总和大于零。支撑区间为 `[-1/4, 1/4]`。检查器先将系数归一化为积分 1，再精确计算 `J = 2 n max(convolution(a,a)) / (sum(a))^2`，其中 `n=208`。检查器用有理数运算计算完整卷积数组。系数非负，因此绝对值最大值等于最大值。检查器验证可行解和分数，不证明最优性。

本地历史见证来自 Matolcsi 和 Vinuesa 于 2009 年发表的论文 arXiv:0907.1379。任务提取了 208 个系数，将小数精确转成有理数，并独立重算得到分数 `1.5097201507458786`。这是一项历史构造，不代表当前纪录或最优性。基线从带固定随机种子的正系数开始，再进行保持非负的局部修改。它不读取人类见证。

## Full-domain certificate

With bin width h=1/(2n), f*f is linear between adjacent convolution knots. At each knot its value is h times an entry of the discrete convolution. The extrema are therefore attained at knots. Integral-one normalization gives J=2n max(b)/(sum(a))². This is a full-domain argument.
