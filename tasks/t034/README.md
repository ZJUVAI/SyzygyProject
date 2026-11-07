# T034: Two-color van der Waerden lower bound for 7-term progressions

## 中文

本任务研究配置 T034-C01：用两种颜色给连续整数前缀 `[1,N]` 着色，使其不含同色的 7 项正步长等差数列。目标是最大化 `N`。校验器逐一检查所有起点和正公差，并从颜色数组重算目标值。候选声明的分数不参与验收。

配置状态为“已通过 Sol 验收（2026-11-06）”。T034-C01 固定颜色数为 2，等差数列长度为 7。已解配置 `W(2,6)=1132` 不在本任务内。当前构造只给出下界，不证明 `W(2,7)` 的精确值。

Herwig、Heule、van Lambalgen 与 van Maaren 的 2007 年论文表 3 报告了素数 `p=617`、zipping 次数 0 和 `W(2,7)>3703`。`human.py` 按二次剩余方法重建长度 3703 的构造。位置 `i=0,...,3702` 按模 617 的非零二次剩余着色；位置 0、617、…、3085 设为颜色 0，末位置 3702 设为颜色 1。若两端同色，则会在步长 617 上形成同色七项数列。此程序重建论文报告的方法，不声称 Rabung 本人执行了这次具体的素数搜索。

Monroe 2025 年论文表 1 也报告同一界限。2026 年 Campos、Fox 与 Schildkraut 的论文给出一般渐近下界，没有报告长度超过 3703 的 `k=7` 具体构造。我们没有完成全面文献调查。Monroe 论文所引代码仓库已记录，但本次实现未能固定其提交版本。

初始程序返回长度 6 的合法构造。传统基线用固定随机种子逐项贪心延长，遇到无法延长时重新开始。二者都不读取 `human.py` 或 `reference.py` 的结果。

## English

This task studies configuration T034-C01. It colors a consecutive prefix `[1,N]` with two colors and forbids a monochromatic 7-term arithmetic progression with positive common difference. The objective is to maximize `N`. The checker examines every start and every positive difference, then recomputes the objective from the color list. It ignores candidate score claims.

The configuration is accepted by Sol on 2026-11-06. It fixes two colors and progression length seven. The solved case `W(2,6)=1132` is outside this task. The construction gives a lower bound. It does not prove the exact value of `W(2,7)`.

Table 3 of the 2007 paper by Herwig, Heule, van Lambalgen, and van Maaren reports prime `p=617`, zero zippings, and `W(2,7)>3703`. `human.py` rebuilds the length-3703 construction with quadratic residues. It colors positions `i=0,...,3702` by the nonzero quadratic-residue class modulo 617. Positions 0, 617, ..., 3085 receive color 0. The final position 3702 receives color 1. If both endpoints had the same color, the positions at spacing 617 would form a monochromatic 7-term progression. This program reconstructs the method reported in the paper. It does not claim Rabung personally ran this specific prime search.

Monroe's 2025 paper reports the same bound in Table 1. A 2026 paper by Campos, Fox, and Schildkraut proves a general asymptotic lower bound. It reports no explicit `k=7` construction longer than 3703. This is not a complete literature survey. Monroe's cited code repository is recorded, but its commit was not pinned during this implementation.

The initial program returns a valid construction of length six. The traditional baseline extends a coloring greedily with a fixed random seed and restarts when it cannot extend. Neither program reads the construction from `human.py` or `reference.py`.
