# T027：QAPLIB tai256c 二次指派问题

## 定义

给定 QAPLIB `tai256c` 的固定整数矩阵 `A`、`B`，以及设施到位置的双射 `p`，最小化

`sum(i=0..255, j=0..255) A[i,j] * B[p[i],p[j]]`。

分数是精确整数。合法解须是 `{0,...,255}` 的一个排列。检查器从任务目录中的固定矩阵读取数据；候选程序只提交排列。任何候选声明的分数都会被忽略。

## 配置与证据

配置为 `T027-C01`，实例为 QAPLIB `tai256c`，`n=256`。QAPLIB 归档解复算得分为 44,759,294。QAPLIB 将该纪录标为 ANT；QAPLIB 历史页把 1997 年改进解归于 T. Stützle。我们复播了保存的解，未重跑原 ANT 搜索。

arXiv v2 于 2024-09-30 更新。论文报告下界 44,200,000、上界 44,759,294 和 1.25% 差距。v2 摘要仍写旧的 1.48% 差距；正文第 3 页及表 4 给出改进值。已查 QAPLIB 页面给出的旧下界不一致：Lehigh 表列 43,849,646，QAPLIB 镜像列 44,095,032。论文把 44,095,032 作为旧界，并报告改进到 44,200,000。2026-11-06 的检索未找到之后的主来源结果或最优性证明；检索范围并非穷尽。任务仍为“已通过 Sol 验收（2026-11-06）”。

## 运行

- `init_program.py`：自包含恒等排列简单起点。
- `baseline.py`：固定种子驱动的随机首次改进交换局部搜索；不读取归档解。
- `evolution.py`：演化运行入口，调用本任务局部搜索。
- `human.py`、`reference.py`：读取公开归档解，仅用于外部对照。
- `check.py`：检查双射，并用 Python 整数精确计算全部 65,536 项。

## Definition

Given the fixed integer matrices `A` and `B` from QAPLIB `tai256c`, minimize over bijections `p` mapping facilities to locations

`sum(i=0..255, j=0..255) A[i,j] * B[p[i],p[j]]`.

Here `p` maps facilities to locations. The objective is an exact integer. The candidate returns only the permutation. The checker loads its own pinned matrices and ignores a claimed score.

## Configuration and evidence

The fixed configuration is `T027-C01`, QAPLIB `tai256c`, `n=256`. Exact replay of the archived QAPLIB permutation gives 44,759,294. QAPLIB labels the record ANT; its history credits T. Stützle with an improved solution in 1997. This task replays the saved witness. It does not reproduce the original ANT search.

The arXiv v2 page lists the last revision as 2024-09-30. Its PDF reports a lower bound of 44,200,000, an upper bound of 44,759,294, and a 1.25% gap. The v2 abstract still gives the earlier 1.48% gap, while the body reports the improved bound. The checked QAPLIB pages disagree on the older lower bound: Lehigh lists 43,849,646 and the QAPLIB mirror lists 44,095,032. The paper treats 44,095,032 as the prior bound and reports 44,200,000. Searches on 2026-11-06 found no later primary result or proof of optimality; the search was not exhaustive. The task status is `accepted_by_sol`.

## Files

- `init_program.py`: self-contained identity-permutation seed.
- `baseline.py`: fixed-seed randomized first-improvement pair-swap local search. It does not read the archived witness.
- `evolution.py`: evolution entry point that calls this task's local search.
- `human.py` and `reference.py`: replay the public archived witness for external comparison only.
- `check.py`: validates the bijection and computes all 65,536 terms with Python integers.

The search defaults to 10,000 pair checks with a fixed `MATHBENCH_SEED`. It uses a wall-clock cutoff only when `MATHBENCH_SEARCH_SECONDS` is set. Run metadata records the seed, pair checks, accepted improvements, and budget mode.
