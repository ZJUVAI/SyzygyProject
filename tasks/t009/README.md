# T009: Binary linear code minimum distance

## 中文

### 目标

按配置构造二元线性码，并最大化最小汉明距离。`T009-C01` 为 `[68,15]`，`T009-C02` 为 `[80,20]`，`T009-C03` 为 `[100,20]`。提交 `k × n` 的 0/1 生成矩阵。验证器会计算矩阵秩，并枚举全部 `2^k-1` 个非零码字。

### 基线

公开的 BKLC 页面给出下界 24、上界 26。Magma 的公开 BKLC 数据库为相同参数返回 `[68,15,24]` 码。生成矩阵保存在 `data/sota_generator.json`，`sota.py` 加载该见证，`data/reproduce_sota.m` 记录 Magma 查询。

本任务检查器独立确认矩阵秩为 15，并枚举全部 32,767 个非零码字。重算的最小距离为 24。这复现了公开最佳已知下界，但不证明最优，因为公开上界为 26。原有 `reference.py`、距离 19 搜索见证和距离 8 人类方法见证保持不变。

公开推导的人类基线由三个 `[16,5,8]` 的一阶 Reed–Muller 码直和组成，再补 20 个零坐标。它有 15 个独立生成行，精确最小距离为 8。此基线来自公开码族的标准定义；它不是 BKLC 页面中的构造。另保存了本项目搜索的距离 19 矩阵。它来自系统形式 `[I|P]` 的本地搜索，属于 AI 生成结果，不属于历史人类记录。

### 新配置（已通过 Sol 验收（2026-11-07））

- `T009-C02`: `[80,20]`，最大化最小距离。Grassl 的精确参数页给出 `[80,20,25]`，并给界 `25 ≤ d_max ≤ 30`。其构造从 `[81,20,26]` 三元 QC 码删除第81坐标。项目按页面的三个生成多项式重建循环移位矩阵，得到秩20，并精确枚举全部1,048,575个非零码字，确认距离25。
- `T009-C03`: `[100,20]`，最大化最小距离。Grassl 页给出 `[100,20,34]`，并给界 `34 ≤ d_max ≤ 40`。其构造从 `[99,20,34]` 三元 QC 码补一个零坐标。项目同样重建生成矩阵并精确枚举全部1,048,575个非零码字，确认距离34。

两个配置均未证明最优。页面中的构造记录较旧。本次于2026-11-07用公开 Magma 2.30-1 数据库分别查询 `[80,20]` 和 `[100,20]`，返回距离25和34，与 Grassl 参数页一致；公开上界仍分别为30和40。生成多项式来自 [Chen (1994)](https://doi.org/10.1109/18.333888) 所列构造，由 Grassl 参数页给出。`reference.py` 对 C02/C03 重放保存的25/34距离公开构造；C01 仍使用原 reference。搜索得到的19/26矩阵保留为本地诊断产物，不作为 reference 或公开对照。

## English

### Goal

`T009-C01` keeps the binary linear `[68,15]` instance. `T009-C02` is `[80,20]`, and `T009-C03` is `[100,20]`. Maximize the minimum Hamming distance for the selected parameters. Return a `k × n` generator matrix with binary entries. The checker computes its rank over GF(2) and enumerates all `2^k-1` nonzero codewords.

### Baselines

The public BKLC page reports a lower bound of 24 and an upper bound of 26. Magma's public BKLC database returns a `[68,15,24]` code for these parameters. The generator matrix is saved in `data/sota_generator.json`; `sota.py` loads this witness, and `data/reproduce_sota.m` records the Magma query.

The task checker independently confirms rank 15 and enumerates all 32,767 nonzero codewords. The recomputed minimum distance is 24. This reproduces the public best-known lower bound. It does not prove optimality because the public upper bound is 26. The existing `reference.py`, distance-19 search witness, and distance-8 human-method witness remain unchanged.

A public-derived human baseline is the direct sum of three first-order Reed–Muller `[16,5,8]` codes, followed by 20 zero coordinates. It has 15 independent generator rows and exact minimum distance 8. This comes from the standard public code family definition. It is not the construction shown on the BKLC page. The package also saves a distance-19 matrix found by this project’s search. That matrix is an AI-generated result, not a historical human record.

### New configurations (accepted by Sol on 2026-11-07)

- `T009-C02`: `[80,20]`, maximize minimum distance. Grassl's parameter page gives a `[80,20,25]` code and bounds `25 ≤ d_max ≤ 30`. It punctures coordinate 81 from a `[81,20,26]` degree-three quasi-cyclic code. We rebuild the 20-row matrix from the three listed generator polynomials, verify rank 20, and enumerate all 1,048,575 nonzero words. The distance is 25.
- `T009-C03`: `[100,20]`, maximize minimum distance. Grassl's page gives a `[100,20,34]` code and bounds `34 ≤ d_max ≤ 40`. It appends one zero coordinate to a `[99,20,34]` degree-three quasi-cyclic code. We rebuild the matrix and enumerate all 1,048,575 nonzero words. The distance is 34.

Neither instance has a proof of optimality. The pages have old modification dates. On 2026-11-07, the public Magma 2.30-1 BKLC database returned distances 25 and 34 for `[80,20]` and `[100,20]`, matching the Grassl pages; the upper bounds remain 30 and 40. The polynomial constructions are attributed to [Chen (1994)](https://doi.org/10.1109/18.333888). `reference.py` replays the saved public constructions with distances 25 and 34 for C02 and C03; C01 keeps its prior reference. The locally searched distance-19/26 matrices remain diagnostic artifacts and are not used as references or public records.

### Sources

- [Grassl BKLC entry for `[68,15]`](https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2), checked 2026-11-05.
- [Magma best-known linear codes documentation](https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html); the database query ran on the [public calculator](https://magma-maths.org/calc/), Magma 2.30-1, checked 2026-11-05.
- [MIT 6.451 lecture notes, Reed–Muller codes](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/bb895c1dee9ce0b39d6846e0aa984981_MIT6_451S05_FullLecNotes.pdf).
- [Grassl BKLC entry for `[80,20]`](https://www.codetables.de/BKLC/BKLC.php?k=20&n=80&q=2), checked 2026-11-07.
- [Grassl BKLC entry for `[100,20]`](https://www.codetables.de/BKLC/BKLC.php?k=20&n=100&q=2), checked 2026-11-07.
- [Chen (1994), “Six New Binary Quasi-Cyclic Codes”](https://doi.org/10.1109/18.333888).
- [Magma BKLC database documentation](https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html), checked 2026-11-07.
