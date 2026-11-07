# T087：480 步函数的自相关比值

## 定义

固定 `N=480` 个等宽区间，步长 `d=13/4800`，总支撑长度 `W=13/10`。候选函数在第 `i` 个区间 `[id,(i+1)d)` 上取非负有理高度 `h_i`，其他位置取 0。高度总质量必须为正。

最大化

`J(h) = min_{0≤t≤1} ∫ f(x)f(x+t) dx / (∫ f(x)dx)^2`。

对 `t=(k+θ)d`，自相关在每个相邻网格点之间关于 `θ` 线性。因此精确最小值只需检查网格点 `k=0,…,369`，以及 `t=1`。由于 `1/d=369+3/13`，端点值是第 369 与第 370 个自相关值的精确线性插值。检查器使用有理数遍历全部这些位置，没有采样，也不使用浮点容差。

## 来源与结果

原问题是 Barnard 与 Steinerberger 2020 年论文中的连续常数，AlphaEvolve 将其列为问题 6.6。论文给出连续问题的下界 `>0.37`、上界 `≤0.411`，并描述经过小幅修改的反正弦函数。`human.py` 将该公式在本配置的 480 个格子中心取值，再四舍五入到 `1/100000`，得到一个独立的有理分段常数函数。它是方法重建，不是论文声称的 480 格见证。精确成绩为 `15833948850637600/43788391811747427`，约 `0.361601515732983`。

`data/source/certificate_n480.json` 是 Kevin Russell / ProjectForty2 的 CHRONOS 辅助证书。其上游仓库固定在 commit `b23f2d386eda9963e33c7531eeeb35c8f54cba37`；证书原始字节 SHA-256 为 `11cc0e743163a1e7f4f3b86bdf1f15c2cfd5fc099db3a323d2ea396b9d28d1fa`。精确重算得 `J=2378625/5958277≈0.3992135645925827`。该构造是 AI 辅助结果，不能归入人类基线。

2026-10-08 的 Chen 与 Gu 论文给出了更强的连续问题下界 `C≥0.410377977432121…`。该结果来自不同的原子加多项式函数及去原子论证，不是本配置的 480 格高度向量，不能直接记作本配置的分数。它没有证明连续问题或本有限维配置的最优值。我们截至 2026-11-06 未找到更强的同参数 480 格精确见证或最优性证明。

## 程序

- `init_program.py` 返回全 1 高度。
- `baseline.py` 从全 1 向量开始，以固定随机种子做 400 次分块变动。搜索使用 NumPy 浮点反馈，所有输出由精确检查器重新评分。
- `evolution.py` 使用相同起点和固定种子做 1,400 次分块变动。
- `human.py` 重建修改后的反正弦公式并量化为精确有理高度。
- `reference.py` 读取固定 AI 证书。
- `check.py` 用 Fraction 精确计算质量、全部相关节点和 `t=1` 插值。

运行器预算为生成 300 秒、验证 60 秒、内存 4 GiB、单线程和 16 MiB 输出。测试覆盖初始、传统搜索、演化、人类公式、AI 证书、非法高度、端点插值、伪造分数以及运行器错误和超时。

## 运行

```sh
.venv/bin/python -m pytest tasks/t087/test_task.py -q
```

本任务已通过 Sol 验收（2026-11-06）。

---

# T087: 480-step minimum autocorrelation ratio

## Definition

Fix `N=480` equal cells with width `d=13/4800` and support length `W=13/10`. The candidate is zero outside the support and has a nonnegative rational height `h_i` on cell `[i*d,(i+1)*d)`. Its total mass must be positive.

Maximize

`J(h) = min_{0≤t≤1} ∫ f(x)f(x+t) dx / (∫ f(x)dx)^2`.

For `t=(k+θ)d`, autocorrelation is linear in `θ` between adjacent grid nodes. The exact minimum therefore occurs at a node `k=0,...,369` or at `t=1`. Since `1/d=369+3/13`, the endpoint is the exact interpolation of the values at nodes 369 and 370. The checker uses rational arithmetic over this full interval. It does not sample shifts or use floating-point tolerances.

## Sources and results

The continuous problem is the minimum-autocorrelation constant studied by Barnard and Steinerberger (2020), and listed as Problem 6.6 by AlphaEvolve. Their paper gives the continuous bounds `>0.37` and `≤0.411` and describes a modified arcsine function. `human.py` samples that formula at the 480 cell centers and rounds heights to multiples of `1/100000`. This is a local reconstruction of the method, not a 480-cell witness claimed by the paper. Its exact score is `15833948850637600/43788391811747427`, about `0.361601515732983`.

`data/source/certificate_n480.json` is the certificate by Kevin Russell / ProjectForty2, assisted by CHRONOS. The upstream repository is pinned to commit `b23f2d386eda9963e33c7531eeeb35c8f54cba37`. The certificate's raw-byte SHA-256 is `11cc0e743163a1e7f4f3b86bdf1f15c2cfd5fc099db3a323d2ea396b9d28d1fa`. Exact recomputation gives `J=2378625/5958277≈0.3992135645925827`. This is an AI-assisted result, not a human baseline.

A paper by Chen and Gu, submitted 2026-10-08, gives a stronger bound `C≥0.410377977432121...` for the continuous problem. It uses a different atomic-polynomial profile and an atom-removal argument. It is not a 480-cell height vector for this configuration, so it is not recorded as this configuration's score. It does not prove the continuous or finite-dimensional optimum. As of 2026-11-06, we found no stronger exact witness on the same 480-cell grid and no proof of its optimum.

## Programs

The initial program returns all heights equal to 1. The baseline starts from that vector and makes 400 fixed-seed block mutations with NumPy feedback. Evolution makes 1,400 such mutations. These programs do not read the human or reference witness. The checker independently recomputes the exact score. The human program reconstructs the modified-arcsine formula. The reference program loads the pinned AI certificate.

The runner allows 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, one thread, and 16 MiB of candidate output. Tests cover all program entries, invalid heights, endpoint interpolation, forged scores, and runner failures and timeouts.

Run tests with:

```sh
.venv/bin/python -m pytest tasks/t087/test_task.py -q
```

This task is accepted by Sol on 2026-11-06.
