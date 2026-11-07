# T032: Zarankiewicz number z(14,19;3,3)

## 中文

给定一个 14 行、19 列的 0/1 矩阵。目标是最大化 1 的数量。任取 3 行和 3 列，所得 3×3 子矩阵不得全为 1。配置为 T032-C01。评测器会重新计算 1 的数量，并检查全部 364 组三行。

主来源为 Saurabh 的论文 [Five improved lower bounds for Zarankiewicz numbers](https://arxiv.org/html/2608.26603v1)，版本 v1，2026-08-27。表 1 给出该格下界 126、上界 135。附录 A 提供 126 个 1 的矩阵。作者将构造归于传统 kicked-greedy 搜索；论文说明搜索不使用语言模型或学习组件。NOVA 自主选择参数、运行搜索并整理结果。因此这里把它记录为传统计算构造及自主编排，不称为作者手工发现。

本任务重放公开矩阵，不声称复现原搜索。原始随机种子为 7，但 kick 次数未记录。较早的 AI 辅助结果 121 单独保留，不替代 126。当前验收状态：已通过 Sol 验收（2026-11-06）。

## English

Given a 14 by 19 binary matrix, maximize its number of ones. Every choice of three rows and three columns must contain at least one zero. The fixed configuration is T032-C01. The checker recounts all ones and checks all 364 row triples.

The primary source is Saurabh, [Five improved lower bounds for Zarankiewicz numbers](https://arxiv.org/html/2608.26603v1), version 1, dated 2026-08-27. Table 1 gives a lower bound of 126 and an upper bound of 135 for this cell. Appendix A gives a matrix with 126 ones. The paper attributes the construction to classical kicked-greedy search and states that it used no language model or learned component. NOVA autonomously selected the cell, ran the search, and packaged the results. We record this as a traditional computational construction with autonomous orchestration, not as a manually discovered construction.

This task replays the published matrix. It does not claim to reproduce the search. The original random seed was 7, but the kick count was not recorded. An earlier AI-assisted result of 121 is listed separately. Status: accepted by Sol on 2026-11-06.
