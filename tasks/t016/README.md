# T016: 有符号阶梯函数自卷积极值，208 步

## English

Return 208 coefficients for a step function on 208 equal bins in `[-1/4, 1/4]`. Signed values are allowed. The coefficient sum must be nonzero; scaling the step function sets its integral to 1 and does not change the objective. Minimize `J = 416 * max_k |sum_i a[i] a[k-i]| / (sum_i a[i])^2` over the full convolution index range `k=0,...,414`. The checker uses exact `Fraction` arithmetic and checks every convolution coefficient. It checks feasibility and score; it does not prove optimality.

The human reference is `1.5097201507458786`. It transfers the published nonnegative 208-step construction by Matolcsi and Vinuesa (2009) to the wider signed class. It is a reproduced feasible baseline, not a claim about the authors' best signed construction, the latest public record, or an optimum. The distinct signed 150-step witness is out of scope here: its reported positive-only peak `1.458105685768` is not an absolute objective; its absolute score is about `2.426895802097`.

The seeded starter emits a deterministic signed vector. The search baseline makes mass-preserving pairwise coefficient changes. Neither reads the human witness. The human and reference programs load only the task-local copy in `data/`.

## 中文

返回 208 个系数，表示区间 `[-1/4, 1/4]` 上等宽分段的阶梯函数。系数可以为负数。系数和必须非零；将函数缩放到积分为 1 不会改变目标值。目标是最小化完整卷积范围 `k=0,...,414` 上的 `J = 416 * max_k |sum_i a[i] a[k-i]| / (sum_i a[i])^2`。检查器用精确的 `Fraction` 运算检查每个卷积系数。检查器验证可行性和分数，不证明最优性。

人类参考值为 `1.5097201507458786`。该基线将 Matolcsi 和 Vinuesa 于 2009 年发表的非负 208 步构造转用于允许负值的类别。这是已复现的可行基线，不表示作者报告过该有符号任务的最佳构造，也不表示当前公开纪录或最优值。另一个有符号 150 步见证不属于本配置：其正峰值 `1.458105685768` 不是绝对值目标；绝对值分数约为 `2.426895802097`。

带固定种子的初始程序会生成确定的有符号向量。搜索基线通过成对修改系数来保持系数和不变。两者都不读取人类见证。人类程序和参考程序只读取 `data/` 中的任务本地副本。

## Full-domain certificate

With bin width h=1/(2n), the continuous autoconvolution is linear between its knots and zero outside its support. The absolute value of a linear function attains its maximum at an endpoint. Checking every discrete convolution entry therefore gives the full-domain maximum, including negative peaks. Integral-one normalization gives J=2n max|b|/(sum(a))².
