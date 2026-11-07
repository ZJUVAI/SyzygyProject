# T050: Longest induced path in the 9-cube

## English

For this task, the graph is the 9-dimensional hypercube `Q9`. Its vertices are the 512 binary strings of length 9. We encode a string as an integer from 0 to 511. Two vertices are adjacent when their Hamming distance is exactly 1.

A snake is an induced path: every consecutive pair is adjacent, and every nonconsecutive pair is nonadjacent. The objective is to maximize the number of path edges, `len(vertices) - 1`. A cycle is not allowed.

The maximum is open. Wynn reported a traditional 190-edge construction in 2012. Orland et al. report a 191-edge construction in 2026. Their current paper states that whether a 192-edge snake exists in `Q9` remains open. The paper attributes the 191-edge result to cube-surgery simulated annealing. It also discloses project-level LLM help with the manuscript and search code, but does not attribute that help to this specific witness or run. We therefore record it as a source-reported computational result with project-level LLM assistance disclosed.

The human reference and frozen baseline are Wynn's 190-edge path, replayed from the full published transition sequence. The public reference is the complete 191-transition sequence printed in Orland et al., Appendix E. Both are saved and checked exactly. The author's record dataset is pinned to commit `46c765399353a588ea50444a5d6610f53102b1c2`. See [IMPLEMENTATION.md](IMPLEMENTATION.md) for source hashes, evidence and checks.

## 中文

本任务使用9维超立方体 `Q9`。它有512个顶点，每个顶点是一个9位二进制串。我们用0到511之间的整数编码顶点。两个顶点的汉明距离为1时相邻。

蛇是诱导路径：相邻的路径顶点必须相邻，任何非相邻的路径顶点都不能相邻。目标是最大化路径边数，即 `len(vertices) - 1`。本任务不接受环。

最大值仍未解决。Wynn于2012年报告了190条边的传统构造。Orland等人在2026年报告了191条边的构造。他们当前论文明确指出，`Q9` 中是否存在192条边的蛇仍是开放问题。论文说明191边结果由立方手术模拟退火得到。作者同时披露，他们在论文写作和搜索代码编写、优化中使用了大语言模型帮助；论文没有说明这项帮助是否用于这条具体见证或该次运行。因此记录为来源报告的计算结果，并注明项目披露了大语言模型协作。

人类基线和冻结对照使用Wynn完整发表序列重放的190边路径。公开参考使用Orland等人附录E中完整发表的191次坐标翻转。两条路径都已保存并精确检查。作者的纪录仓库固定在提交 `46c765399353a588ea50444a5d6610f53102b1c2`。来源哈希和验证记录见 [IMPLEMENTATION.md](IMPLEMENTATION.md)。

## Programs and evaluation

The five program entries are `init_program.py`, `baseline.py`, `human.py`, `reference.py`, and `evolution.py`. They all expose `run_code()` and read `MATHBENCH_CONFIG_ID` and `MATHBENCH_SEED`. The initial program flips each coordinate once, giving a valid 9-edge path. The traditional search uses bounded, seeded greedy endpoint extension. The evolution entry applies seeded endpoint truncation and regrowth. The human and reference programs replay their fixed external witnesses; neither witness is loaded by the initial or search programs.

The checker tests all vertices and all pairs with exact integer bit counts. It ignores any declared score. The default search limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory and one thread. Search iteration counts are fixed by default. `MATHBENCH_SEARCH_SECONDS` can set an exploratory wall-clock limit. `evaluator.py` calls the shared evaluator.

### Links

- [Orland et al., current arXiv paper v3](https://arxiv.org/html/2607.15270v3), especially §6 and Appendix E.
- [Authors' record dataset](https://github.com/Math-AI-Caltech/Snake-in-the-Box), pinned in the task records.
- [Wynn, 2012](https://arxiv.org/html/1201.1647), §VI and Appendix.
- [Current Q9 status entry](https://leapsinbounds.org/constants/snake-in-the-box-9/), checked 2026-11-06. It lists a verified lower bound of 191 and no upper bound.


Additional configurations use the same induced-path rules. Use `MATHBENCH_CONFIG_ID`. C01 has 9 coordinates; C02 has 10; C03 has 11. Vertex labels range from zero to `2**dimension - 1`. The objective counts edges. The initial program uses only the public dimension.

C02 reproduces the 379-edge Q10 path. C03 reproduces the 746-edge Q11 path and records the later reported value 750 separately. Sources are Orland et al. arXiv:2607.15270v3 Table 1 and its Echols footnote. The historical comparator extends Wynn's Q9 path by adding an endpoint step in each new dimension. Both additions are accepted by Sol on 2026-11-07.

新增配置为10维与11维。验证复算379边和746边。11维750边另列为文献报告。新增配置已通过 Sol 验收（2026-11-07）。
