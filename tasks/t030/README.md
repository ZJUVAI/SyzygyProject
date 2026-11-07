# T030：DIMACS DSJC1000.5 图着色

## 中文

本任务固定 DIMACS 图 DSJC1000.5，包含 1000 个顶点和 249,826 条无向边。顶点编号为 0 至 999。候选须给每个顶点一个整数颜色，并确保每条边的端点颜色不同。目标是最小化使用的不同颜色数。评测器逐边检查构造，并从颜色列表重算不同颜色数；候选声明的分数不参与验收。

候选输入 `data/instance.json` 只含实例名、顶点数和边表。其 SHA-256 为 `51550de59559742f72c2da8e3963edab39124cd8f334eb63cae10d9bb3f132bd`。固定输入由 DIMACS 格式纯文本副本生成。副本保留在 `data/source/`，来源仓库固定到 2026-09-17 的提交。原始 Rutgers 文件带 `.col.b` 后缀且采用二进制边编码；本任务使用仓库中同名标准 `p edge` 文本版本，不把二进制文件当作候选输入。

Olawale Titiloye 与 Alan Crispin 的 2012 年论文报告找到了 DSJC1000.5 的 82 色着色。Titiloye 作者页提供该证书；本任务下载证书后检查了全部 1000 个顶点和 249,826 条边，复算为 82 色且无冲突。证书保存在 `data/source/DSJC1000.5_K82_col.txt`，复算摘要在 `data/DSJC1000.5_K82_verification.json`。这是当前核对到的最佳公开结果。作者页还留有旧的 83 色 QA-col 证书，保存在 `data/source/DSJC1000.5_K83.txt`。

Samir Loudni 的 ID-VNS 页面提供 86 色着色。下载的见证覆盖 1000 个顶点，独立复算为 86 个不同颜色，且所有边都合法。人类基线取该见证，保存在 `data/human_witness.json`；`human.py` 会重放该构造。冻结的人类参考分数为 86。

最优值仍未确定。Cazenave、Negrevergne 与 Sikora 的 2025 arXiv 论文在第 6.2 节表 4 的说明中明确称这些困难实例的色数未知，并列出下界 73。Held、Cook 与 Sewell 的论文也报告下界 73。本任务未独立重算这个下界。当前报告区间为 73 至 82。Hertz、Plumettaz 与 Zufferey 的 VSS-Col 论文将该图的 `χ` 标为未知、`k*` 标为 83。开放状态依据论文的明确陈述。来源检查日期为 2026-11-06。

传统基线使用随机并列打破的多起点 DSATUR 贪心着色。它只读取固定图，不读取比较见证。seed 0 的 113 色输出、复算结果和运行记录保存在 `best/seed0_dsatur_*`。初始程序完全自包含，为每个顶点分配独立颜色。状态：已通过 Sol 验收（2026-11-06）。

## English

This task fixes the DIMACS DSJC1000.5 graph. It has 1,000 vertices and 249,826 undirected edges. Vertex labels are 0 through 999. A candidate assigns an integer color to every vertex. The endpoints of every edge must have different colors. The objective is to minimize the number of distinct colors. The evaluator checks every edge and counts the colors again. It ignores any score claimed by the candidate.

Candidate input `data/instance.json` contains only the instance name, vertex count, and edge list. Its SHA-256 is `51550de59559742f72c2da8e3963edab39124cd8f334eb63cae10d9bb3f132bd`. The input was generated from a DIMACS-format text copy. The copy is saved in `data/source/` and pinned to a repository commit dated 2026-09-17. The original Rutgers file has a `.col.b` suffix and uses binary edge encoding. This task uses the same-named standard `p edge` text version; the binary file is not candidate input.

Titiloye and Crispin's 2012 paper reports an 82-coloring of DSJC1000.5. Titiloye's author page provides the certificate. This task checked all 1,000 vertices and 249,826 edges; the certificate has 82 distinct colors and no conflict. The certificate is saved in `data/source/DSJC1000.5_K82_col.txt`, with a replay summary in `data/DSJC1000.5_K82_verification.json`. This is the best public result found in the reviewed sources. The author page also retains an older 83-color QA-col certificate in `data/source/DSJC1000.5_K83.txt`.

Samir Loudni's ID-VNS page provides an 86-coloring. The downloaded witness assigns all 1,000 vertices. An independent replay counts 86 distinct colors and checks every edge. The human baseline is this witness, saved in `data/human_witness.json`. `human.py` replays it. The frozen human reference score is 86.

The optimum remains unknown. In their 2025 arXiv paper, Cazenave, Negrevergne, and Sikora state in the note for Section 6.2, Table 4, that the chromatic numbers of these difficult instances seem unknown. Their DSJC1000.5 row reports a lower bound of 73. Held, Cook, and Sewell also report 73. This task has not independently recomputed that lower bound. The reported interval is 73 to 82. The VSS-Col paper by Alain Hertz, Matthieu Plumettaz, and Nicolas Zufferey marks `χ` unknown and gives `k* = 83`. The open status relies on the papers' explicit statements. Sources were checked on 2026-11-06.

The traditional baseline uses multi-start DSATUR greedy coloring with seeded random tie breaks. It reads the fixed graph and does not read comparison witnesses. The seed 0 result with 113 colors, exact verification, and run record are saved under `best/seed0_dsatur_*`. The initial program is self-contained and assigns a separate color to each vertex. Status: accepted by Sol on 2026-11-06.
