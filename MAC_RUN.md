# 在 Mac 继续运行

## 当前数据

服务器已完成并复核 8 个任务、14 个配置。GitHub 精简版不含这些生成结果；本地续跑会重新生成结果。另有 T009-C02 的第一种子构造，尚未完成该任务验收。服务器进程已中断。历史失败尝试保留在结果目录中。完整状态见 `reports/remaining_search/summary.json`，逐次检查见 `reports/remaining_search/audit.json`。失败导入记录不算已完成配置。

T081 已超过冻结对照，但没有建立公开纪录。最新来源核对见 `reports/remaining_search/public_comparison_notes.json`。

## 推荐运行方式

安装并启动 Docker Desktop。在项目根目录运行：

```sh
docker build -t syzygy-mathbench .
docker run --rm --memory=4g --cpus=1 -v "$PWD:/work" syzygy-mathbench
```

入口按顺序处理剩余任务。本地已有已复核配置的完整任务会跳过；全新克隆会运行全部 19 个任务。未完成的任务在新目录重跑全部配置。旧文件不会覆盖。每个配置运行两个种子。每次搜索目标时间为 45 秒，生成上限为 300 秒，验证上限为 60 秒。

Docker 路径用于保留 Linux 运行器。此服务器无法验证 Docker Desktop 或 Apple Silicon 上的实际运行。首次构建需网络。依赖按 `requirements-lock.txt` 安装。

查看已保存结果，无需重新搜索：

```sh
python3 scripts/summarize_remaining_search.py
```

Linux 运行器使用 `resource` 和进程资源限制。没有在原生 macOS 上验证这些限制。不要将本次实验当作隔离的模型比较。部分程序未输出迭代计数；预算、种子、构造和重放成绩已保存。时间截断结果会受机器速度影响。

## 仓库范围

GitHub 保留运行器、搜索程序、任务定义、必要的人类基线见证及测试。生成报告、截图、网页快照和旧队列脚本不上传。冻结比较表 `reports/sota_acceptance.json` 是汇总器的输入，予以保留。网站验证放在 `tests_optional`，仅在重新生成网站及证据后运行。
