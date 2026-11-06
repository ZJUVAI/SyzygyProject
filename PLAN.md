# 项目计划

此文件是唯一的项目规划和研究结论入口。任务参数以各任务的 `task.json` 为准。公开来源保存在 `records.json`，SOTA 构造及复算信息保存在 `sota.json` 和 `data/`。自己的最佳构造保存在 `best/<配置ID>/`。

## 固定规则

- 保留20个任务，当前共35个配置。参数、种子与重复运行分别记录。已证明最优的配置退役，旧ID不复用。
- 每个配置有标量目标、方向、约束和同参数的人类构造对照。公开报告值与复算值分开。
- 正式成绩从构造独立重算。使用精确计算或保守区间。无效构造不计分。
- 简单起点和传统搜索不得读取对照见证。模型隔离实验与本地代码辅助搜索分开。
- 兼容分数采用冻结对照。超过对照不等于刷新公开纪录。跨任务汇总公式尚未冻结。
- 默认生成300秒、验证60秒、单线程。Linux地址空间限制4GiB；macOS记录未执行此限制。

## 当前状态

历史任务实现验收覆盖35个配置。完整模型对比实验尚未开展。服务器后续搜索已复核8个任务、14个配置；T009仅完成一个种子，仍待续跑。T005-C01另有接近所引公开值的独立结果。保留的最佳构造可在各任务的 `best/` 中重放。

| 任务 | 参数 | 后续搜索 |
|---|---|---|
| N001 | {"q": 7, "power": 5} | 待继续 |
| T001 | {"n": 26, "container": "unit square"}；{"n": 32, "container": "unit square"}；{"n": 50, "container": "unit square"} | 已复核 |
| T002 | {"n": 26}；{"n": 29}；{"n": 38} | 待继续 |
| T005 | {"n": 26, "container": "unit square", "radii": "variable"}；{"n": 32, "container": "unit square", "radii": "variable"} | C01已有独立结果 |
| T009 | {"n": 16, "space": "S2", "objective": "minimum pairwise angular separation in radians"}；{"n": 17, "space": "S2", "objective": "minimum pairwise angular separation in radians"}；{"n": 19, "space": "S2", "objective": "minimum pairwise angular separation in radians"} | 待继续 |
| T014 | {"n": 11}；{"n": 12}；{"n": 16} | 已复核 |
| T035 | {"degree": 4, "girth": 10} | 待继续 |
| T044 | {"marks": 29}；{"marks": 30}；{"marks": 32} | 待继续 |
| T057 | {"max_cardinality": 512, "integer_interval": [-1000000, 1000000]} | 待继续 |
| T060 | {"v": 24, "k": 14, "t": 4} | 待继续 |
| T066 | {"n": 68, "k": 15, "q": 2} | 待继续 |
| T067 | {"n": 17, "distance": 6} | 待继续 |
| T073 | {"L": 100}；{"L": 80}；{"L": 120} | 已复核 |
| T079 | {"steps": 208, "support": ["-1/4", "1/4"], "nonnegative": true} | 已复核 |
| T080 | {"steps": 20, "support": ["-1/4", "1/4"], "nonnegative": true} | 已复核 |
| T081 | {"steps": 208, "support": ["-1/4", "1/4"], "signed_values_allowed": true, "integral": 1} | 已复核 |
| T082 | {"steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1} | 已复核 |
| T089 | {"n": 29, "entries": "±1"} | 已复核 |
| T097 | {"target": "2^192-2^64-3"}；{"target": "2^221-5"}；{"target": "2^521-3"} | 待继续 |
| T099 | {"k": 343} | 待继续 |

## 待办

1. 在Mac原生Python3.13环境安装固定依赖，运行公共测试及任务测试。
2. 继续其余任务。每个配置保存构造、种子、预算、环境和重放命令。
3. 改善T073搜索算法后重新测量。现有best保留旧结果，尚未运行的新代码不算成绩。
4. 核对新结果与同参数公开来源，再由主代理验收。不得自动把程序运行成功标记为Sol验收。
5. 冻结跨配置汇总规则后，再开展隔离的完整模型比较。

## 已知限制

- T081已超过旧的非负208步对照。绝对峰值与正峰值是不同目标。公开更强报告还使用300、600、800步，不能当作208步结果。来源：https://github.com/teorth/optimizationproblems/blob/main/constants/1d.md 。
- T057开发代理曾意外显示human.py；不纳入隔离的冷启动模型比较。
- T009、T057的独立数值复算只作交叉检查，正式成绩仍采用验证器的精确或区间依据。
- 时间截断结果受机器速度影响。部分旧程序未输出迭代数。
- Mac实机尚未验证。服务器旧Python不满足最低版本，其4项T009测试因缺少math.nextafter失败；此前有效环境的完整测试通过。

## 维护方式

以后只在本文件更新计划、结论、状态和待办。不再维护research或reports。任务的机器可读参数、来源、见证和复算结果随任务代码更新。临时运行数据写入各任务的runs目录，不提交Git。原始研究及完整历史实验已移到仓库外备份。

## 上游接口

SimpleTES使用`mathbench/simpletes_evaluator.py`，对应T073-C01。DREAM-RSI使用`mathbench/dream_rsi_evaluator.py`，对应T005-C02。与对应任务的instruction.txt和init_program.py配套。这里只完成接口级验证，尚未运行完整上游模型实验。

## 本轮整理验证

15个保留的最佳构造通过独立进程严格重放。18项公共测试通过。全套202项测试中198项通过；4项T009测试仍因当前服务器Python3.8缺少math.nextafter失败。没有放宽数学检查来消除这些失败。
