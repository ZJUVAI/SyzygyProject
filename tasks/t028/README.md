# T028：Taillard Ta051 排列流水车间

## 中文

本任务固定 Taillard Ta051：50 个作业、20 台机器。每个作业都按相同机器顺序加工。候选须提交所有机器共用的一条作业排列。任务不接受非排列调度。目标是最小化最大完工时间（makespan）。

候选输入为 `data/ta051.json`，其中只有 20×50 的正整数加工时间矩阵。矩阵行对应机器，列对应作业编号减一。评测器用整数递推独立计算所有完工时间，并忽略候选声明的分数。官方 Taillard 原始数据副本和当前上下界表保存在 `data/source/`，不属于候选输入白名单。

Eric Taillard 的官方页面列出 Ta051 同参数的下界 3771 和上界 3846。该表注明仅允许排列调度，并标记上界来源为 Va、下界来源为 Taillard。Taillard 页面把该界列为截至 2026-06-03 的当前记录。上界见证采用 Ravetti、Riveros、Mendes、Resende、Pardalos 2012 年公布的排列。独立地用官方矩阵复算得到 makespan 3846。这个见证是可行构造，不是最优性证明；当前区间为 3771 至 3846。

Olivier Brunner 的 Zenodo v8 数据集（2026-01-16）也记录 Ta051 的上界见证。该记录后来更新到 v11（2026-07-31）；v11 页面警告应谨慎解释 `Optimal` 字段。本任务不依据该字段判断最优性，而以 Taillard 官方界表和 Gmys 2022 年论文的 Ta051 仍开放结论核对状态。若发现新的更优见证或最优性证明，应更新记录并重新审查配置。

状态：已通过 Sol 验收（2026-11-06）。

## English

This task fixes Taillard Ta051 with 50 jobs and 20 machines. Every job uses the same machine order. A candidate must return one job permutation for all machines. Non-permutation schedules are invalid. The objective is to minimize the makespan.

The candidate input is `data/ta051.json`. It contains only the 20 by 50 positive integer processing-time matrix. Rows index machines. Columns index job labels minus one. The evaluator recomputes all completion times with integer arithmetic and ignores any score claimed by the candidate. A copy of Taillard's original data and the current bounds table is in `data/source/`. These files are outside the candidate input allowlist.

Eric Taillard's official page lists a same-instance lower bound of 3771 and upper bound of 3846 for Ta051. The page says that only permutation schedules are allowed. It credits Va for the upper bound and Taillard for the lower bound. The page labels these as the current bounds as of 2026-06-03. The upper-bound witness is a permutation published by Ravetti, Riveros, Mendes, Resende, and Pardalos in 2012. An independent replay on Taillard's official matrix gives makespan 3846. This witness proves feasibility, not optimality. The current interval is 3771 to 3846.

Olivier Brunner's Zenodo v8 dataset (2026-01-16) also records the Ta051 upper-bound witness. The record was later updated to v11 (2026-07-31). Its page warns readers to use caution with the `Optimal` field. This task does not use that field to establish optimality. It cross-checks the open status against Taillard's official bounds table and Gmys's 2022 paper, which reports Ta051 as still open. Update the records and review the configuration if a better witness or an optimality proof is found.

Status: accepted by Sol on 2026-11-06.
