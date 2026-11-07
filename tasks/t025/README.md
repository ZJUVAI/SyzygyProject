# T025：有限域中的最大 cap set

## 中文

### 定义与配置

本任务固定在七维向量空间 \(\mathbb F_3^7\) 中寻找点数尽可能多的集合。集合中任意三个不同点都不能满足坐标和为零（模 3）。这等价于集合不含仿射直线。目标是最大化点数。

配置 `T025-C01` 固定维数 7、域大小 3。Thackeray 证明不存在 289 点 cap，因此候选点数的安全上限为 288。当前已知构造为 236 点；最大值仍未确定。

### 验证与程序

评测器检查每个坐标、重复点和所有不同点对。对每一对点，它精确计算唯一可能的第三点。候选程序声明的分数不参与评分。

`init_program.py` 返回二进制子立方体。`baseline.py` 从该种子出发，按固定种子随机排列整个空间，并用精确禁用点集合做贪心扩展。`human.py` 从 Edel 作者公开的 8×248 投影矩阵重建 236 点仿射切片。`reference.py` 读取保存的逐点见证。搜索程序不读取这些参考数据。

### 来源与状态

Edel 与 Bierbrauer 在[论文](https://doi.org/10.1023/A:1011216716700)表 2 和定理 5 给出 236 点构造，并称其为 Calderbank–Fishburn cap。Calderbank 与 Fishburn 在[1994 年论文](https://doi.org/10.1007/BF01388452)首次报告该构造。作者的[矩阵页](https://www.yvesedel.de/Matritzen/CAPs/Matrizen/(248,7,3).html)提供可重建坐标。Thackeray 的[2022 年预印本](https://arxiv.org/abs/2206.09804)证明上界 288。2026 年 11 月 6 日核查到的同维下界和上界仍为 236 与 288；没有找到七维最大值的最优性证明。

**状态：已通过 Sol 验收（2026-11-06）。**

## English

### Definition and configuration

Find a largest subset of the seven-dimensional vector space \(\mathbb F_3^7\) with no affine line. Equivalently, no three distinct points may sum to zero coordinate-wise modulo 3. The objective is to maximize the number of points.

Configuration `T025-C01` fixes dimension 7 and field order 3. Thackeray proved that no 289-point cap exists, so 288 is a safe upper limit. The best reproduced construction has 236 points. The maximum is not known.

### Verification and programs

The checker validates every coordinate, rejects duplicate points, and checks every pair for a third point on its affine line. It computes the objective from the point list and ignores any claimed score.

`init_program.py` returns the binary subcube. `baseline.py` starts from that seed and greedily adds points in seeded random orders. `human.py` rebuilds the 236-point affine slice from the 8 by 248 projective matrix on Edel's author page. `reference.py` reads the saved point witness. The search baseline does not read reference data.

### Sources and status

Edel and Bierbrauer give the 236-point construction in Table 2 and Theorem 5 of their [paper](https://doi.org/10.1023/A:1011216716700) and identify it as the Calderbank–Fishburn cap. Calderbank and Fishburn first published it in [1994](https://doi.org/10.1007/BF01388452). Edel's [author page](https://www.yvesedel.de/Matritzen/CAPs/Matrizen/(248,7,3).html) provides the matrix used to rebuild the coordinates. Thackeray's [2022 preprint](https://arxiv.org/abs/2206.09804) proves the upper bound 288. The source check on 2026-11-06 found no proof of the exact maximum in dimension 7.

**Status: accepted by Sol on 2026-11-06.**
