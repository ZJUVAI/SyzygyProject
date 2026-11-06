# SyzygyProject

数学构造 benchmark，包含 20 个任务。任务定义和必要的基线见证位于 `tasks/`，评测运行器位于 `mathbench/`，研究记录位于 `research/`。

## 在 Mac 运行

安装并启动 Docker Desktop，然后运行：

```sh
docker build -t syzygy-mathbench .
docker run --rm --memory=4g --cpus=1 -v "$PWD:/work" syzygy-mathbench
```

默认按顺序搜索 T005 以外的 19 个任务。已有完整复核结果的任务会跳过。新克隆会重新生成结果。具体说明见 [MAC_RUN.md](MAC_RUN.md)。Docker 镜像尚未在 Mac 上验证。

## 开发

需要 Python 3.11 或更新版本。固定依赖见 `requirements-lock.txt`。

```sh
python3 -m pip install -r requirements-lock.txt
python3 -m mathbench list
python3 -m pytest tests tasks -q
```

生成的构造、日志、报告、截图和网页快照不纳入 Git。必要的基线见证用于验证和外部对照，予以保留。网站验证测试位于 `tests_optional/`，需要先重新生成网站和相关证据。

接口见 [tasks/CONTRACT.md](tasks/CONTRACT.md)，开发要求见 [AGENTS.md](AGENTS.md)。搜索反馈与正式数学验证分开。正式成绩由独立验证器从构造重算。
