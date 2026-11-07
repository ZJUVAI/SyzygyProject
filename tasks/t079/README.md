# T079：有限域 Kakeya 集 / Finite-field Kakeya set

## 中文

固定任务是在三维向量空间 `F_31^3` 中，为 993 个射影方向各选一条仿射直线，并使所有直线的点集并集尽量小。射影方向的标准表示取最后一个非零坐标为 1。每条直线包含 31 个点，所有坐标运算均模 31。

评测器会检查方向集合是否完整且无重复，并重新生成全部直线点后精确计算并集大小。简单起点把所有方向的直线都放在原点上，覆盖全部 29,791 个点。传统对照采用二次剩余构造，精确复算为 8,641 点。公开的 Station AI 论文给出 8,289 点构造；本任务按论文公式重建直线见证并精确复核。该值是构造上界，不是最优性证明。

主要来源：Bukh 与 Chao，*Sharp density bounds on the finite field Kakeya problem* (2021)，第 4 节关于传统奇数阶构造；Chung、Du 与 Wesley，*Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment* (2026)，第 6.1 节及其形式化验证材料。

## English

For the fixed task, choose one affine line in each of the 993 projective directions of `F_31^3`. Minimize the size of their union. Use the unique direction representative whose last nonzero coordinate is 1. Each line has 31 points, and all coordinate arithmetic is modulo 31.

The checker requires a complete, duplicate-free direction list. It rebuilds every point on every line and computes the union size exactly. The simple seed puts all lines through the origin and covers all 29,791 points. The traditional quadratic-residue construction has 8,641 points after exact checking. A 2026 Station AI paper gives an 8,289-point construction. This task rebuilds its line witnesses from the published formula and verifies them exactly. The value is a construction bound, not an optimality proof.

Main sources: Bukh and Chao, *Sharp density bounds on the finite field Kakeya problem* (2021), Section 4 on the traditional odd-field construction; Chung, Du, and Wesley, *Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment* (2026), Section 6.1 and its formal verification material.
