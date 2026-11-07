# T052：长度 12、最小距离 9 的置换码

## 数学定义

配置 `T052-C01` 固定字母表 `{0,...,11}`。每个码字是这 12 个符号的一个排列。不同码字的 Hamming 距离（对应位置符号不同的个数）必须至少为 9。目标是最大化码字数量 `M(12,9)`。

解答使用 `{"codewords": [[...], ...]}`。评测器精确检查每个码字和全部码字对，并重新计算数量。它不采用程序给出的分数。

## 来源、纪录与基线

Smith 和 Montemanni 的表报告 `M(12,9) ≥ 1320`、`M(12,9) ≤ 11880`。论文 §4 item 22 使用 `PGL(2,11)` 在 `F_11 ∪ {∞}` 上的作用构造 1320 个置换，内部最小距离为 10。此处在有限域上将点 `0,...,10,∞` 编码成 `0,...,11`，并从射影矩阵公式重建全部置换。

对保存的 1320 个码字，评测器检查了全部 `870540` 对；实算最小距离为 10。`human.py` 从群作用公式生成构造。`reference.py` 重放固定 JSON 见证。该 1320 是当前已查来源中最高的同参数报告；未找到证明 `M(12,9)=1320` 的结果。2012 表中的 11880 是已查到的上界，不声称它是当前最强上界。2025 年 Bereg 等人的置换多项式论文给出其他参数的下界；其结果表没有列出 `(12,9)`。作者的在线置换码索引可检索，但其总表直接访问返回 403；能读取的 `n-1`、`n-2` 表不适用于本配置。纪录调查日期为 2026-11-06。

人类对照和冻结基线均为传统群论构造的 1320。该构造来源早于现代 LLM 生成式 AI，来源没有报告 AI 参与。AI 辅助或来源未披露的同参数结果未在所查来源中发现。

## 程序与搜索

- `init_program.py` 从恒等排列的 12 个循环平移开始；构成有效的 12 码字起点。
- `baseline.py` 使用固定种子的随机贪心装包，按完整距离约束加入候选排列。
- `evolution.py` 运行多个随机贪心批次并保留最好有效批次。
- `human.py` 按传统 PGL(2,11) 群作用公式生成 1320 个码字。
- `reference.py` 从 `data/reference/pgl_2_11_n12_d9.json` 重放固定参考见证。
- 搜索入口可用 `MATHBENCH_SEED` 和 `MATHBENCH_SEARCH_ITERATIONS` 固定。每次最多 500/750 个候选（也可分别用 `T052_CANDIDATES_PER_RESTART`、`T052_CANDIDATES_PER_GENERATION` 设置，上限 10000）。默认每次生成上限 300 秒，验证上限 60 秒，内存 4 GiB、一个计算线程。可选 `MATHBENCH_SEARCH_SECONDS` 会改为按时间截断，结果可能依赖机器。
- 初始程序和传统搜索不读取 `data/reference/`。对照资产须在模型上下文之外。

## 本地检查

在仓库根目录运行：

```sh
.venv/bin/python -m pytest tasks/t052/test_task.py -q
.venv/bin/python -m json.tool tasks/t052/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t052/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t052/records.json > /dev/null
```

状态：已通过 Sol 验收（2026-11-06）。

---

# T052: Length-12 permutation codes with minimum distance 9

## Mathematical definition

Configuration `T052-C01` uses the alphabet `{0,...,11}`. Each codeword is a permutation of these 12 symbols. Every pair of distinct codewords must have Hamming distance at least 9, where Hamming distance counts positions with different symbols. The objective is to maximize the number of codewords, `M(12,9)`.

The solution has the form `{"codewords": [[...], ...]}`. The checker validates every row and every pair, then recomputes the code size. It ignores any score supplied by the program.

## Sources, record, and baseline

Smith and Montemanni report `M(12,9) ≥ 1320` and `M(12,9) ≤ 11880`. In §4, item 22, they use the action of `PGL(2,11)` on `F_11 ∪ {∞}` to construct 1320 permutations with internal minimum distance 10. This task encodes the points `0,...,10,∞` as `0,...,11` and rebuilds the permutations from the projective-matrix formula.

The checker evaluates all `870540` pairs in the saved 1320-word code and finds minimum distance 10. `human.py` generates the construction from the group action. `reference.py` replays the fixed JSON witness. The 1320 code is the highest same-parameter report found in the sources checked. No proof that `M(12,9)=1320` was found. The 11880 upper bound in the 2012 table is the located bound; it is not claimed to be the strongest bound now. The 2025 permutation-polynomial paper by Bereg et al. reports lower bounds for other parameters, and its result tables do not list `(12,9)`. The authors' online permutation-array index appears in search, but direct access to its general table returned HTTP 403; its reachable `n-1` and `n-2` tables do not cover this configuration. The survey date is 2026-11-06.

The human result and frozen baseline are both 1320 from a traditional group-theoretic construction. This source predates modern LLM-based generative AI and reports no AI contribution. No AI-assisted or provenance-undisclosed same-parameter result was found in the checked sources.

## Programs and search

- `init_program.py` starts with the 12 cyclic shifts of the identity permutation. This is a valid 12-word code.
- `baseline.py` uses fixed-seed random greedy packing and adds a candidate only when it meets every distance constraint.
- `evolution.py` runs multiple random greedy batches and keeps the best valid batch.
- `human.py` generates 1320 words from the traditional PGL(2,11) action.
- `reference.py` replays the fixed witness in `data/reference/pgl_2_11_n12_d9.json`.
- Fix runs with `MATHBENCH_SEED` and `MATHBENCH_SEARCH_ITERATIONS`. Each run considers at most 500/750 candidates by default (override with `T052_CANDIDATES_PER_RESTART` or `T052_CANDIDATES_PER_GENERATION`, capped at 10000). Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one compute thread. Optional `MATHBENCH_SEARCH_SECONDS` enables a time cutoff; results can depend on machine speed.
- The initial program and traditional searches do not read `data/reference/`. Keep comparison assets outside the model context.

## Local checks

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t052/test_task.py -q
.venv/bin/python -m json.tool tasks/t052/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t052/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t052/records.json > /dev/null
```

Status: accepted by Sol on 2026-11-06.
