# T042: 最大 3 项等差数列自由子集

## 中文

配置 T042-C01 固定全集为 `[1,212]`。构造子集 `A`，使 `|A|` 最大，并禁止存在 `a<b<c` 且 `a+c=2b` 的三项等差数列。目标为集合大小，单位为整数个数，方向为最大化。检查器用整数运算精确检查所有入选元素对可能形成的中项关系；候选程序声明的分数不参与验收。

此有限实例仍未完全解决。Ergezer 的论文及其后续公开代码记录给出同参数的 43 元素构造。论文指出 44 元素可行性仍未解决。当前代码记录显示历史 T1c 两个分块已有独立 DRAT 证明，T2 有 6,045/6,071 个分块得到无证明日志的求解器闭合；完整 T3 分块空间仍未获得完整认证。因此这些局部进展不能证明 `r_3(212)≤43`，当前已认证范围仍为 `43≤r_3(212)≤44`。论文 v1、当前仓库与 Zenodo v2 的状态分别记录在 `records.json`。

当前维护版论文明确披露 Claude Sonnet 4.5、Claude Opus 4.6 与 Codex GPT-5 参与写作修改、代码生成与审查、实验规划、仓库脚手架和计算编排。但来源没有说明这些工具是否参与提出或搜索出这一个 43 元素集合。该具体构造的发现流程记为未披露，不作为冻结人类基线。人类基线按 Odlyzko–Stanley 1978 年的贪心序列 `S(1)` 重建。其元素是三进制展开只含 0 和 1 的非负整数。我们取五位数字并整体加一，得到：

`A={1+Σ(i=0..4) ε_i 3^i : ε_i∈{0,1}}`。

该集合有 32 个不同元素，最大值为 122。逐位检查可得：相加不发生三进制进位；若 `x+z=2y`，每一位满足 `x_i+z_i=2y_i`，故 `x_i=y_i=z_i`，只可能是平凡等式。人类程序重建该公式；其输出也保存在 `data/reference/odlyzko_stanley_n212_32.json`，检查器另行精确核验其有限实例成绩 32。

初始程序返回 `{1}`。传统搜索从这个简单种子开始，固定随机种子打乱其余 211 个整数，并用预先生成的等差数列三元组增量检查，反复贪心加入可行元素。默认 48 次重启；可设置 `MATHBENCH_SEARCH_SECONDS` 做按时间截断的探索。该搜索不读取人类构造、公开见证或 `best/`。

共享运行器默认给每次生成 300 秒、给验证 60 秒、4 GiB 内存和一个 CPU 线程。

公开 43 构造保存在 `data/reference/`，只由 `reference.py` 读取。`best/` 只保存本任务搜索输出。配置仍为“已通过 Sol 验收（2026-11-06）”。

## English

Configuration T042-C01 fixes the universe `[1, 212]`. Construct a subset `A` of maximum size with no triple `a < b < c` satisfying `a + c = 2b`. The scalar objective is `|A|`, measured in integers and maximized. The checker uses exact integer arithmetic and checks every possible midpoint pair among the selected elements. It ignores candidate score claims.

This finite instance remains open. Ergezer's paper and its later public code record a 43-element construction at this parameter. The paper leaves the feasibility of a 44-element set unresolved. The current code record says that independent DRAT proofs now close both historical T1c chunks. A solver portfolio closed 6,045 of 6,071 T2 chunks without proof logs. The full T3 cube space still lacks complete certification. These local results do not prove `r_3(212) <= 43`; the certified range remains `43 <= r_3(212) <= 44`. The paper v1, current repository, and Zenodo v2 snapshots are recorded separately in `records.json`.

The current maintained paper discloses the use of Claude Sonnet 4.5, Claude Opus 4.6, and Codex GPT-5 for writing and revision, code generation and review, experiment planning, repository scaffolding, and computational orchestration. It does not state whether these tools proposed or searched for this specific 43-element set. The witness-specific discovery path is recorded as undisclosed. The public construction is not the frozen human baseline. The human baseline rebuilds the Odlyzko–Stanley 1978 greedy sequence `S(1)`, whose terms are the nonnegative integers with ternary digits 0 and 1. We take five digits and shift by one:

`A={1+Σ(i=0..4) ε_i 3^i : ε_i∈{0,1}}`.

This set has 32 distinct elements and maximum 122. No ternary carries occur in a sum of two such numbers. If `x + z = 2y`, each digit satisfies `x_i + z_i = 2y_i`, so `x_i = y_i = z_i`; only a trivial progression is possible. `human.py` rebuilds the formula. Its output is also saved in `data/reference/odlyzko_stanley_n212_32.json`, and the checker exactly verifies the finite score of 32.

The initial program returns `{1}`. The traditional search starts from this simple seed, shuffles the other 211 integers with a fixed seed, and greedily inserts points after an incremental check against precomputed AP triples. Its default budget is 48 restarts. `MATHBENCH_SEARCH_SECONDS` enables a wall-clock cutoff. The search does not read the human construction, public witness, or `best/`.

The shared runner allows 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one CPU thread by default.

The public 43-set is stored under `data/reference/` and is read only by `reference.py`. The `best/` directory stores this task's own search output. The configuration is accepted by Sol on 2026-11-06.

## Sources

- Odlyzko and Stanley, “Some Curious Sequences Constructed with the Greedy Algorithm” (January 1978), [author-hosted note](https://www-users.cse.umn.edu/~odlyzko/unpublished/greedy.sequence.pdf). Remark 1 identifies the seed-1 sequence with numbers whose ternary expansions contain no 2; this gives the 0/1 digit formula used here.
- Mehmet Ergezer, “Witness-split + window-cardinality refinement for `r_3(N)`” (arXiv:2606.04016v1, 2026-05-31 submission; HTML body date 2026-08-24), [paper](https://arxiv.org/abs/2606.04016), [source snapshot](https://github.com/memoatwit/erdos_1194/tree/mpc-submission-v1.2/erdos_r3). The exact arXiv source archive and witness file hashes are recorded in `records.json`.
- Maintained code snapshot, [repository README at main](https://github.com/memoatwit/erdos_1194/blob/main/erdos_r3/README.md), current commit `cfd76934bff8cb5d5016e9f599063d698a09d47e`, tag `mpc-submission-v1.4` at `4c5811007a286c0b10c9b8bf4a91f79653847b55`.
- The current paper's [generative AI declaration](https://github.com/memoatwit/erdos_1194/blob/cfd76934bff8cb5d5016e9f599063d698a09d47e/erdos_r3/paper/paper.tex#L211-L220) describes broad assistance but does not specify the discovery path for this witness.
- Ergezer, [Zenodo v2 artifact record](https://doi.org/10.5281/zenodo.21413746), modified 2026-07-18. The record says the upper bound remains open and the full cube cover is not certificate-checked.
