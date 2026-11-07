# T090：长度 64 的周期二元序列能量

## 定义与配置

序列为 `s_0,…,s_63 ∈ {−1,+1}`。对每个非零循环位移 `k=1,…,63`，定义

`C_k = Σ_{i=0}^{63} s_i s_{(i+k) mod 64}`。

目标是最小化周期旁瓣能量 `E = Σ_{k=1}^{63} C_k²`。所有相关和与能量均为整数。此处使用周期边界，不采用非周期相关公式。

配置 T090-C01 固定 `N=64`。初始程序返回全 `+1` 序列，能量为 258048。

## 人类构造与公开结果

Tyler 和 Loftsson 的 NASA 报告表 2 给出长度 64 的十六进制序列 `B24FEAE7E4529CF0`。按最高有效位优先读取，`1` 映射为 `+1`，`0` 映射为 `−1`。本任务逐项复算得到周期能量 240，峰值旁瓣 4。该结果是冻结的人类方法对照。报告表中 `M=(240)`，括号表示作者认为可能存在更低值。表下注释 ZZ 引用 J. Watkins 1985 年 6 月的个人通信；本任务只记录该表中的序列，不对其最初发现者作超出原表的归属。

Mertens 和 Bessenrodt 的 §4.2 表 4 对 `N=64` 报告 `ΔE=14`，即本任务能量 `E=16ΔE=224`。该行来自数值搜索，ground state 栏标为 `?`，所以没有最优性证明，也没有恢复其序列见证。该值单独列作公开报告结果；冻结参考仍用可复现的能量 240。

来源：

- [Tyler and Loftsson, *Periodic Binary Sequences With Very Good Autocorrelation Properties*](https://ipnpr.jpl.nasa.gov/progress_report/42-82/82O.PDF)，TDA Progress Report 42-82，1985 年 4–6 月，第 143–158 页，表 2；[NASA NTRS 记录](https://ntrs.nasa.gov/citations/19860000930)。报告副本 SHA-256：`edc332b8a9410cb0d8f14d6db65225469f592c5096c88fa3e8051315282d63cf`。
- [Mertens and Bessenrodt, *On the ground states of the Bernasconi model*](https://arxiv.org/abs/cond-mat/9707104)，§4.2，表 4。期刊版本：1998，DOI [10.1088/0305-4470/31/16/004](https://doi.org/10.1088/0305-4470/31/16/004)。

截至 2026-11-06 检查的来源，长度 64 的 224 仍只是数值结果，没有找到同一周期目标的闭合证明。Mertens 和 Bessenrodt 指出此类长度 `N=4t` 的穷举只做到 `N≤40`。此开放状态结论限于所查来源。后来的长度 64 非周期低能研究不改变本任务的周期定义。

## 搜索与精确评分

检查器校验恰有 64 个整数 `−1` 或 `+1`，然后直接计算全部 63 个非零循环相关和、能量和峰值旁瓣。候选附带的成绩字段不会影响结果。

传统搜索使用固定种子的多起点单比特模拟退火。每次翻转只用整数差量更新相关和；输出仍由独立检查器从头重算。默认四次重启，每次 5000 步。搜索只使用自身随机初值，不读取 NASA 或其他对照序列。初始构造、搜索、人类重建和固定参考分别由独立入口提供。

默认生成限时 300 秒，验证限时 60 秒，内存 4 GiB，一个线程。当前配置已通过 Sol 验收（2026-11-06）。

## English

### Definition

The sequence is `s_0,…,s_63 ∈ {−1,+1}`. For each nonzero cyclic shift `k=1,…,63`, define `C_k = Σ_i s_i s_(i+k mod 64)`. The objective is to minimize the periodic sidelobe energy `E = Σ_{k=1}^{63} C_k²`. All correlations and energies are exact integers. The boundary is periodic; the aperiodic formula is not used.

The simple initial program returns the all-`+1` sequence, with energy 258048.

### Human and public results

Table 2 of the NASA report by Tyler and Loftsson gives the length-64 hex sequence `B24FEAE7E4529CF0`. Read most-significant bit first and map `1` to `+1` and `0` to `−1`. Exact recomputation gives periodic energy 240 and peak sidelobe 4. This is the frozen reproduced human baseline. The table prints `M=(240)`; parentheses indicate that the authors thought a lower value might exist. Footnote ZZ cites J. Watkins, personal communication, June 1985. This task records the sequence as printed and does not make a stronger claim about its original discoverer.

Section 4.2, Table 4 of Mertens and Bessenrodt reports `ΔE=14` at `N=64`, which gives this task's energy `E=16ΔE=224`. It is a numerical-search result. The ground-state column is `?`; no optimality proof or sequence witness was recovered. We record 224 as a reported public value and keep 240 as the reproducible reference.

The checker validates all 64 entries and recomputes every off-peak periodic correlation, energy, and peak sidelobe with integer arithmetic. Search uses seeded multistart single-bit simulated annealing and reads no comparison sequence. The task is accepted by Sol on 2026-11-06.
