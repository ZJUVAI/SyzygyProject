# T055：部分 MaxSAT 实例

## 定义与固定参数

MaxSAT 输入是加权合取范式。硬子句必须全部满足；目标是最大化满足的软子句权重。

配置 `T055-C01` 固定 MSE 2026 实例 `b4794d123e18a908924d3d33cdeeae3b`，属于 `inconsistency-measurement`。它有 1630 个变量、6150 个硬子句和 649 个权重为 1 的软单位子句。输出是按变量 `1,...,1630` 排列的布尔数组。目标分数为满足软子句权重，最大值 649。官方以未满足软权重报告成本；成本 62 对应本任务分数 587。

`check.py` 从固定 WCNF 精确检查所有硬、软子句。它拒绝违反硬子句的赋值，并重新计算软权重；不使用候选自报分数。

## 来源与记录

原始规范化实例保存在 `data/source/`，SHA-256 为 `cd81f483b6cc3d05e9760274eee7697d9cc0f0a5a7146d3c6887af687d149195`。实例元数据来自 MSE 2026 完整基准集 Zenodo 记录 21283148。比赛结果和解算器日志来自 MSE 2026 Zenodo 记录 21358014（v1，2026-07-14）。

输入采用 MSE `std_wcnf` 格式：硬子句行以 `h` 开头，软子句行以正权重开头，并以 `0` 结束。

官方 `ANYTIME-UW` 60 秒赛道的 BouMS 日志给出未满足软成本 62，完成文件标记 `VERIFIED`。日志索引位置和 CRC、完整 assignment 及其 SHA-256 均记录在 `sota.json`。我们从日志中提取 assignment，并独立检查全部 6150 个硬子句和 649 个软子句，得到分数 587。比赛元数据显示最优成本未知，因此该实例仍未证明最优。公开日志没有说明 BouMS 或这次运行是否使用 AI，AI 来源标记为未知。

冻结人类基线为分数 360。`human.py` 对所有硬子句运行传统 DPLL 可满足性方法，再做精确的硬约束可行单变量软分数改进。DPLL 的方法来源为 Davis、Logemann 和 Loveland 1962 年论文；SymPy 1.14.0 提供本次可重放的实现。该 360 是本地复现的方法基线，不是比赛公开纪录。初始程序也从硬子句重新运行 DPLL，不读取人类或纪录见证。

## 程序与搜索

- `init_program.py` 独立解析公开 WCNF，只对硬子句运行 DPLL，产生有效起点。
- `baseline.py` 从硬可行赋值开始，按固定种子做随机块翻转，只保留硬可行解并更新最好软分数。
- `evolution.py` 从硬可行赋值建立小型种群，做有界块变异并精确过滤硬约束。
- `human.py` 重建传统 DPLL 硬可行赋值并做单变量贪心改进。
- `reference.py` 重放固定的 MSE 2026 BouMS 官方解。
- 搜索默认以固定迭代数运行，种子来自 `MATHBENCH_SEED`。默认每次生成限时 300 秒，验证另限时 60 秒，内存 4 GiB，一个计算线程。`MATHBENCH_SEARCH_SECONDS` 可显式启用按时长截断。
- 传统搜索和初始程序只读取公开公式，不读取比较 assignment。比较文件应放在模型上下文之外。

## 检查

从仓库根目录运行：

```sh
.venv/bin/python -m pytest tasks/t055/test_task.py -q
.venv/bin/python -m json.tool tasks/t055/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t055/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t055/records.json > /dev/null
```

状态：已通过 Sol 验收（2026-11-06）。

---

# T055: Partial MaxSAT instance

## Definition and fixed parameters

A MaxSAT input is a weighted conjunctive normal form. Every hard clause must be true. The objective is to maximize the total weight of satisfied soft clauses.

Configuration `T055-C01` fixes the MSE 2026 instance `b4794d123e18a908924d3d33cdeeae3b` from the `inconsistency-measurement` family. It has 1630 variables, 6150 hard clauses, and 649 soft unit clauses of weight 1. The output is a Boolean array ordered by variables `1,...,1630`. The score is the satisfied soft weight, with maximum 649. The official benchmark reports unsatisfied soft cost; cost 62 corresponds to our score 587.

`check.py` reads the fixed WCNF and checks every hard and soft clause exactly. It rejects assignments that violate a hard clause and recomputes the soft weight. It ignores any score claimed by the candidate.

## Sources and results

The normalized source instance is saved under `data/source/`. Its SHA-256 is `cd81f483b6cc3d05e9760274eee7697d9cc0f0a5a7146d3c6887af687d149195`. Instance metadata comes from the MSE 2026 complete benchmark collection, Zenodo record 21283148. Competition results and solver logs come from MSE 2026 Zenodo record 21358014, v1, published 2026-07-14.

The input uses the MSE `std_wcnf` format: hard-clause lines start with `h`; soft-clause lines start with a positive weight. Each line ends with `0`.

The official BouMS log in the `ANYTIME-UW` 60-second track reports unsatisfied soft cost 62, and the completion file says `VERIFIED`. The log index offset and CRC, the complete assignment, and its SHA-256 are saved in `sota.json`. We extracted the assignment and independently checked all 6150 hard clauses and 649 soft clauses. The resulting score is 587. The competition metadata lists the optimum cost as unknown, so optimality is open. The official release does not state whether AI contributed to BouMS or this run; AI provenance is recorded as unknown.

The frozen human baseline is 360. `human.py` runs the traditional DPLL satisfiability method on the hard clauses, then performs exact single-variable soft-score improvements that preserve every hard clause. The method source is the 1962 paper by Davis, Logemann, and Loveland; SymPy 1.14.0 supplies the replayable implementation. The value 360 is a locally reproduced method baseline, not a published competition record. The initial program also runs DPLL on the hard clauses and does not read any comparison witness.

## Programs and search

- `init_program.py` parses the public WCNF on its own and runs DPLL on the hard clauses to make a valid starting assignment.
- `baseline.py` starts from a hard-feasible assignment and applies fixed-seed random block flips. It keeps only hard-feasible assignments and retains the best soft score.
- `evolution.py` builds a small population from a hard-feasible assignment, mutates bounded blocks, and filters each candidate against every hard clause.
- `human.py` rebuilds a traditional DPLL assignment and applies greedy single-variable improvements.
- `reference.py` replays the fixed MSE 2026 BouMS assignment.
- Searches use a fixed iteration count by default and read the seed from `MATHBENCH_SEED`. Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one compute thread. Set `MATHBENCH_SEARCH_SECONDS` to use a wall-clock cutoff.
- The seed and search programs read only the public formula. They do not read comparison assignments. Keep those files outside the model context.

## Checks

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t055/test_task.py -q
.venv/bin/python -m json.tool tasks/t055/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t055/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t055/records.json > /dev/null
```

Status: accepted by Sol on 2026-11-06.
