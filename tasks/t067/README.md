# T067: Maximum size of a binary code A(n,d)

## 中文

### 目标

构造长度为 17 的二元码。任意两个不同码字的汉明距离至少为 6。目标是最大化码字数量。提交 `codewords` 列表。每个码字可用 0 到 131071 的整数表示，也可用 17 个整数位表示。

### 基线与来源

Brouwer 的公开表列出 `258 ≤ A(17,6) ≤ 340`，并将下界 258 归于 Moshe Milshtein。该下界来自长度 16、最小距离 5、含 258 个码字的构造，再为每个码字添加整体奇偶校验位。表格和论文摘要可确认该结果，但公开页面未给出码字列表；本包没有声称复现 258 个码字。

本包复现一个较弱的经典构造：二元原始 BCH `[15,7,5]` 码加整体奇偶校验位，再加一个零坐标，得到长度 17、距离至少 6、含 128 个码字的码。检查器对全部 8128 对码字精确计算汉明距离。该构造不代表最优值。

## English

### Goal

Construct a binary code of length 17. Every pair of distinct codewords must have Hamming distance at least 6. Maximize the code size. Return a `codewords` list. Each word can be an integer from 0 to 131071 or a list of 17 integer bits.

### Baselines and sources

Brouwer's public table gives `258 ≤ A(17,6) ≤ 340` and attributes the lower bound 258 to Moshe Milshtein. The bound comes from a length-16 code with minimum distance 5 and 258 words, extended by an overall parity bit. The table and paper abstract support this result, but the public page does not provide the word list. This package does not claim to reproduce the 258-word witness.

This package reproduces a weaker classical construction: the binary primitive BCH `[15,7,5]` code with an overall parity bit and one zero coordinate. It has length 17, minimum distance at least 6, and 128 words. The checker computes all 8,128 pairwise distances exactly. This construction is not claimed to be optimal.

### Sources

- [Brouwer, Small binary codes table](https://aeb.win.tue.nl/codes/binary-1.html), checked 2026-11-03.
- [Milshtein, A new two-error-correcting binary code of length 16](https://doi.org/10.1007/s12095-019-00365-7), published online 2019; issue 2020. The abstract reports a 258-word length-16 code with distance 5.
- [BCH code definition and parameters](https://www.encyclopediaofmath.org/wiki/BCH_code), checked 2026-11-03.
