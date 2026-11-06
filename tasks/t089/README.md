# T089: Maximum determinant of order-29 sign matrices

## English

Construct a 29 by 29 matrix with entries in {-1, +1}. The objective is the absolute determinant. The checker computes the determinant with integer Bareiss elimination. This checks feasibility and score; it does not prove global optimality.

The published human witness is from Orrick, Solomon, Dowdeswell, and Smith (2003). Its exact score is `320 * 7^12 * 2^28 = 1188957517256767569920`. The matrix is transcribed into `data/human_order29.json` from the paper's displayed order-29 matrix and its score is reproduced exactly. Source: [Orrick et al., New Lower Bounds for the Maximal Determinant Problem](https://arxiv.org/abs/math/0304410). Brent's [order-29 page](https://maths-people.anu.edu.au/~brent/maxdet/order29/) also lists this construction and related Gram data. The record is a lower bound, not a proof of the maximum.

The deterministic seed is `2I-J`, a nonsingular sign matrix with determinant magnitude `27 * 2^28`. The search baseline starts only from this seed. It uses random restarts and seeded row and entry flips and compares exact determinants. It does not read the human witness.

## 中文

构造一个 29 阶矩阵。每个元素只能是 -1 或 +1。目标是增大行列式绝对值。检查器使用整数 Bareiss 消元，精确计算行列式。该检查只验证矩阵和分数，不证明全局最优。

Orrick、Solomon、Dowdeswell 和 Smith 在 2003 年发表了人类构造。行列式绝对值为 `320 * 7^12 * 2^28 = 1188957517256767569920`。任务从论文中的 29 阶矩阵转录数据，并已用精确整数计算复核。该数值是下界，不是最大值证明。

确定性初始矩阵为 `2I-J`，其行列式绝对值为 `27 * 2^28`。搜索基线从此矩阵开始，进行随机重启，并按固定随机种子翻转行或元素，并比较精确行列式。它不读取人类见证文件。
