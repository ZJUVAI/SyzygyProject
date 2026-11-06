# SyzygyProject

数学构造 benchmark，包含 20 个任务。

- `tasks/`：任务定义、搜索程序、独立验证器和必要的基线见证。
- `mathbench/`：公共运行器和评测接口。
- `scripts/`：搜索入口及验收工具。
- `tests/`：公共测试。任务测试与各任务放在一起。
- `research/`：参数选型和来源记录。

## 安装

Mac 和 Linux 均使用 Python 3.11 或更新版本，无需 Docker。建议使用 Python 3.13。

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
```

## 搜索

```sh
python scripts/search.py resume          # 顺序运行 T005 以外的 19 个任务
python scripts/search.py run T073        # 单独运行一个任务
python scripts/search.py summary         # 汇总已有结果
python scripts/search.py audit           # 检查已有结果
```

完整任务已有复核记录时，续跑会跳过它。中断任务会在新目录重跑全部配置。已有文件不会覆盖。每个配置使用两个种子，每次搜索目标时间为 45 秒。生成上限为 300 秒，验证上限为 60 秒，数值库使用一个线程。

Linux 工作进程限制地址空间为 4 GiB。macOS 不执行此内存限制，结果的 `environment.memory_limit_enforced` 会记录为 `false`。两种平台均由独立验证器重算数学成绩。本次修改尚未在 Mac 实机上验证。

结果写入 `reports/remaining_search/`，不纳入 Git。冻结比较输入 `reports/sota_acceptance.json` 和必要的基线见证予以保留。服务器旧结果仍在原服务器及迁移包中；新克隆会重新生成结果。

## 验证

```sh
python -m mathbench list
python -m pytest tests tasks -q
```

接口见 [tasks/CONTRACT.md](tasks/CONTRACT.md)，项目要求见 [AGENTS.md](AGENTS.md)。研究选型见 [research/configuration_selection.md](research/configuration_selection.md)。
