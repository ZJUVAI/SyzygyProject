# T066: Binary linear code minimum distance

## 中文

### 目标

构造二元线性 `[68,15]` 码，并最大化最小汉明距离。提交 `15 × 68` 的 0/1 生成矩阵。验证器会计算矩阵秩，并枚举全部 32767 个非零码字。

### 基线

公开的 BKLC 页面给出下界 24、上界 26。Magma 的公开 BKLC 数据库为相同参数返回 `[68,15,24]` 码。生成矩阵保存在 `data/sota_generator.json`，`sota.py` 加载该见证，`data/reproduce_sota.m` 记录 Magma 查询。

本任务检查器独立确认矩阵秩为 15，并枚举全部 32,767 个非零码字。重算的最小距离为 24。这复现了公开最佳已知下界，但不证明最优，因为公开上界为 26。原有 `reference.py`、距离 19 搜索见证和距离 8 人类方法见证保持不变。

公开推导的人类基线由三个 `[16,5,8]` 的一阶 Reed–Muller 码直和组成，再补 20 个零坐标。它有 15 个独立生成行，精确最小距离为 8。此基线来自公开码族的标准定义；它不是 BKLC 页面中的构造。另保存了本项目搜索的距离 19 矩阵。它来自系统形式 `[I|P]` 的本地搜索，属于 AI 生成结果，不属于历史人类记录。

## English

### Goal

Construct a binary linear `[68,15]` code and maximize its minimum Hamming distance. Return a `15 × 68` generator matrix with binary entries. The checker computes the matrix rank and enumerates all 32,767 nonzero codewords.

### Baselines

The public BKLC page reports a lower bound of 24 and an upper bound of 26. Magma's public BKLC database returns a `[68,15,24]` code for these parameters. The generator matrix is saved in `data/sota_generator.json`; `sota.py` loads this witness, and `data/reproduce_sota.m` records the Magma query.

The task checker independently confirms rank 15 and enumerates all 32,767 nonzero codewords. The recomputed minimum distance is 24. This reproduces the public best-known lower bound. It does not prove optimality because the public upper bound is 26. The existing `reference.py`, distance-19 search witness, and distance-8 human-method witness remain unchanged.

A public-derived human baseline is the direct sum of three first-order Reed–Muller `[16,5,8]` codes, followed by 20 zero coordinates. It has 15 independent generator rows and exact minimum distance 8. This comes from the standard public code family definition. It is not the construction shown on the BKLC page. The package also saves a distance-19 matrix found by this project’s search. That matrix is an AI-generated result, not a historical human record.

### Sources

- [Grassl BKLC entry for `[68,15]`](https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2), checked 2026-11-05.
- [Magma best-known linear codes documentation](https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html); the database query ran on the [public calculator](https://magma-maths.org/calc/), Magma 2.30-1, checked 2026-11-05.
- [MIT 6.451 lecture notes, Reed–Muller codes](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/bb895c1dee9ce0b39d6846e0aa984981_MIT6_451S05_FullLecNotes.pdf).
