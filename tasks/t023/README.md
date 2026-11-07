# T023 二元强度四覆盖数组

## 中文

配置固定为强度 `t=4`、20 列、二元符号集 `{0,1}`。每四列必须覆盖全部 16 种有序模式。目标是最小化行数。评测器允许最多 6,196 行。所有汉明重量不超过 4 的 20 位向量构成一个 6,196 行可行数组，因此此上限不会排除最优解。评测器穷举全部 `C(20,4)=4845` 个列组及其 16 种模式，并从数组本身重算行数。

[NIST IPOG-F 表](https://math.nist.gov/coveringarrays/ipof/tables/table.4.2.html)为相同参数提供 65 行数组。原文件中的 `-` 表示未指定值；`human.py` 将其补为 0，然后由精确检查器复核完整二元数组。归档见证保存在 `data/nist_ca_t4_v2_k20.txt`。

[Colbourn 2024 年 11 月表](https://www.data2intelligence.de/ColbournTables/t4v2.html)记录了同参数 39 行构造，来源标记为 Hadamard 构造加 NCK 后优化。表格未附该见证。本任务将 39 记为已报告的公开上界，将 65 记为已下载并可复算的人类基线。

下界为 32。任意 20 列数组删去 7 列后仍须覆盖强度 4 的所有模式，因此得到一个 13 列覆盖数组。Izquierdo-Marquez 与 Torres-Jimenez 在 [论文](https://arxiv.org/abs/1711.10040) 中证明 `CAN(4,13,2)=32`。因此当前区间为 `32 <= CAN(4,20,2) <= 39`。所引论文没有证明 20 列实例最优。本任务状态为“已通过 Sol 验收（2026-11-06）”。

## English

The configuration has strength `t=4`, 20 columns, and the binary alphabet `{0,1}`. Every set of four columns must contain all 16 ordered patterns. The objective is to minimize the number of rows. The checker allows at most 6,196 rows. All 20-bit vectors of Hamming weight at most four form a feasible 6,196-row array, so this cap cannot exclude an optimum. The checker enumerates all `C(20,4)=4845` column sets and all 16 patterns in each projection. It recomputes the row count from the array.

[NIST's IPOG-F table](https://math.nist.gov/coveringarrays/ipof/tables/table.4.2.html) provides a 65-row array for these parameters. In the source file, `-` marks an unspecified value. `human.py` completes each such entry as 0, then the exact checker verifies the completed binary array. The archived witness is `data/nist_ca_t4_v2_k20.txt`.

The [November 2024 Colbourn table](https://www.data2intelligence.de/ColbournTables/t4v2.html) reports a 39-row construction for the same parameters. Its source is listed as a Hadamard construction with NCK postoptimization. The table does not include this witness. This task records 39 as a reported public upper bound and 65 as the downloaded, reproducible human baseline.

The lower bound is 32. Deleting seven columns from any 20-column array still gives a strength-four covering array, now with 13 columns. Izquierdo-Marquez and Torres-Jimenez prove `CAN(4,13,2)=32` in their [paper](https://arxiv.org/abs/1711.10040). Therefore, the current interval is `32 <= CAN(4,20,2) <= 39`. The cited paper does not prove that the 20-column instance is optimal. Status: accepted by Sol on 2026-11-06.
