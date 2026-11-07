# T084：31 项整数 B3 集的最小直径

## 定义

选取 31 个不同整数。任取 3 项组成多重集，允许重复取同一项。要求 5,456 个三项和两两不同，并最小化直径 `max(A) - min(A)`。整体平移不会改变可行性或直径。

检查器使用精确整数加法，对整数大小和正负不设上限。超过 4,300 位的数请用规范十进制字符串提交，以避开 Python JSON 解析器的默认位数限制。

简单合法起点为 `{0, 4^0, 4^1, ..., 4^29}`。每个三项和的四进制位都在 0 到 3 之间，因此不会进位，不同多重集的和也不同。

## 配置与来源

`T084-C01` 固定 31 项、阶数 3。Martos Ojeda、Delgado Ordoñez 和 Trujillo Solarte 的论文表 3 列出一个 Singer 广义构造，参数为 `q=31`、`m=31`，直径为 19,407。见 `data/reference/public_m31_19407.json`。该列表根据论文网页全文转录，不是 PDF 的逐字节副本。检查器会独立验证 5,456 个和及直径。

论文将表中构造称为近最优，并在结论中称当时只知道 7 项及以下的最优 B3 集。我们截至 2026-11-06 检查了同参数来源和检索结果，没有找到 31 项的闭合证明。这个结论限于已检查来源，不代表穷尽所有出版物。

论文引用 Atkinson、Santoro 和 Urrutia 的下界 `G3(m+1) > 10m^3/57`。取 `m=30` 后，31 项直径至少为 4,737。该下界不能证明当前构造最优。[1986 年论文 PDF](https://people.scs.carleton.ca/~santoro/Reports/DistinctSums.pdf)可在线查看。直接计数还可得下界 1,819：平移使最小元素为 0 后，5,456 个不同三项和都在 0 到 3D 之间。

公开的 19,407 构造作为冻结的人类对照和固定参考。实现会重放并检查论文表格中的构造。作者没有说明 2021 年的构造是否使用 AI。仓库中的转录和重放为本基准制作，不归功于原作者。

## 程序与预算

- `init_program.py` 返回四进制起点，不读对照数据。
- `baseline.py` 按递增候选值贪心构造，最多检查 100,000 个候选；达到上限时返回合法四进制起点。它不读人类或参考构造。
- `evolution.py` 从贪心结果开始，做 1,500 次精确检查的单项变动。
- `human.py` 重放论文表 3 的构造。
- `reference.py` 重放当前复现出的同参数最佳见证。
- `check.py` 枚举所有可重复的无序三项，并重算直径。

运行器生成限时 300 秒，验证限时 60 秒，内存 4 GiB，单线程，输出上限 16 MiB。测试覆盖合法对照和起点、非法和冲突、任意大小整数、伪造分数，以及运行器报错和超时。

## 重现

```sh
.venv/bin/python -m pytest tasks/t084/test_task.py -q
```

本任务已通过 Sol 验收（2026-11-06）。

---

# T084: 31-element integer B3 set

## Definition

Choose 31 distinct integers. The sums of all 5,456 multisets of three elements, with repetition allowed, must be distinct. Minimize `max(A) - min(A)`. Translation does not change feasibility or diameter.

The checker uses exact integer arithmetic and sets no limit on integer size or sign. Use canonical decimal strings for values longer than 4,300 decimal digits to avoid Python's JSON integer parser limit. The initial program uses `{0, 4^0, ..., 4^29}`. Base-4 digits of a sum are at most 3, so no carries occur.

## Configuration and evidence

`T084-C01` fixes 31 elements and order 3. Table 3 of Martos Ojeda, Delgado Ordoñez, and Trujillo Solarte lists a Singer-generalized construction with `q=31`, `m=31`, and diameter 19,407. The list in `data/reference/public_m31_19407.json` was transcribed from the paper's web-rendered full text, then checked by the exact task checker. It is not a byte-identical PDF extraction.

The paper describes the table as near-optimal and says optimal B3 sets were known through cardinality 7. We checked current same-parameter sources through 2026-11-06 and found no proof of optimality for 31 elements. This states the sources checked, not a complete survey of all publications.

The cited Atkinson–Santoro–Urrutia bound gives `G3(m+1) > 10m^3/57`. With `m=30`, the integer diameter is at least 4,737. A direct counting argument gives the weaker lower bound 1,819. Neither bound proves the 19,407 construction optimal.

## Programs and reproduction

The initial program uses the base-4 construction. The traditional baseline uses an increasing-candidate greedy rule with at most 100,000 candidate checks, then a valid base-4 fallback. Neither program reads comparison data. The evolution program starts from the greedy construction and makes 1,500 exact-checked mutations. The human and reference programs replay the 19,407 published construction. Its 5,456 sums are checked exactly.

Run tests with:

```sh
.venv/bin/python -m pytest tasks/t084/test_task.py -q
```

This task is accepted by Sol on 2026-11-06.
