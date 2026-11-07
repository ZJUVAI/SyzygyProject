# T082: 和平共存的皇后军队

## 数学定义

在标准 `30×30` 棋盘上放置相同数量的白皇后和黑皇后。坐标是从 0 开始的 `[行,列]`，范围为 `0..29`。同色皇后可以互相攻击。任意白皇后都不能沿同行、同列或对角线攻击黑皇后。最大化每种颜色的皇后数 `m`。

人类记录见证有每种颜色 131 个皇后。当前已查来源没有给出 `n=30` 的最优性证明。一个有限上界是 225：设白黑分别占用 `rW,rB` 行、`cW,cB` 列。异色不能共行或共列，所以行数与列数各自的和都至多 30。每方的皇后数至多是其占用行列矩形面积。由 Cauchy–Schwarz，`2√m≤√(rW cW)+√(rB cB)≤30`，因此 `m≤225`。

## 来源和记录

OEIS A250000 将 `n≤30` 的这组构造归于 Stephen Ainley 的 1977 年作品，并列出 `a(30)≥131`。Kamenetsky 2019 年公开文件含完整 30 行布局。本任务将其解析为零起始坐标，并保存原布局和校验后的坐标。校验器检查全部 `131×131=17161` 个异色皇后对。

Clinch、Drescher、Huynh、Saffidine 的 ALENEX 2025 论文讨论构造、上界和局部搜索；论文称其搜索很快找到 Ainley 构造，并给出仅对充分大的 `n` 成立的渐近上界。本任务不把该渐近界套用到 `n=30`。DiMichele、Forbes 的 INFORMS 论文报告 `n=16` 的已确认最优值为 37；这比旧 OEIS 文本中“只知道前 15 项”的说法更新，但未解决 `n=30`。

## 程序与运行

简单起点为白 `(0,0)`、黑 `(1,2)`。传统搜索重复运行随机贪心的成对加点；演化搜索保留有效布局，并尝试移除一对后再加入一对。搜索只从简单构造开始，不读取人类或参考布局。人类入口从本地保存的 OEIS 原始文本解析棋盘；参考入口重放保存的 JSON 坐标。

```sh
.venv/bin/python -m tasks.t082.init_program
.venv/bin/python -m tasks.t082.baseline
.venv/bin/python -m tasks.t082.evolution
.venv/bin/python -m tasks.t082.human
.venv/bin/python -m tasks.t082.reference
.venv/bin/python -m pytest tasks/t082 -q
```

默认搜索使用固定种子 0、12 次传统重启、30 代演化和 4 个体。生成上限 300 秒，验证上限 60 秒，内存 4 GiB，单线程。状态：`accepted_by_sol`。

---

# T082: Peaceable queens

## Mathematical definition

Place equal-sized white and black armies on a standard `30×30` chessboard. Coordinates are zero-based `[row,column]` pairs in `0..29`. Queens of the same color may attack each other. No white queen may attack a black queen along a row, column, or diagonal. Maximize the army size `m`.

The reproduced human construction has 131 queens of each color. No optimality proof for `n=30` was found in the checked sources. A finite upper bound is 225. Let `rW,rB` be the numbers of rows used by each color and `cW,cB` the corresponding column counts. Opposite colors cannot share a row or column, so each pair of sums is at most 30. Each army lies in its occupied-row by occupied-column rectangle. Cauchy–Schwarz gives `2√m≤√(rW cW)+√(rB cB)≤30`, hence `m≤225`.

## Sources and record status

OEIS A250000 attributes its constructions for `n≤30` to Stephen Ainley (1977) and lists `a(30)≥131`. Kamenetsky's 2019 public file contains the full 30-row layout. The task parses that chart into zero-based coordinates and saves both the source text and verified coordinate witness. The checker examines all `131×131=17161` cross-color pairs.

The ALENEX 2025 paper by Clinch, Drescher, Huynh, and Saffidine studies constructions, bounds, and local search. It says its search quickly finds the Ainley construction and states an asymptotic upper bound only for sufficiently large `n`; this task does not apply that bound to `n=30`. The INFORMS paper by DiMichele and Forbes reports a confirmed optimum of 37 for `n=16`. This corrects older OEIS text that says only the first 15 terms are known, but does not settle `n=30`.

## Programs and commands

The simple starting layout is white `(0,0)` and black `(1,2)`. The traditional search repeats randomized greedy pair additions. The evolutionary search keeps feasible layouts and tries pair removal and re-addition. Both start from the simple construction and do not read human or reference layouts. The human entry parses the saved OEIS source text; the reference entry replays the saved JSON coordinates.

Run all five entry points and the task tests with:

```sh
.venv/bin/python -m tasks.t082.init_program
.venv/bin/python -m tasks.t082.baseline
.venv/bin/python -m tasks.t082.evolution
.venv/bin/python -m tasks.t082.human
.venv/bin/python -m tasks.t082.reference
.venv/bin/python -m pytest tasks/t082 -q
```

Defaults use seed 0, 12 traditional restarts, 30 evolutionary generations, and population 4. Runner limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread. Status: `accepted_by_sol`.
