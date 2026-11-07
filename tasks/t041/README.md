# T041：单位正方形中的 17 个可旋转正方形

## 数学定义

在闭单位正方形 `[0,1]²` 内放置恰好 17 个正方形。边长可以不同，方向不受限制。任意两块的内部不得相交；边界接触合法。目标是最大化 17 个边长之和。

固定配置为 `T041-C01`。成绩是精确重算的边长和。冻结对照 `H=4` 来自 4×4 网格并将一格分成两块边长 `1/8` 的正方形。兼容分数为 `J/H`。分数超过 1 只表示超过这个冻结对照。

## 程序接口

`run_code()` 返回 `{"squares": [...]}`。每块正方形用精确有理数中心 `(x,y)`、正边长 `side` 和单位边方向 `(cos,sin)` 表示。验证器要求 `cos²+sin²=1`，按精确有理数计算四角、容器约束、136 个分离轴测试和目标值。边界相切合法。候选分数声明会被忽略。

输入使用有理数，是为了让每个结果都能精确复算。有理单位方向在单位圆上稠密。将任意合法装填的每块边长略微缩小，可以给墙边和方块之间留出严格间隙；之后可用有理中心、边长和有理单位方向作足够小的扰动。因此此精确输入格式保留原问题的上确界。

模型起点在 `init_program.py`。它把 17 个边长 `1/17` 的方块排成一行，得分为 1。`baseline.py` 穷举 4×4 网格中可分割的格子和两种分割方向。`human.py` 从公式重建人类方法对照。`reference.py` 回放公开的固定有理构造。起点和搜索程序不读取对照数据。

## 来源与当前证据

人类方法对照是 15 个边长 `1/4` 的格子和 2 个边长 `1/8` 的格子，边长和恰为 4。Erdős–Graham 1975 论文研究等方格装填方法；本任务保存的 17 块坐标是我们按网格和单格细分公式重建的见证，不声称是该论文的原始坐标或最佳记录。

固定公开构造来自 [Sprite143/erdos-106-counterexample](https://github.com/Sprite143/erdos-106-counterexample)，固定提交 `edbfb534e78d4f1f9b1a5a7298b9b022285b4962`。该仓库给出闭式构造和精确有理坐标，声称边长和为 `2190452873/547596200`。本任务验证器独立重算完整的 17 块构造。原始搜索证书中的较低数值 `2000062156200269/500000000000000` 单独存档，不与闭式构造值混淆。

2026-11-06 检索到 ProbXiv 的问题记录把该构造标为 AI-assisted，并称 Claude Opus 5 发现；页面说尚无人员检查。它同时记录一份机器检查的 Lean formalization，并提示 Lean 检查形式化本身，不检查它是否等价于网页陈述。GitHub 仓库也称尚未经过人类审稿。故公开结果按 AI 辅助、未同行评审、任务内精确复算记录；不称为人类结果或最优值。

AlphaEvolve 论文 §6.35 报告其在 `n=17` 找到值 4。这是搜索结果，不是上界证明。Baek、Koizumi 与 Ueoro 的已证明结果针对轴平行正方形，不限制本任务的任意旋转版本。当前已保存公开构造给出下界 `2190452873/547596200`；面积约束和 Cauchy–Schwarz 给出上界 `√17`。没有找到两者相等的上界证明，因此不声称最优。

## 资源和状态

生成预算 300 秒，验证预算 60 秒，内存 4 GiB，单线程。精确验证使用 17 块正方形的有理数运算。当前状态：**已通过 Sol 验收（2026-11-06）**。验证命令及限制见 `IMPLEMENTATION.md`。

# T041: 17 rotatable squares in the unit square

## Definition

Place exactly 17 squares in the closed unit square `[0,1]^2`. Side lengths may differ and orientations are unrestricted. The interiors of distinct squares must be disjoint. Boundary contact is allowed. Maximize the sum of the 17 side lengths.

The fixed configuration is `T041-C01`. The score is the exact recomputed sum. The frozen comparison is `H=4`, from a 4 by 4 grid with one cell replaced by two squares of side `1/8`. The compatibility score is `J/H`. A score above 1 means only that it exceeds this frozen comparison.

## Program interface

`run_code()` returns `{"squares": [...]}`. Each square uses an exact rational centre `(x,y)`, positive side length `side`, and unit edge direction `(cos,sin)`. The checker requires `cos²+sin²=1`, then checks all four corners, containment, all 136 separating-axis pairs, and the objective with exact rational arithmetic. Boundary contact is legal. The checker ignores any candidate score claim.

Rational input lets the checker replay each result exactly. Rational unit directions are dense on the unit circle. Shrinking the squares in any feasible packing by an arbitrarily small amount creates positive wall and pair gaps; sufficiently small rational perturbations of centres, sides, and unit directions preserve feasibility. Thus this exact input format preserves the supremum of the unrestricted problem.

The model seed is `init_program.py`. It places 17 squares of side `1/17` in one row and scores 1. `baseline.py` enumerates the 16 choices of split cell and two split directions in a 4 by 4 grid. `human.py` rebuilds the human-method comparison from its formula. `reference.py` replays the fixed public rational construction. The seed and search code do not read comparison data.

## Sources and evidence

The human-method comparison has fifteen squares of side `1/4` and two of side `1/8`, for an exact sum of 4. Erdős and Graham (1975) study equal-square packing methods. The 17-square coordinates saved here are reconstructed from the grid and one-cell subdivision formula. They are not presented as the paper's original coordinates or a best-record construction.

The fixed public construction is from [Sprite143/erdos-106-counterexample](https://github.com/Sprite143/erdos-106-counterexample), pinned at commit `edbfb534e78d4f1f9b1a5a7298b9b022285b4962`. The repository gives a closed-form construction with exact rational coordinates and reports `2190452873/547596200`. This task checker independently recomputes all 17 squares. The lower value `2000062156200269/500000000000000` from the original search certificate is archived separately from the closed-form value.

On 2026-11-06, a search found a ProbXiv record for problem 106. It labels this construction AI-assisted and says Claude Opus 5 found it; the page states that no person has examined it. It also lists a machine-checked Lean formalization and warns that Lean checks the formalization, not whether it matches the webpage statement. The GitHub repository also says that the construction has not had human referee review. This archive therefore records an AI-assisted, unrefereed public result that is exactly rechecked by this task. It does not call it a human result or an optimum.

AlphaEvolve §6.35 reports a search result of 4 for `n=17`; that is not an upper-bound proof. The proved result by Baek, Koizumi, and Ueoro covers axis-parallel squares, not the unrestricted rotations in this task. The saved public construction gives a lower bound of `2190452873/547596200`. The area constraint and Cauchy–Schwarz give the upper bound `√17`. No matching upper bound was located, so this task makes no optimality claim.

## Limits and status

Generation budget: 300 seconds. Verification budget: 60 seconds. Memory: 4 GiB. Threads: one. Exact verification uses rational arithmetic for 17 squares. Status: **accepted by Sol on 2026-11-06**. See `IMPLEMENTATION.md` for commands and limitations.
