# T051: unrestricted discrepancy-3 sequences

## Definition

For a finite sign sequence `x_1,...,x_N` with each `x_i` in `{-1,+1}`, define its homogeneous-progression discrepancy as the largest absolute prefix sum

`|x_d + x_(2d) + ... + x_(kd)|`,

over positive integers `d,k` with `kd <= N`. T051-C01 fixes the cap at 3 and maximizes `N`. Signs are unrestricted; no multiplicative rule is imposed. The checker uses exact integer arithmetic and checks every such prefix.

The initial program returns `[1]`, a valid one-term sequence. `baseline.py` extends a sequence one term at a time. When it chooses `x_n`, it checks each divisor `d` of `n`; these are exactly the progressions whose new prefix ends at `n`. It uses a fixed seed, 24 trials, and a 5000-term limit by default. It reads no comparison witness. Set `MATHBENCH_SEARCH_SECONDS` for an explicit time cutoff.

## Published status and comparison

Konev and Lisitsa's SAT paper reports an unrestricted C=3 sequence of length 130000. The first 127600 terms are completely multiplicative. Their paper and data page do not prove that 130000 is longest. We recovered a complete sign sequence from a public notebook in a Wolfram Community discussion about the problem, then checked every progression prefix locally. The discussion refers to the Konev-Lisitsa report and data page. The saved text is a reconstruction from that public notebook; we do not claim byte identity with the original compressed author download. The source text contains 130000 signs and has SHA-256 `024af56550adebd499df5c4e857453f518655e7e175af6e8d8a017e047f754c2`.

The exact maximum 1160 for C=2 is a different cap. The exact maximum 127645 for completely multiplicative C=3 sequences is a restricted problem. Neither resolves the unrestricted C=3 maximum. Tao's theorem rules out an infinite sequence with bounded discrepancy, but it gives no exact finite maximum. The 2026 Princeton thesis we checked treats the solved C=2 range and does not close the unrestricted C=3 case. We therefore record 130000 as a verified lower bound and leave the finite maximum open.

Primary sources:

- Konev and Lisitsa, [Computer-Aided Proof of Erdős Discrepancy Properties, arXiv:1405.3097v2](https://arxiv.org/html/1405.3097v2), especially §4.
- [Konev and Lisitsa author data page](https://cgi.csc.liv.ac.uk/~konev/edp/), checked 2026-11-06.
- The recovered [public notebook](https://community.wolfram.com/uploads/short-url/tecwlpwuwx7kcTAYpoVaduRt9FD.nb) is linked from this [Wolfram Community discussion](https://community.wolfram.com/t/discrepancy-conjecture/6798). Notebook SHA-256: `cc6066cefd3c28435aee484b8ad4c952f6d17919732acc5e21a412ed45cadbca`.
- Tao, [The Erdős discrepancy problem, arXiv:1509.05363](https://arxiv.org/abs/1509.05363), for the infinite-sequence theorem.

## Programs and budgets

- `check.py` independently recalculates validity and length. Optional score fields do not affect its result.
- `init_program.py` is a short valid seed. `baseline.py` and `evolution.py` do not read comparison data.
- `human.py` replays the recovered human construction. `reference.py` replays the frozen public comparison.
- `evaluator.py` uses the shared evaluator. Generation budget is 300 seconds; verification budget is 60 seconds; default memory is 4 GiB and one thread.

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t051/test_task.py -q
.venv/bin/python -m json.tool tasks/t051/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t051/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t051/records.json > /dev/null
```

## 定义

给定有限符号序列 `x_1,...,x_N`，每项取 `-1` 或 `+1`。对正整数 `d,k` 且 `kd<=N`，检查齐次算术子列前缀和 `x_d+x_(2d)+...+x_(kd)`。T051-C01 固定上界为 3，目标是最大化序列长度 `N`。序列不受乘法性限制。评测器用整数精确计算检查所有前缀。

初始程序返回有效的一项序列 `[1]`。传统搜索程序每次添加一项，并检查所有满足 `d|n` 的前缀。默认固定种子、24 次尝试和 5000 项上限。搜索不读取人类见证或参考见证。可用 `MATHBENCH_SEARCH_SECONDS` 设置显式时间上限。

## 已知结果和对照

Konev 与 Lisitsa 的 SAT 论文报告了一条长度 130000、无乘法性限制的 C=3 序列。前 127600 项完全乘法。论文和作者数据页没有证明 130000 是最大值。我们从作者数据页链接的公开 notebook 中恢复了完整序列，并用本地程序精确检查全部前缀。保存的文本是从该 notebook 恢复的表示；没有声称它与原始压缩文件逐字节相同。文本含 130000 项，SHA-256 为 `024af56550adebd499df5c4e857453f518655e7e175af6e8d8a017e047f754c2`。

C=2 的精确最大值 1160 是另一个上界配置。C=3 完全乘法序列的精确最大值 127645 属于受限问题。两者都没有解决无乘法性限制的 C=3。Tao 的定理排除无限且差异有界的序列，但没有给出有限最大长度。我们检查的 2026 年 Princeton 论文讨论已解决的 C=2 范围，未解决无乘法性限制的 C=3。因此将 130000 记为已验证下界，有限最大值仍开放。

主来源与复核日期见上方英文来源列表。任务状态为已通过 Sol 验收（2026-11-06）。
