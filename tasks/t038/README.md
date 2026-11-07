# T038：12 阶互相正交拉丁方的数量

## 中文

### 目标和配置

配置 `T038-C01` 固定阶数为 12。程序提交一组同阶拉丁方，并最大化方阵数量。符号固定为整数 0 至 11。每一行和每一列都须各含这些符号一次。任意两个不同方阵叠加后，144 个有序符号对都须恰好出现一次。

验证器逐项检查所有约束，并重算目标值。它不采信程序报告的分数。验证是精确整数运算。

### 人类构造和公开记录

Charles E. Roberts 的论文报告了阶数 12 的构造，其数量达到当时已知下界 5。SageMath 10.10 的组合设计数据库保存五个 12 阶方阵，并将这份数据归于 Brendan McKay。目录保存了该版本的函数片段和从中逐字提取的五方阵数据。提取时把字母 `a` 至 `l` 映射为 0 至 11，没有执行 Sage 代码。`human.py` 和 `reference.py` 读取这份数据。论文作者与 Sage 数据归属是两项不同记录。

五个方阵已逐行、逐列和逐对精确复算。五是已验证下界，不是最优性证明。普遍上界为 11。11 个方阵等价于阶数 12 的射影平面；其存在性仍未解决。公开资料未给出六个方阵不存在的证明，本配置不声称 5 已最优。

### 起点和传统基线

`init_program.py` 返回一个循环拉丁方。`baseline.py` 用 GF(3) 与 GF(4) 的直积构造两个互相正交的方阵。MacNeish 的乘积构造给出这两个方阵；程序按有限域算术直接重建它们，不读取五方阵对照数据。`evolution.py` 从该构造开始，以固定种子搜索随机同位变换，并保留当前最好可行解。

## English

### Goal and configuration

Configuration `T038-C01` fixes the order at 12. Return a family of Latin squares and maximize its size. Use the integer symbols 0 through 11. Each row and column must contain every symbol once. Each pair of different squares must contain all 144 ordered symbol pairs once.

The checker verifies every constraint and recomputes the objective with exact integer operations. It ignores any score reported by the program.

### Human construction and public record

Charles E. Roberts reports a construction at order 12 that meets the then-current lower bound of five. The SageMath 10.10 combinatorial design database stores five squares of order 12 and attributes the data to Brendan McKay. This task stores the function fragment and the five squares extracted from it. The extraction maps letters `a` through `l` to 0 through 11. It does not execute Sage code. `human.py` and `reference.py` replay this data. The paper author and the Sage data attribution are separate records.

All five squares pass exact row, column, and pair checks. Five is a verified lower bound, not a proof of optimality. The general upper bound is 11. Eleven squares are equivalent to a projective plane of order 12, whose existence remains open. The sources checked do not prove that six squares cannot exist. This task does not claim that five is optimal.

### Starter and classical baseline

`init_program.py` returns one cyclic Latin square. `baseline.py` uses the direct product of constructions over GF(3) and GF(4) to build two orthogonal squares. MacNeish's product construction gives this family; the program rebuilds it with finite-field arithmetic and does not read the five-square comparison data. `evolution.py` starts from this construction, tries seeded random isotopies, and keeps its best feasible family.

### Sources

- [Charles E. Roberts (1992), “Sets of mutually orthogonal Latin squares with ‘like subsquares’”](https://doi.org/10.1016/0097-3165(92)90052-V).
- [Harris F. MacNeish (1922), “Euler Squares”](https://doi.org/10.2307/1967920), for the direct-product construction used by the classical baseline.
- [SageMath 10.10 database entry for `MOLS_12_5`](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/designs/database.html#sage.combinat.designs.database.MOLS_12_5).
- [Google DeepMind formal-conjectures entry on the order-12 MOLS problem](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Paper/LatinSquare.lean).
- [Morris, “Mutually orthogonal Latin squares”](https://www.cs.uleth.ca/~morris/Combinatorics/html/sect_Latin-squares-MOLS.html).
