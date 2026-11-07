# T063: degree-100 Mahler measure

## 中文

### 数学目标与配置

给定整数多项式

\[
P(x)=a_0+a_1x+\cdots+a_{100}x^{100},
\]

求一个**恰为 100 次**、本原、在 \(\mathbb Q[x]\) 上不可约且非分圆的多项式，使 Mahler 测度

\[
M(P)=|a_{100}|\prod_{P(z)=0}\max(1,|z|)
\]

尽量小。系数不预先限制为互反、稀疏或单首项。此配置不声称已证明最优。

唯一配置 `T063-C01` 固定次数 100。候选须提交从常数项到最高次项的 101 个整数系数，以及 100 个复平面有理圆盘。检查器精确核对系数本原性和不可约性。每个圆盘用 Rouché 定理认证恰含一个根，所有圆盘两两分离，故覆盖全部根。计算各根模长的有理上下界并相乘，返回 Mahler 测度区间的上端作为最小化目标。区间相对宽度不得超过 `1e-10`；浮点根只可用于生成候选圆心，不能作为正式分数。圆盘有理数不设精度上限，统一运行器对候选输出实施 16 MiB、4 GiB 和 60 秒验证限制。

### 来源和公开纪录

Mossinghoff 的固定仓库提交 `7e3798516710370a758e16eb5de6bccbee98bb6a` 中，`BestByDegree_200.txt` 的恰 100 次一行给出报告值 `1.247365098370`、`v=8` 和 51 个互反系数。`data/source/mossinghoff_degree_100_row.json` 保存该原始行及仓库固定版本。`data/reference/mossinghoff_degree_100_certificate.json` 保存展开的多项式和 100 个有理根圆盘。当前精确复核的保守测度上界约为 `1.2473650983705`。

Chervonyi、Gukov、Luong 的 arXiv:2610.30277v1（2026-10-21）报告：对 91 个已有文献数据匹配 85 个，仅在次数 178、188、190、202、242、250 报告严格改进；次数 100 不在改进列表中。论文介绍整体人机协作流程，但未把 100 次这一旧记录归因于该流程。来源没有证明次数 100 的最优性；论文也指出逐次数最优性证明仅覆盖到次数 54。此处把 Mossinghoff 项作为已复现的历史人类方法/公开对照，并披露其逐项搜索过程未详述。

### 程序和运行

- `check.py`：精确验证数据、不可约性、100 个根圆盘、根覆盖及 Mahler 测度区间。
- `init_program.py`：独立简单起点 \(x^{100}-2\)。它用显式单位根近似建议圆心；有理圆盘仍须通过精确检查。
- `baseline.py`：固定迭代枚举 Eisenstein 多项式 \(x^{100}-p\)，其中 \(p\) 为素数。该族中 Mahler 测度恰为 \(p\)，作为传统有限搜索基线。它不读取比较数据。
- `evolution.py`：在同一族上作确定种子的常数项变异与精英选择。默认 60 代、4 次重启；可用 `MATHBENCH_EVOLUTION_ITERATIONS`、`MATHBENCH_RESTARTS` 调整，硬上限分别为 300、20。该简化搜索是任务内传统搜索演示，不是对称/稀疏系数空间的全域搜索。
- `human.py`：从已固定的 Mossinghoff 见证数据复现同次数公开人类记录。
- `reference.py`：固定复播相同公开记录，用于 SOTA 档案。

五个入口均定义 `run_code()`，读取 `MATHBENCH_CONFIG_ID` 与 `MATHBENCH_SEED`。默认传统搜索使用固定迭代数；设 `MATHBENCH_SEARCH_SECONDS` 时由共享 `search_steps` 提供探索用时截断。评测器另按公共接口限制生成 300 秒、验证 60 秒、内存 4 GiB、一个线程。初始程序与搜索程序不加载 `data/reference/` 或 `data/source/`。

### 复核方式

运行：

```sh
.venv/bin/python -m pytest tasks/t063 -q
.venv/bin/python -m json.tool tasks/t063/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/records.json > /dev/null
```

