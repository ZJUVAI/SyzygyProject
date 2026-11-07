# T070: minimum coprime dissection of a 1000 square

## 中文

### 定义和配置

配置 `T070-C01` 固定一个边长为 1000 的正方形。用轴对齐的整数边长小正方形完整覆盖它，要求所有小正方形边长的最大公因数为 1。目标是最小化小正方形数量。允许复合结构和子拼图。这里的最大公因数条件来自 Mrs Perkins's quilt 定义；它不附加“primitive”限制。来源把 primitive 用于描述没有子拼图或不是由较小拼图实质导出的结构。

Pegg 于 2017 年 7 月发布的资料给出边长 1000 的 27 块拼法。[问题页面](https://www.squaring.net/quilts/mrs-perkins-quilts.html)说明定义和历史状态；[下载文件](https://www.squaring.net/downloads/MrsPerkinssQuilts.txt.zip)包含 40,000 行。资料行列出 27 个边长，本任务按最低位置、再最左位置的 skyline 规则恢复坐标，并独立验证。该拼法给出上界 27，不证明最小值为 27。

来源页面指出，阶数超过 18 的多数结果尚未证明最优。Wynn 的[穷举工作](https://arxiv.org/abs/1308.5420)只覆盖不超过 18 块。页面列出的 OEIS A005670 精确值覆盖外边长 1 到 120，不包括 1000。当前配置仍开放。不得把 27 说成已证最优。

### 数据和验证

- `data/source/pegg_2017_row_1000.txt`：保存原文件第 1000 行，含块数、外边长和 27 个小正方形边长。
- `data/source/source_notes.json`：记录源 ZIP 和 TXT 的 SHA-256、原行号、下载地址和来源范围。任务目录只保留这一个数据行。
- `data/reference/pegg_1000_27.json`：skyline 恢复的 27 个 `[x,y,side]`，作为固定对照。
- `check.py`：检查整数坐标、范围、正边长、最大公因数、总面积、重叠和全覆盖。它为每个整数 x 列保存 1000 位覆盖掩码。重复覆盖位表示小正方形重叠；所有列都填满才接受。

初始程序把 999×999 正方形放在左下角，再用 999 个顶边单位正方形和 1000 个右边单位正方形填满余下条带，共 2000 块，边长最大公因数为 1。

- `baseline.py`：穷举所有整除 1000 的均匀块数，把一个方块换成边长 `s-1` 的方块和单位条带，比较生成的 15 个有效构造。
- `evolution.py`：用定种子变异 guillotine 切割计划。每个矩形叶由欧几里得切割法铺成方块；若边长最大公因数大于 1，就把一个方块细分以加入单位边长。
- `human.py`：从 Pegg 数据行按 skyline 规则重建人类/传统计算见证。
- `reference.py`：复播固定的 27 块见证。
- `evaluator.py`：连接共享候选评测接口。

传统搜索和演化搜索不读取 `data/source/` 或 `data/reference/`。初始程序自包含。程序从 `MATHBENCH_CONFIG_ID` 读取配置，从 `MATHBENCH_SEED` 读取种子。默认使用固定迭代数；设置 `MATHBENCH_SEARCH_SECONDS` 后可启用共享时间截断。预算为生成 300 秒、验证 60 秒、4 GiB、单线程。

### 测试

```sh
.venv/bin/python -m pytest tasks/t070 -q
.venv/bin/python -m json.tool tasks/t070/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t070/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t070/records.json > /dev/null
```

测试涵盖原数据行解码、27 块人类见证、初始方案、传统和演化搜索、重叠、缺失面积、非互素边长、重复块记录、错误类型、越界、伪造分数、程序异常和超时。状态为已通过 Sol 验收（2026-11-06）。

## English

### Definition and configuration

`T070-C01` fixes a square of side 1000. Tile it with axis-aligned squares of positive integer side lengths. The gcd of all tile sides must be 1. Minimize the number of tiles. Compound arrangements and sub-quilts are allowed. The gcd condition is part of the Mrs Perkins's quilt definition. This task does not add the separate source term “primitive,” which describes a quilt with no sub-quilts or no substantial derivation from a smaller quilt.

Pegg's July 2017 data gives a 27-square tiling for outer side 1000. The [problem page](https://www.squaring.net/quilts/mrs-perkins-quilts.html) describes the definition and record status. The [download file](https://www.squaring.net/downloads/MrsPerkinssQuilts.txt.zip) contains the row for size 1000. The row lists 27 tile sides. This task restores the positions by lowest y and then lowest x skyline placement, and checks the result. The tiling proves an upper bound of 27 on the minimum number. It does not prove that 27 is optimal.

The source page says that most results past order 18 are not proved optimal. Wynn's [exhaustive generation](https://arxiv.org/abs/1308.5420) covers dissections with at most 18 squares. The page lists OEIS A005670 exact values for outer sides 1 through 120, not 1000. This configuration remains open. Do not present 27 as a proved optimum.

### Data and verification

- `data/source/pegg_2017_row_1000.txt` stores line 1000 of the source data: the tile count, outer side, and 27 tile sides.
- `data/source/source_notes.json` records the source ZIP and TXT SHA-256 values, row number, URL, and provenance. The task stores only the one source row.
- `data/reference/pegg_1000_27.json` stores the 27 skyline placements `[x,y,side]` for fixed replay.
- `check.py` checks integer coordinates, bounds, positive sides, gcd, total area, overlap, and full coverage. It stores a 1000-bit occupancy mask for each integer x-column. A repeated bit means overlap. Every column must be full.

The initial program puts a 999 by 999 square at the lower left. It fills the top strip with 999 unit squares and the right strip with 1000 unit squares. The result has 2000 tiles and side gcd 1.

- `baseline.py` scans every divisor of 1000 as a uniform block count, then replaces one block by a square of side `s-1` and unit strips. It compares all 15 generated constructions.
- `evolution.py` mutates seeded guillotine split plans. It fills each rectangular leaf by Euclidean square dissection. If the side gcd is above 1, it refines one tile to add unit sides.
- `human.py` rebuilds the traditional computational witness from Pegg's size row with the skyline rule.
- `reference.py` replays the fixed 27-tile witness.
- `evaluator.py` connects the shared candidate-evaluation interface.

The initial and search programs do not read `data/source/` or `data/reference/`. The initial program is standalone. Programs read `MATHBENCH_CONFIG_ID` and `MATHBENCH_SEED`. They use fixed iteration counts by default. Set `MATHBENCH_SEARCH_SECONDS` for the shared time cutoff. The limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread.

### Tests

```sh
.venv/bin/python -m pytest tasks/t070 -q
.venv/bin/python -m json.tool tasks/t070/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t070/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t070/records.json > /dev/null
```

Tests cover source-row decoding, the 27-square human witness, the initial construction, baseline and evolution output, overlap, missing area, non-coprime sides, duplicate tile records, repeated sizes, invalid types, out-of-bounds tiles, forged scores, worker errors, and timeouts. Status is accepted by Sol on 2026-11-06.
