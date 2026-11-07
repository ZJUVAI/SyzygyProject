# T089: 一维符号不确定性

## 定义

固定一维 Fourier 变换

\[
\widehat f(\xi)=\int_{\mathbb R}f(x)e^{-2\pi i x\xi}\,dx,
\qquad
A(g)=\inf\{r>0:g(x)\ge0\text{ whenever }|x|\ge r\}.
\]

配置 T089-C01 使用有限有理系数多项式
\[
f(x)=p(\pi x^2)e^{-\pi x^2},\qquad p\in\mathbb Q[t].
\]
没有预设次数上限。Fourier 变换仍为 \(q(\pi\xi^2)e^{-\pi\xi^2}\)，评测器从 \(p\) 精确计算 \(q\)。必须满足 \(p(0)<0\)、\(q(0)<0\)，并且两者最终非负。

数学目标是最小化 \(A(f)A(\widehat f)\)。评测器用精确有理实根隔离找到每个多项式最后一个“负变正”根；偶数重接触根不计为半径。输出分数是原始乘积的严格有理区间，兼容排名使用上端。区间不把浮点根当证书。

## 构造与来源

可重建的人类基线来自经典 Hermite-Gaussian 特征函数。取
\[
p(t)=t^2-\frac32t-\frac1{1000}.
\]
这是 \(H_4(\sqrt{2t})/64\) 加一个有理常数修正。H4 的 Fourier 特征值为 +1，常数 Gaussian 也为 +1，因此 \(q=p\)；原点严格为负。2017 年 Gonçalves、Oliveira e Silva 与 Steinerberger 的论文系统研究了这类 Hermite 构造：[论文](https://doi.org/10.1016/j.jmaa.2017.02.030)。该弱基线按固定参数重新构造并由本地精确 checker 验证。

公开资料另报告了更强结果。Cohn、de Laat 与 Gonçalves 的未发表结果被 Georgiev 等人在 [2025 年 AlphaEvolve 论文](https://arxiv.org/abs/2511.02864v1)中报告为 0.3102。Station v2 后来报告上界 0.3089，使用 226 次多项式及严格有理全尾证书。Station 的[验证笔记](https://dualverse.ai/station/math/sign-uncertainty-principle/)和[论文](https://arxiv.org/abs/2608.23691)说明该结果由多模型 AI agent 协作产生；论文方法章节列出 GPT-5.5、Claude Opus 4.8 与 Gemini 3.1 Pro。精确多项式系数已保存于 `data/source/`，原始压缩数据和证明位于[固定仓库版本](https://github.com/dualverse-ai/station_data_v2/tree/a4ae9192fa75b7ffc6909ed018a712510062378b/artifacts/sign_uncertainty)。本任务没有重放高次数证书，因此将它列作公开报告，不冒称本配置已复现。来源固定版本与证据状态见 `sota.json` 和 `records.json`。

截至 2026-11-06，检查的来源没有给出本配置的最优性证明。Tomar 的[2026 年预印本](https://www.mefyi.com/papers/sign-uncertainty-constant/)把无约束问题的界缩至 0.30272004 至 0.30349081。其 0.30349081 构造使用多个 Gaussian 的混合，不属于这里固定的单个多项式乘单个 Gaussian 家族，单独记为不同范围。

## 运行

使用 `.venv/bin/python`。入口为 `run_code()`；初始构造为 `init_program.py`，传统随机搜索为 `baseline.py`，固定参考为 `reference.py`。评测入口为 `evaluate(program_path)`。默认生成限时 300 秒，验证限时 60 秒，内存 4 GiB，一个线程。

# T089: One-dimensional sign uncertainty

## Definition

Use the Fourier transform
\[
\widehat f(\xi)=\int_{\mathbb R}f(x)e^{-2\pi i x\xi}\,dx,
\qquad A(g)=\inf\{r>0:g(x)\ge0\text{ for every }|x|\ge r\}.
\]

T089-C01 searches over finite rational polynomials with no configured degree cap:
\[
f(x)=p(\pi x^2)e^{-\pi x^2}.
\]
Its Fourier transform is \(q(\pi\xi^2)e^{-\pi\xi^2}\). The checker computes \(q\) exactly from \(p\). Both \(p(0)\) and \(q(0)\) must be strictly negative. Both polynomials must become nonnegative on a full tail.

The raw objective is to minimize \(A(f)A(\widehat f)\). Exact rational real-root isolation finds the last negative-to-positive root of each polynomial. Even-multiplicity contacts do not count as a crossing. The checker returns a rational interval for the raw product and uses its upper endpoint for ranking.

## Construction and sources

The frozen human baseline rebuilds a classical Hermite-Gaussian eigenfunction:
\[
p(t)=t^2-\frac32t-\frac1{1000}.
\]
It is \(H_4(\sqrt{2t})/64\) plus a rational constant correction. The order-four Hermite Gaussian and the constant Gaussian both have Fourier eigenvalue +1, so \(q=p\), and both values at zero are strictly negative. Gonçalves, Oliveira e Silva, and Steinerberger studied these Hermite constructions in 2017 ([paper](https://doi.org/10.1016/j.jmaa.2017.02.030)). The fixed baseline is rebuilt and checked with exact arithmetic.

Public sources report stronger results. Georgiev et al. reported an unpublished human result of 0.3102 in their [2025 AlphaEvolve paper](https://arxiv.org/abs/2511.02864v1). Station v2 later reported an upper bound of 0.3089 using a degree-226 polynomial and a strict rational whole-tail certificate. Its [verification notes](https://dualverse.ai/station/math/sign-uncertainty-principle/) and [paper](https://arxiv.org/abs/2608.23691) attribute this result to collaboration among AI agents; the paper describes a Station with GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro. The exact polynomial coefficients are saved under `data/source/`, and the original compressed data and proof are available in its [pinned repository version](https://github.com/dualverse-ai/station_data_v2/tree/a4ae9192fa75b7ffc6909ed018a712510062378b/artifacts/sign_uncertainty). This task has not replayed that high-degree certificate, so it remains a reported public result rather than a reproduced score. See `sota.json` and `records.json` for the pinned source and evidence status.

The sources checked through 2026-11-06 do not prove optimality for this configuration. Tomar's [2026 preprint](https://www.mefyi.com/papers/sign-uncertainty-constant/) narrows the unrestricted problem to 0.30272004–0.30349081. Its 0.30349081 construction uses a mixture of Gaussians. It is outside this single-Gaussian polynomial family and is recorded separately.

## Run

Use `.venv/bin/python`. Each program exposes `run_code()`. The simple start is `init_program.py`; the traditional search is `baseline.py`; the frozen reference is `reference.py`. The evaluator entry is `evaluate(program_path)`. Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one thread.