测试验证起点和公开根证书，破坏系数、破坏根盘、重复根盘、bool/浮点/NaN 系数、边界次数、伪造分数不变性，以及工作进程异常和超时。独立关键量包括 100 个根圆盘、两两分离检查数 `4950`、精确不可约性、区间相对宽度与源文件哈希。基准仍需 Sol 独立复核。

## English

### Definition and fixed configuration

For an integer polynomial \(P(x)=\sum_{k=0}^{100}a_kx^k\), minimize

\[
M(P)=|a_{100}|\prod_{P(z)=0}\max(1,|z|)
\]

over primitive, irreducible, non-cyclotomic polynomials of **exact degree 100**. Coefficients are not restricted to reciprocal or sparse forms, and need not be monic. This task does not claim an optimality proof.

The only configuration is `T063-C01`, degree 100. A candidate contains 101 integer coefficients in ascending order and 100 rational complex disks. The checker proves primitiveness and irreducibility exactly. It certifies one root in each disk with Rouché's theorem, checks that all disks are pairwise disjoint, and bounds the complete root product with rational arithmetic. It returns the upper endpoint as the minimization objective. The relative width of the certified interval must be at most `1e-10`. Floating-point roots may propose disk centers, but they never determine the score. Rational disk precision has no fixed ceiling; the common runner applies the 16-MiB output, 4-GiB memory, and 60-second verification limits.

### Sources and public result

The degree-100 row in `BestByDegree_200.txt` at Mossinghoff's pinned repository commit `7e3798516710370a758e16eb5de6bccbee98bb6a` reports `1.247365098370`, `v=8`, and 51 reciprocal coefficients. The source row and pin are recorded in `data/source/mossinghoff_degree_100_row.json`. The expanded polynomial and its 100 rational root disks are in `data/reference/mossinghoff_degree_100_certificate.json`. The current exact certificate gives a conservative upper bound near `1.2473650983705`.

Chervonyi, Gukov, and Luong, arXiv:2610.30277v1 (2026-10-21), report matching 85 of 91 published literature values and strict improvements at degrees 178, 188, 190, 202, 242, and 250. Degree 100 is not among the listed improvements. Their paper describes project-level human-AI work but does not attribute this older degree-100 entry to that workflow. The degree-100 minimum remains open; the paper says degree-wise optimality has only been proved through degree 54. This task records the Mossinghoff entry as a reproduced historical human/public result and states that the source does not give a detailed per-entry search method.

### Programs and budget

- `check.py` validates integer data, irreducibility, all root disks, root coverage, and a rational Mahler interval.
- `init_program.py` starts from \(x^{100}-2\). Explicit root approximations only propose centers; exact disk checks decide validity.
- `baseline.py` scans a fixed number of Eisenstein polynomials \(x^{100}-p\), with prime \(p\). In this family the Mahler measure is exactly \(p\). It does not read comparison data.
- `evolution.py` uses seeded coefficient mutation and elitist selection in the same family. Defaults are 60 generations and 4 restarts. `MATHBENCH_EVOLUTION_ITERATIONS` and `MATHBENCH_RESTARTS` set bounded alternatives (maximum 300 and 20). This is a simple traditional-search baseline, not a global search over all degree-100 polynomials.
- `human.py` rebuilds the pinned Mossinghoff witness.
- `reference.py` replays the same public witness for the SOTA record.

All five entries define `run_code()` and read `MATHBENCH_CONFIG_ID` and `MATHBENCH_SEED`. Search defaults use fixed iteration counts. `MATHBENCH_SEARCH_SECONDS` enables the shared exploration cutoff. The evaluator uses the common 300-second generation, 60-second verification, 4-GiB memory, and one-thread limits. The seed and search programs do not load comparison assets from `data/`.

### Validation

Run:

```sh
.venv/bin/python -m pytest tasks/t063 -q
.venv/bin/python -m json.tool tasks/t063/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t063/records.json > /dev/null
```

Tests cover valid and damaged polynomials, damaged and duplicate disks, bool/float/NaN coefficients, degree boundaries, ignored claimed scores, and worker errors and timeouts. Independent quantities include all 100 certified disks, 4,950 pairwise separation checks, exact irreducibility, interval width, and the pinned source hash. Sol review is pending.
