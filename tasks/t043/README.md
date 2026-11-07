# T043: Constant-dimension subspace codes

## English

For the fixed configuration `q=2, n=7, k=3, d=4`, maximize the number of 3-dimensional subspaces of `F₂⁷` such that any two distinct subspaces have subspace distance at least four. The distance is `d_S(U,V) = 2k - 2 dim(U ∩ V)`. The frozen human reference is 333.

Heinlein, Kiermaier, Kurz, and Wassermann published an explicit 333-subspace construction. Their paper reports an integer-linear-programming search. This task reconstructs its Appendix C orbit representatives with the two matrices for `G_{4,6}`, then verifies every subspace and every pair exactly over `F₂`. This is a reproducible construction, not a proof of optimality or a claim of an unaided hand construction.

The exact counting bound is 381: there are 2,667 two-dimensional subspaces and each three-dimensional subspace contains seven of them. Since a distance-four code cannot use a two-dimensional subspace twice, its size is at most 381. The 2025 survey gives the sharper alternative `A₂(7,4;3) ≤ 378` or `A₂(7,4;3) = 381`. The exact optimum remains open in the checked sources. See [IMPLEMENTATION.md](IMPLEMENTATION.md) for source versions, replay details, and limits.

## 中文

本配置固定 `q=2, n=7, k=3, d=4`，目标是最大化 `F₂⁷` 中满足任意两个不同子空间的子空间距离至少为 4 的三维子空间数量。距离定义为 `d_S(U,V) = 2k - 2 dim(U ∩ V)`。冻结的人类参考值为 333。

Heinlein、Kiermaier、Kurz 和 Wassermann 发表了一个含 333 个子空间的显式构造。论文说明该构造来自整数线性规划搜索。本任务从论文附录 C 的轨道代表和 `G_{4,6}` 的两个生成矩阵重建构造，并在 `F₂` 上精确检查全部子空间和子空间对。这是可复现构造，不构成最优性证明，也不表示该结果来自人工手算。

直接计数给出上界 381：二元七维空间有 2,667 个二维子空间，每个三维子空间含七个二维子空间。距离至少为 4 的码不能重复使用二维子空间，所以码大小至多为 381。2025 年综述给出更强的条件上界：`A₂(7,4;3) ≤ 378` 或 `A₂(7,4;3) = 381`。所查来源中的精确最优值仍未解决。来源版本、重放方法和限制见 [IMPLEMENTATION.md](IMPLEMENTATION.md)。
