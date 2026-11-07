# T037: 五维 kissing number

## 定义与配置

给定五维单位球面上的方向集合。每对不同方向的夹角至少为 60 度。目标是最大化方向数。配置 `T037-C01` 固定维数 5 和角度下界 60 度。方向用非零有理向量表示，再作精确归一化。评测器用有理数运算核查角度条件；这限定可提交的证书表示，不声称所有实坐标构形都能用有理坐标表示。

对非零向量 (u,v)，角度条件等价于 (u\cdot v\leq 0)，或在内积为正时满足 (4(u\cdot v)^2\leq (u\cdot u)(v\cdot v))。因此验证不使用浮点容差。

## 来源与基线

Korkine–Zolotareff 的 (D_5) 根系给出 40 个向量：任取两个不同坐标放置 ±1，其余坐标为零。每个向量平方范数为 2，不同向量内积至多为 1。Cohn–Rajagopal 对该构造及五维已知结果作了近期综述：[论文 v3](https://arxiv.org/abs/2412.00937v3)，[期刊版](https://doi.org/10.1007/s00454-026-00841-x)。人类见证由公式重建并由本任务逐对精确验证。

已知下界为 40，公开证明的上界为 44。尚无已检查来源证明 unrestricted 五维 kissing number 等于 40。有限 ternary 坐标集合中的最优性不推出任意实坐标构形的最优性。搜索指令不包含人类见证；初始构形是十个正负坐标轴方向。

## 状态

实现状态：已通过 Sol 验收（2026-11-06）。正式排名只使用 checker 验证通过的构造。声称的分数会被忽略。

# T037: Five-dimensional kissing number

## Definition and configuration

Choose directions in five-dimensional Euclidean space. Every pair must have an angle of at least 60 degrees. Maximize the number of directions. `T037-C01` fixes dimension 5 and the 60 degree limit. Submitted directions use nonzero rational vectors and are normalized exactly. This limits the witness format. It does not claim that every real-coordinate configuration has rational coordinates.

For nonzero vectors (u,v), the angle condition holds when (u\cdot v\leq0), or, for positive inner product, when (4(u\cdot v)^2\leq(u\cdot u)(v\cdot v)). The checker uses exact rational arithmetic.

## Source and baseline

The (D_5) root system of Korkine and Zolotareff gives 40 vectors. Place ±1 in any two distinct coordinates and zero in the rest. Each vector has squared norm 2. Distinct vectors have inner product at most 1. Cohn and Rajagopal review this construction and the known five-dimensional results in their [v3 paper](https://arxiv.org/abs/2412.00937v3) and [journal version](https://doi.org/10.1007/s00454-026-00841-x). The human witness is reconstructed from the formula and checked pair by pair exactly.

The known lower bound is 40. The best published upper bound found is 44. No checked source proves that the unrestricted five-dimensional kissing number is 40. Optimality over a finite ternary alphabet does not prove optimality over unrestricted real coordinates. The model prompt does not expose the human witness. The initial construction is the ten signed coordinate axes.

## Status

Implementation status: accepted by Sol on 2026-11-06. Only checker-verified constructions count in formal results. The checker ignores claimed scores.
