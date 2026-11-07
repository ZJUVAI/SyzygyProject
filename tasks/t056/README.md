# T056：Taillard ta41 一般作业车间排程

## 中文

配置 `T056-C01` 固定为 Taillard 的 `ta41`，含 30 个工件、20 台机器。每个工件有自己的机器路线和加工时间。路线可以彼此不同。每台机器的加工顺序也分别决定。

目标是最小化最大完工时间。该任务是一般 job-shop，不是 permutation flow-shop。checker 从机器上的工件顺序构造精确的优先关系图，并以整数最长路计算最早完工时间；有环的顺序无效。

公开输入来自 Taillard 官方实例页的 `tai30_20.txt` 首个实例。该文件的旧上界字段已过时；本任务单独记录已验证的公开排程。Shylo 与 Pardalos 的 `ta41` 排程公开值为 2006，已下载并复算。最新核对到 2026-11-06 时，`optimizizer.com/TA.php` 仍列 2006 为上界，1912 为下界；2025 年 OR-Tools 论文还报告运行后数值下界 1915，但作者说明该下界没有形式化证明。没有查到 ta41 最优性闭合。

冻结弱人类方法基线为 3296。`human.py` 重建 Giffler–Thompson 活跃排程生成法，并在冲突集中采用最长加工时间规则。最佳公开排程 2006 与该弱基线分开记录。所有搜索从简单的机器内工件升序排程开始；搜索代码不读取 `data/reference/`。

## English

Configuration `T056-C01` fixes Taillard's `ta41` instance with 30 jobs and 20 machines. Each job has its own machine route and processing times. Job routes may differ. The processing order is chosen separately for each machine.

The objective is to minimize the makespan. This is a general job-shop problem, not a permutation flow-shop problem. The checker builds the exact precedence graph from job routes and machine orders, then computes earliest completion times with integer longest paths. A cyclic order is invalid.

The input is the first instance in Taillard's official `tai30_20.txt` file. Its old bound fields are stale. The task records a separately verified public schedule. Shylo and Pardalos report a `ta41` schedule with makespan 2006; the downloaded sequence was independently checked. As of 2026-11-06, `optimizizer.com/TA.php` still lists 2006 as the upper bound and 1912 as the lower bound. A 2025 OR-Tools paper reports a numerical lower bound of 1915 after a long run, but it does not provide a formal proof for that bound. No proof closing `ta41` was found.

The frozen weak human method baseline is 3296. `human.py` reconstructs Giffler–Thompson active-schedule generation and uses a longest-processing-time rule within the conflict set. The best public schedule at 2006 is recorded separately. All search starts from the simple machine-order schedule sorted by job index. Search code does not read `data/reference/`.
