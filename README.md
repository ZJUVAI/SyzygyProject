# Syzygy Mathbench

数学构造程序 benchmark。首批已完成 10 个类别、20 个任务、35 个固定配置，均通过 Sol 验收。
任务研究见 [研究目录](research/README.md)，实现要求见 [任务接口](tasks/CONTRACT.md)。

本轮由7个Luna任务代理实现14个新增配置，Sol逐配置验收。每题1–3个配置。
完整参数与来源见[配置选型](research/configuration_selection.md)，新增成绩见[扩展报告](reports/configuration_expansion.md)。
项目要求见[AGENTS.md](AGENTS.md)。

## 使用

```sh
python3 -m pip install -r requirements-lock.txt
python3 -m pip install -e '.[test]'
python3 -m mathbench list
python3 -m mathbench evaluate T073 tasks/t073/init_program.py --strict
python3 -m mathbench evaluate T005 tasks/t005/baseline.py --config T005-C02 --strict --output runs/example
python3 -m pytest
python3 -m mathbench replay T073 reports/witnesses/T073/T073-C01/human/solution.json
python3 -m mathbench export-seed T005 /tmp/t005-cold --config T005-C02
```

`run_code()` 输出构造。评测器独立验证数据并重算数学指标。
最大化任务兼容分数为结果除以冻结的人类基线；最小化任务为基线除以结果。
无效结果分数为零，原始目标值为空。目标值、有效性和验证状态一并报告。

需要 Python 3.11 或更新版本。此前已验证环境为 `.venv`。当前服务器的虚拟环境解释器已失效；迁移时须重新安装环境，或按 [Mac 运行说明](MAC_RUN.md) 使用 Docker。
默认生成预算为 300 秒，验证预算为 60 秒，内存为 4 GiB。数值库使用一个线程，Linux工作进程固定到一个允许的CPU。
运行器通过子进程限制资源；它不提供操作系统安全容器。

## 实验材料

本项目搜索改进见 [独立结果库](reports/own_results.json)。T005-C01 的半径和达到 2.635983084917607783…，已通过精确复算。该结果接近所引公开严格值。其余 19 个任务的搜索建议见 [优先级评审](reports/search_priorities.md)。目前已复核其余任务中的 8 个任务、14 个配置。结果见 [搜索汇总](reports/remaining_search/README.md)。服务器中断后的续跑方式见 [Mac 运行说明](MAC_RUN.md)。

被测系统只接收 `instruction.txt`、`init_program.py`、公共接口和评测反馈。
`human.py`、`reference.py`、纪录档案及其数据只用于外部对照，不放入模型初始上下文。
初始程序和传统搜索程序不得读取参考见证。实验操作者应将对照资产放在被测系统无法访问的位置。
`export-seed` 只导出模型指令、初始程序、固定参数及必要的种子辅助代码。
传统搜索默认采用固定迭代次数与随机种子。显式设置 `MATHBENCH_SEARCH_SECONDS` 后可按时间截断；该模式的结果会受机器速度影响。

程序运行结束后，可信验证器读取构造数据。候选程序自行声明的分数不参与评分。
`--output` 保存构造、验证结果和运行元数据。`--strict` 要求精确或经过认证的验证结果。
数值快验可提供搜索反馈，但不能作为正式数学证书。

## 实现状态

研究中的“通过选型”与实现验收分开。每个任务均由一个独立 Luna 代理实现，再由 Sol 主代理验收。完成状态为 `accepted_by_sol`。
详见[验收报告](reports/acceptance.md)、[逐配置结果](reports/acceptance.json)及[独立复算](reports/independent_audit.json)。保存的构造及验证记录位于 `reports/witnesses/`。

187项测试、15项子测试、140次严格程序运行通过。35个配置完成独立关键量复算、破坏样例拒绝和声明分数无效检查。两个上游接入示例通过接口级验证。完整模型对比实验尚未开展。

部分人类方法对照弱于公开纪录。T060使用62块对照，T066使用距离8对照，T067使用128码字对照。公开23块、距离24和258码字的见证仍未复现。T009采用16、17、19点配置，排除已获最优性证明的15点配置。T002采用26、29、38个正方形；17个配置因公开最优性证明报告退役。所有差异均在报告中单列。
