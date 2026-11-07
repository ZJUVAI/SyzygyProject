# T018: Maximum determinant of order-29 sign matrices

## English

Construct a 29 by 29 matrix with entries in {-1, +1}. The objective is the absolute determinant. The checker computes the determinant with integer Bareiss elimination. This checks feasibility and score; it does not prove global optimality.

The published human witness is from Orrick, Solomon, Dowdeswell, and Smith (2003). Its exact score is `320 * 7^12 * 2^28 = 1188957517256767569920`. The matrix is transcribed into `data/human_order29.json` from the paper's displayed order-29 matrix and its score is reproduced exactly. Source: [Orrick et al., New Lower Bounds for the Maximal Determinant Problem](https://arxiv.org/abs/math/0304410). Brent's [order-29 page](https://maths-people.anu.edu.au/~brent/maxdet/order29/) also lists this construction and related Gram data. The record is a lower bound, not a proof of the maximum.

The deterministic seed is `2I-J`, a nonsingular sign matrix with determinant magnitude `27 * 2^28`. The search baseline starts only from this seed. It uses random restarts and seeded row and entry flips and compares exact determinants. It does not read the human witness.

## 中文

构造一个 29 阶矩阵。每个元素只能是 -1 或 +1。目标是增大行列式绝对值。检查器使用整数 Bareiss 消元，精确计算行列式。该检查只验证矩阵和分数，不证明全局最优。

Orrick、Solomon、Dowdeswell 和 Smith 在 2003 年发表了人类构造。行列式绝对值为 `320 * 7^12 * 2^28 = 1188957517256767569920`。任务从论文中的 29 阶矩阵转录数据，并已用精确整数计算复核。该数值是下界，不是最大值证明。

确定性初始矩阵为 `2I-J`，其行列式绝对值为 `27 * 2^28`。搜索基线从此矩阵开始，进行随机重启，并按固定随机种子翻转行或元素，并比较精确行列式。它不读取人类见证文件。

## Order 27 configuration (C02)

The task also includes order 27. The human baseline is the printed construction in Orrick et al. (2003), with exact determinant magnitude `12611693314584870912`. Brent's archive lists 12,911 known Hadamard equivalence classes and reports determinant `546 * 6^11 * 2^26 = 13293406466724593664`. The first archived representative is saved in `data/reference/order27.json` and independently checked exactly. The archive calls the Gram matrix conjectured optimal; no proof of global optimality is claimed. C02 remains accepted by Sol on 2026-11-07.

配置 C02 固定为 27 阶。人类基线来自 Orrick 等人 2003 年论文，精确行列式绝对值为 `12611693314584870912`。Brent 档案列出 12,911 个已知 Hadamard 等价类，报告值为 `546 * 6^11 * 2^26 = 13293406466724593664`。档案中的首个代表矩阵已保存并精确复算。来源称其 Gram 矩阵为猜想最优；本任务不声称已有全局最优证明。C02 已通过 Sol 验收（2026-11-07）。
