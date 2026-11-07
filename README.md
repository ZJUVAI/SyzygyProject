# SyzygyProject v1.0

正式数学构造 benchmark 包含 100 个任务、139 个配置。入选名单和筛选依据见 [PLAN.md](PLAN.md#正式目录筛选100题)。

- `tasks/`：任务定义、搜索程序、独立验证器和必要的基线见证。
- `mathbench/`：公共运行器和评测接口。
- `scripts/`：搜索、验收、成绩表和网站数据更新入口。独立数学复算模块在 `scripts/audits/`。
- `tests/`：公共测试。任务测试与各任务放在一起。
- `PLAN.md`：统一维护计划、研究结论和待办。

## 安装

Mac 和 Linux 均使用 Python 3.11 或更新版本，无需 Docker。建议使用 Python 3.13。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
```

## 任务编号

正式任务编号为 `T001`–`T100`。每题的配置从 `C01` 开始。运行 `python -m mathbench list` 查看任务。

## 搜索

```sh
python scripts/search.py resume          # 顺序续跑已验收的任务配置
python scripts/search.py run T013        # 单独运行一个任务
python scripts/search.py summary         # 汇总已有结果
python scripts/search.py audit           # 检查已有结果
python scripts/result_table.py --highlight-best  # 四列成绩，粗体与🏆标记行内最好值
python scripts/search.py run T013 --label _long --seconds 180 --baseline-seconds 30 --seeds 0 1
```

完整任务已有复核记录时，续跑会跳过它。中断任务会在新目录重跑全部配置。已有文件不会覆盖。每个配置使用两个种子，每次搜索目标时间为 45 秒。生成上限为 300 秒，验证上限为 60 秒，数值库使用一个线程。

`--seconds` 可显式增加演化搜索预算，上限为 240 秒。`--baseline-seconds` 单独设置传统搜索预算。`--config` 可重复指定配置。Linux 可用 `--cpu` 指定一个可用 CPU。运行器把已有自有最佳构造复制到运行目录，并仅向演化程序传入 `MATHBENCH_WARM_START`；支持此变量的程序可继续搜索。续搜结果与隔离的冷启动模型比较分开报告。

四列表依次显示初始程序、自有已验证最佳搜索结果、公开构造的复算值、来源报告的最好值。报告值没有见证时，与复算值分别显示。表中小数仅用于显示，原始精确值保存在 JSON 记录中。

Linux 工作进程限制地址空间为 4 GiB。macOS 不执行此内存限制，结果的 `environment.memory_limit_enforced` 会记录为 `false`。两种平台均由独立验证器重算数学成绩。本次修改尚未在 Mac 实机上验证。

临时结果写入各任务的 `runs/`，不上传。每个任务的 `sota.json` 保存公开结果、来源和验证信息，`data/` 保存必要见证。自己的最佳构造保存在 `best/<配置ID>/`，可以直接重放。

## 验证

T011、T006、T012、T008、T010 和 T013 的演化搜索使用 C++17 内核，需要可执行的 `g++`。编译计入生成预算，源码及编译器版本记入运行档案。重放已保存的 JSON 构造只需 Python，不需要编译器。

```sh
python -m mathbench list
python -m pytest tests tasks -q
```

接口见 [tasks/CONTRACT.md](tasks/CONTRACT.md)，项目要求见 [AGENTS.md](AGENTS.md)。计划与状态只更新 [PLAN.md](PLAN.md)。

搜索表中的数值接近项使用 `≈`，不把末位变化解释为突破纪录。验收工具的 `--candidate-only` 仅验证所选合法构造，保留其他候选或对照的失败状态，不把整轮实验记为通过。
