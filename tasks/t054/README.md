# T054: length-100/101/102 binary sequences with low peak sidelobes

## Definition

The input is a configured-length sequence `s_0,...,s_(n-1)`, with every entry in `{-1,+1}`. For each nonzero shift `k=1,...,99`, its aperiodic autocorrelation is

`C[k] = sum(s[i] * s[i+k], i=0,...,99-k)`.

The task minimizes the peak sidelobe level `PSL = max(abs(C[k]), k=1,...,99)`. The main peak at shift zero is excluded. The checker calculates all 99 values with exact integer arithmetic.

## Why this differs from T013

T013 minimizes the energy `E=sum(C[k]^2)`. PSL and energy are not monotone transforms of each other, even at the fixed length 100, 101, or 102. Exact recalculation gives the T013 public energy witness `E=578, PSL=8`; the Nunn-Coxson PSL witness has `E=874, PSL=5`. Energy prefers the first sequence while PSL prefers the second. Thus neither task's objective order determines the other.

## Public construction and current status

Nunn and Coxson's 2008 Table 2 prints a length-100/101/102 code in hexadecimal and reports PSL 5. We expand `DF490FFB1F8390A54E3CD9AAE` to 100 bits, most significant bit first, and map 1 to +1 and 0 to -1. A global sign change leaves every autocorrelation unchanged. The checker recomputes all sidelobes and obtains PSL 5.

The latest checked survey is version 2 of Brest et al., posted 2026-07-28. Section 1 says exact minima are known for lengths up to 61 and at length 64. It directs readers to Nunn and Coxson for reported values at lengths 71 to 105. It describes results outside the exact range as best-known values. We therefore use N=100 as an open configuration and record PSL 5 as a feasible public construction, not a proof of optimality. The source does not provide a certified nontrivial lower bound for this exact optimum.

Sources checked on 2026-11-06:

- Nunn and Coxson, [Best-Known Autocorrelation Peak Sidelobe Levels for Binary Codes of Length 71 to 105](https://www.norbertwiener.umd.edu/crowds/documents/best_known_binary.pdf), IEEE Transactions on Aerospace and Electronic Systems 44(1), 2008, Table 2, N=100.
- Brest et al., [Binary Sequences with Low Aperiodic Autocorrelations: Small Peak Sidelobe Levels, version 2](https://www.preprints.org/manuscript/202605.0907), posted 2026-07-28, §1.
- The definition and distinction from merit factor are also stated in the 2026 survey, §1. The merit factor is `L^2/(2E)`, so it is a monotone transform of T013 energy at fixed length. PSL is not a monotone transform of that sum of squares.

## Programs and limits

- `init_program.py` returns configured-length positive signs. This is valid and has PSL 99.
- `baseline.py` uses fixed-seed single-bit-flip simulated annealing. It updates exact integer correlations and does not read comparison data. The default is 12 restarts with 3000 flips each. Set `MATHBENCH_SEARCH_SECONDS` for a time cutoff.
- `human.py` rebuilds the published hexadecimal construction. `reference.py` replays the frozen same-parameter public record from task data.
- `evaluator.py` uses the shared runner. Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread.

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t054/test_task.py -q
.venv/bin/python -m json.tool tasks/t054/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t054/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t054/records.json > /dev/null
```

## 定义

输入是长度为 100 的符号序列 `s_0,...,s_99`，每项为 `-1` 或 `+1`。对每个非零位移 `k=1,...,99`，计算非周期自相关

`C[k] = sum(s[i] * s[i+k], i=0,...,99-k)`。

目标是最小化峰值旁瓣 `PSL=max(abs(C[k]), k=1,...,99)`。零位移主峰不计入目标。评测器用整数精确计算全部 99 项。

## 与 T013 的区别

T013 最小化能量 `E=sum(C[k]^2)`。固定长度 100 时，两项目标也不是单调变换关系。对 T013 的公开能量见证精确重算得到 `E=578, PSL=8`；对 Nunn-Coxson 的 PSL 见证精确重算得到 `E=874, PSL=5`。能量目标偏好前者，PSL 目标偏好后者。因此不能用一个目标的排序代替另一个目标。

## 公开构造与当前状态

Nunn 与 Coxson 2008 年论文表 2 给出长度 100 的十六进制序列，报告 PSL 为 5。我们按最高位优先将 `DF490FFB1F8390A54E3CD9AAE` 展开为 100 个二进制位，将 1 映射为 +1、0 映射为 -1。整体符号取反不会改变自相关值。评测器重新计算全部旁瓣，得到 PSL=5。

截至 2026-11-06 检查到的最新综述是 Brest 等人 v2，2026-07-28 发布。第 1 节说长度不超过 61 和长度 64 的精确最小值已知，并将 71 至 105 的报告值指向 Nunn-Coxson。综述将精确范围以外的结果称为已知最好值。因此选择 N=100 作为未解决配置，把 PSL=5 记为公开可行构造，不称全局最优。已查来源没有给出该具体最优值的非平凡认证下界。

任务状态：已通过 Sol 验收（2026-11-06）。

## Added open configurations

T054-C02 fixes length 101 and T054-C03 fixes length 102. Nunn and Coxson (2008), Table 2, prints the complete hexadecimal witnesses and reports PSL 5 for both. The frozen source rows are recorded in `data/source/`; exact integer recomputation gives PSL 5. Brest et al. (2026 v2, §1) identifies exact minima only through length 61 and length 64 and points to Nunn–Coxson for 71–105. We treat both as open candidates, not proved optima. Both additions are accepted by Sol on 2026-11-07.

### Configuration status

| Configuration | Length | Public human construction | Recomputed PSL | Status |
|---|---:|---|---:|---|
| T054-C01 | 100 | Nunn–Coxson (2008), Table 2 | 5 | Accepted by Sol (2026-11-06) |
| T054-C02 | 101 | Nunn–Coxson (2008), Table 2 | 5 | Accepted by Sol |
| T054-C03 | 102 | Nunn–Coxson (2008), Table 2 | 5 | Accepted by Sol |

For C02 and C03, full hexadecimal witness strings and source row excerpts are saved in `data/source/`. Exact recomputation gives PSL 5 for each. Brest et al. (2026), v2, §1 describes values above length 61 (except 64) as best-known and points to Nunn–Coxson for 71–105. The checked sources do not prove the minima for lengths 101 or 102.
