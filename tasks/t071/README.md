# T071: Maximum binary single-deletion-correcting code at length 16

## Definition

Choose a set `C` of distinct 16-bit binary words. If any one bit is deleted from a codeword, the remaining 15-bit string must identify that codeword uniquely. In exact terms, for any two different codewords, their sets of length-15 strings obtained by one deletion must be disjoint. Maximize `|C|`.

The number of distinct outputs from one codeword can be less than 16 when it has repeated bits. Therefore, simply dividing all 16-bit words by a fixed ball size is not a valid exact bound. The checker verifies the full deletion-output sets directly, using integer bit strings.

## Same-parameter human construction

The classical Varshamov–Tenengolts class `VT_0(16)` is defined by

```text
sum(i * x_i for i = 1..16) == 0 (mod 17)
```

where `x_i` is the bit at one-based position `i`. The checksum class is traced to Varshamov and Tenengolts' 1965 work on single asymmetric errors. Levenshtein established its single-deletion correction property. The exact formula is also stated in §2.2 of the 2026 paper. It has 3,856 words at length 16. The task generates this code from the formula and verifies every deletion output.

The frozen public list is stored separately from the formula-based human program. Both independently check to 3,856 words.

## Open status and AI-assisted record

Weindel and Heckel's 2026 arXiv v2 states that VT codes are conjectured to be maximum for every finite length, while optimality has been proved only through length 11. Its §5.1, Table 1 gives the n=16 VT construction as 3,856 and an LP upper bound of 4,202. Thus the selected length-16 maximum remains open in the sources checked on 2026-11-06.

The same paper reports an LLM-guided evolutionary rediscovery of a priority function proved equivalent to `VT_0`, including size 3,856 at n=16. We record this AI-assisted result separately. It equals the classical code size and does not prove the n=16 maximum.

## Search entries

The initial program returns the one-word code `{0}`. The traditional baseline scans random permutations of all 65,536 words and greedily adds a word when its deletion outputs do not conflict with earlier choices. It does not read human or reference witnesses. The fixed default uses two trials; the seed comes from `MATHBENCH_SEED`. `MATHBENCH_SEARCH_SECONDS` can set an exploratory wall-clock cutoff.

## Sources

- R. R. Varshamov and G. M. Tenengolts, [Codes which correct single asymmetric errors](https://m.mathnet.ru/php/archive.phtml?jrnid=at&option_lang=eng&paperid=11293&wshow=paper), *Avtomatika i Telemekhanika* 26 (1965), 288–292.
- V. I. Levenshtein, [Binary codes capable of correcting deletions, insertions, and reversals](https://nymity.ch/sybilhunting/pdf/Levenshtein1966a.pdf), Russian original 1965; English translation in *Soviet Physics Doklady* 10 (1966), 707–710.
- Franziska Weindel and Reinhard Heckel, [LLM-Guided Search for Deletion-Correcting Codes](https://arxiv.org/abs/2504.00613), arXiv:2504.00613v2, 2026-06-05; HTML revision checked 2026-11-06. See §1, §2.2 and §5.1 Table 1.

## Reproduction

Set `MATHBENCH_CONFIG_ID=T071-C01` and run any of the five `run_code()` entries. Run tests with:

```sh
.venv/bin/python -m pytest tasks/t071/test_task.py -q
```

---

# T071：长度 16 的最大二元单删除纠错码

## 定义

选择一组互异的 16 位二元串 `C`。删除任一码字中的任意一位后，剩余的 15 位串必须唯一确定原码字。精确定义是：任意两个不同码字在单次删除后得到的 15 位串集合互不相交。最大化 `|C|`。

若一个码字有连续相同位，删除不同位置可能得到相同输出，因此其不同删除输出数可能小于 16。不能用固定球大小直接除以总字数作精确上界。检查器直接构造并检验各码字的全部不同删除输出。

## 同参数人类构造

经典 Varshamov–Tenengolts 类 `VT_0(16)` 定义为

```text
sum(i * x_i for i = 1..16) == 0 (mod 17)
```

其中 `x_i` 是从 1 开始编号的第 `i` 位。该校验和类源自 Varshamov 与 Tenengolts 1965 年关于单次非对称错误的工作；Levenshtein 证明了它可纠正一次删除。2026 年论文第 2.2 节也给出同一公式。长度 16 时有 3,856 个码字。任务按公式生成构造，并精确检查每种删除输出。

公开码字列表和公式程序分别保存。两者都独立验得 3,856 个码字。

## 开放状态与 AI 辅助记录

Weindel 和 Heckel 的 2026 年 arXiv v2 说明，VT 码被猜想在所有有限长度都最大，但目前只证明到长度 11。该文第 5.1 节表 1 给出 n=16 时 VT 构造大小 3,856，线性规划上界为 4,202。因此，截至 2026-11-06 检查的来源，所选长度的最大值仍未解决。

同文报告 LLM 引导的演化搜索重新发现了一个已证明等价于 `VT_0` 的优先函数，n=16 时也得到 3,856。此 AI 辅助结果单独记录。它与经典码大小相同，也没有证明 n=16 最优。

## 搜索入口

初始程序返回单字码 `{0}`。传统基线随机排列全部 65,536 个字，并在删除输出与已选字不冲突时贪心加入。它不读取人类或参考见证。默认固定运行两轮，种子来自 `MATHBENCH_SEED`。可用 `MATHBENCH_SEARCH_SECONDS` 设置探索时限。

## 来源

- R. R. Varshamov 与 G. M. Tenengolts，[Codes which correct single asymmetric errors](https://m.mathnet.ru/php/archive.phtml?jrnid=at&option_lang=eng&paperid=11293&wshow=paper)，*Avtomatika i Telemekhanika* 26 (1965), 288–292。
- V. I. Levenshtein，[Binary codes capable of correcting deletions, insertions, and reversals](https://nymity.ch/sybilhunting/pdf/Levenshtein1966a.pdf)，俄文原文 1965；英文译文刊于 *Soviet Physics Doklady* 10 (1966), 707–710。
- Franziska Weindel 和 Reinhard Heckel，[LLM-Guided Search for Deletion-Correcting Codes](https://arxiv.org/abs/2504.00613)，arXiv:2504.00613v2，2026-06-05；HTML 页面于 2026-11-06 检查。参见第 1、2.2、5.1 节表 1。

## 复现

设置 `MATHBENCH_CONFIG_ID=T071-C01` 并运行五个 `run_code()` 入口之一。测试命令：

```sh
.venv/bin/python -m pytest tasks/t071/test_task.py -q
```
