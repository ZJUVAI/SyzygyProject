# T100 实现记录

## 冻结配置

- ID：`T100-C01`
- 图：50 个标记顶点，700 条简单无向边。
- 目标：最小化三角形数。
- 方向：minimize；比较基线 1,817。
- 状态：`accepted_by_sol`。

## 来源、固定参数与开放状态

主数学来源为 Hong Liu、Oleg Pikhurko、Katherine Staden，*The exact minimum number of triangles in graphs of given order and size*, arXiv:1712.00633v2 (2020)，Definition 1.1、Theorem 1.9、Conjecture 1.11: <https://arxiv.org/html/1712.00633v2>。期刊版 DOI 为 <https://doi.org/10.1017/fmp.2020.7>。定义 1.1 给出有限构造 `H*`。在 `(n,e)=(50,700)`，其分部大小为 `(23,23,4)`，完全三部图有 `529+92+92=713` 条边。删去小部单个顶点到大小 23 的一部中 13 个顶点的边后，留下 700 条边。每条所删边消去 23 个不同三角形，因此构造恰有 `23*23*4 - 13*23 = 1817` 个三角形。

Theorem 1.9 只证明充分大 `n` 的结果，且其 `n0` 未给出；不能据此宣称本例已解决。Conjecture 1.11 才是所有有限 `(n,e)` 的猜想。

2026-11-07 检索的较新来源包括 Liu 和 Pikhurko, *A note on extremal constructions for the Erdős–Rademacher problem*, arXiv:2311.18753v2（最后修订 2024-10-07；2025 年期刊版）: <https://arxiv.org/abs/2311.18753v2>。该文摘要和引言讨论 `r>=4` 的修订构造猜想，没有给出 `r=3,n=50,e=700` 的有限最优性证明。Li、Feng、Peng 的 Lovász–Simonovits supersaturation 文章 arXiv:2408.01709v2（2026-03-18 修订）<https://arxiv.org/abs/2408.01709v2> 仍叙述严格条件 `q<n/2`。`n=40,e=420` 的边界 `q=n/2` 不在该严格版本覆盖范围内；本任务 `q=75` 远超边界。

题包页面 <https://zerothesis.com/challenges/min-triangles-fixed-edges?tab=brief> 在 2026-11-07 标记 `(50,700)` 的 1,817 构造为 “no; conjectured”。同日获取的 API JSON SHA-256 为 `77f2aba338edc73c3447f8b3256a869d307206d53002332e01763dd41b821860`，缓存于 `runs/zerothesis_pack_20261107.json`。HTML 页面 SHA-256 为 `9c65310a04e1596a0cc2f5e78677493547c26a5680da1ecf9e3eb5e0798cfcba`。该包声称 LPS 构造已在充分大参数证明、对本行仍属猜想；它是参数状态的补充快照，数学重建以论文定义为准。

LPS Theorem 1.2 与 blow-up argument 给出连续密度下界。这里 `lambda=2e/n^2=14/25`。Razborov 的精确密度公式给出 `g3(14/25)=98/1125`，因此本例放大下界为 `n^3/6 * g3(14/25)=49000/27`。由整数性得下界 1,815。当前来源未判定最优值是 1,815、1,816 还是 1,817。

## 实现与对照隔离

- `check.py` 检查精确顶点数、边数、简单无向图约束，并用位集枚举每个三角形一次。候选声明的成绩字段不会影响验证结果。
- `init_program.py` 输出按词典序的前 700 条边；它不导入任务模块，也不读取任何对照数据。
- `baseline.py` 从固定随机种子的一般 700 边图开始，用贪心换边及周期扰动搜索。默认 5,000 步。
- `evolution.py` 从独立随机图进行模拟退火换边。默认 10,000 步。两种搜索都在任意图空间中提案，不使用 `H*` 构造或比较文件。
- `human.py` 按 LPS Definition 1.1 重建 `H*`。独立精确检查得分 1,817。
- `reference.py` 读取冻结的 `data/reference/hstar_50_700.json`。它不读取 `best/`。
- 默认生成限时 300 秒，验证限时 60 秒，4 GiB 和单线程由公共运行器管理。

## 局限

本地复现了论文给出的可行构造，没有证明 1,817 是全局最优值。题包状态和文献核查均有固定时间点，但文献检索不是穷尽证明。放大下界与近 Mantel 定理未闭合该参数。

## 验证记录

使用 Python 3.13.12，Linux x86_64，运行 `.venv/bin/python -m pytest tasks/t100/test_task.py -q`：25 项通过。测试直接调用五个 `run_code()` 入口，并将每个输出交给正式检查器。测试还用独立的 `trace(A^3)/6` 重算构造三角形数，拒绝错误配置、错误边数、自环、重复边、布尔端点、浮点端点、非有限值和越界端点，并确认伪造 `objective`、`score`、`claimed_score` 不改变整份验证结果。通过 `mathbench.evaluate._run` 检查工作进程错误和超时；再临时替换加载配置和任务目录的查找函数，实际调用任务的 `evaluate()` 适配器，用完整配置严格评估冻结参考并得到分数 1。测试不修改永久注册表。

默认固定预算的本机试跑：传统搜索 5,000 次交换，用时 6.536 秒，返回图三角形数 2,444；演化搜索 10,000 次交换，用时 22.483 秒，返回图三角形数 3,414。耗时依赖机器。命令：

```sh
.venv/bin/python - <<'PY'
import os
from tasks.t100.baseline import run_code as baseline
from tasks.t100.evolution import run_code as evolution
os.environ["MATHBENCH_CONFIG_ID"] = "T100-C01"
print(baseline()["search"])
print(evolution()["search"])
PY
```
