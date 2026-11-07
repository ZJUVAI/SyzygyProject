# T068: Binary length-10 radius-one covering code

## Definition

Choose a set `C` of 10-bit binary words. Every 10-bit word must differ in at most one position from at least one member of `C`. Minimize `|C|`. This is the covering-code number `K(10,1)`. The fixed configuration is `T068-C01`.

The input is a list of distinct integers in `0..1023`, each written as its 10-bit binary expansion. The checker forms every radius-one Hamming ball as an exact 1024-bit integer mask and verifies that their union is the full universe. It does not rely on a reported score.

## Reproduced public code

OEIS A000983's source file credits Dmitry Kamenetsky and lists `a(10)<=120`, followed by 120 ten-bit words. The next section is `a(11)<=192`; the task parser and frozen witness stop before that entry. The exact list is saved under `data/reference/` and separately checked against all 1024 words.

The 120-word witness is a feasible upper bound on `K(10,1)`. It does not establish the minimum. The current OEIS page gives `107-120` for `a(10)`. The Kéri binary table independently lists `107-120`. The lower bound 107 is also cited to Bertolo, Östergård, and Weakley (2004). The exact value remains open in the sources checked on 2026-11-06.

Östergård's 1991 paper reports a 120-word binary code derived from a 60-word mixed `F_4 x F_2^7` cover. The OEIS list is frozen as a separate public witness. We do not claim that it is the same code or construction as the 1991 one.

## Human-method baseline

Use the binary `[7,4,3]` Hamming code, then append each of the eight possible 3-bit suffixes. The resulting product code has `16*8=128` words. Its first seven coordinates cover the 7-cube perfectly: the parity-check matrix has the seven distinct nonzero 3-bit columns, so each syndrome is either zero or identifies the unique bit to flip. Matching the suffix leaves total Hamming distance at most one. This is a same-parameter human construction, reconstructed from Hamming's classical code.

## Sources

- [OEIS A000983](https://oeis.org/A000983), current definition and range `a(10)=107..120`.
- Dmitry Kamenetsky, [Best known solutions for n<=11](https://oeis.org/A000983/a000983.txt), 2020-07-27; `a(10)<=120` and its 120-word list.
- Gerzson Kéri, [Tables for bounds on covering codes](https://old.sztaki.hu/~keri/codes/index.htm), [binary table PDF](https://old.sztaki.hu/~keri/codes/2_tables.pdf), length 10, radius 1, bounds 107-120.
- R. Bertolo, P. R. J. Östergård, and W. D. Weakley, [An updated table of binary/ternary mixed covering codes](https://doi.org/10.1002/jcd.20008), *Journal of Combinatorial Designs* 12 (2004), 157–176; OEIS cites it for the lower bound 107.
- P. R. J. Östergård, [A new binary code of length 10 and covering radius 1](https://doi.org/10.1109/18.61135), *IEEE Transactions on Information Theory* 37 (1991), 179–180.
- R. W. Hamming, [Error Detecting and Error Correcting Codes](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x), *Bell System Technical Journal* 29 (1950), 147–160.

## Reproduction

Run the five entries with `MATHBENCH_CONFIG_ID=T068-C01`. Run tests with:

```sh
.venv/bin/python -m pytest tasks/t068/test_task.py -q
```

The initial program returns all 1024 words. The traditional baseline uses a greedy set-cover method and redundant-word deletion. Neither reads comparison files.

---

# T068：二元长度 10、覆盖半径 1 的覆盖码

## 定义

选择一组 10 位二元串 `C`。每个 10 位二元串都必须与 `C` 中至少一个码字相差至多一位。最小化 `|C|`。该数记为覆盖码数 `K(10,1)`。固定配置为 `T068-C01`。

输入是 `0..1023` 中互异整数，每个整数表示对应的 10 位二进制串。检查器用精确的 1024 位整数掩码构造各半径一 Hamming 球，并验证并集等于全空间。检查器不采信程序声明的分数。

## 已复现公开码

OEIS A000983 源文件署名 Dmitry Kamenetsky，并列出 `a(10)<=120` 及 120 个 10 位码字。下一节是 `a(11)<=192`；任务解析器和冻结见证在 n=10 结束。文件中的 120 字码已保存，并对 1024 个输入逐个复核。

这给 `K(10,1)` 提供可行上界，不证明最小值。当前 OEIS 页面给出 `107-120`；Kéri 的二元码表也列出 `107-120`。107 下界还引用 Bertolo、Östergård 和 Weakley 2004 年论文。截至 2026-11-06 检查的来源没有给出精确值。

Östergård 1991 年论文报告了一个由 60 字混合 `F_4 x F_2^7` 覆盖码变换得到的 120 字二元码。本任务把 OEIS 列表作为单独的公开见证，不声称它与 1991 年的码相同。

## 人类方法基线

取二元 `[7,4,3]` Hamming 码，并附加所有 8 种 3 位后缀，得到 `16*8=128` 个码字。前七位的 Hamming 码完美覆盖 7 维二元空间：校验矩阵的列是七个互异非零 3 位向量，因此每个 syndrome 为零，或唯一标出应翻转的位。后缀保持不变，所以总距离不超过一。这是由经典 Hamming 码重建的同参数人类构造。

## 来源

- [OEIS A000983](https://oeis.org/A000983)，当前定义与 `a(10)=107..120` 范围。
- Dmitry Kamenetsky，[Best known solutions for n<=11](https://oeis.org/A000983/a000983.txt)，2020-07-27；`a(10)<=120` 及 120 字列表。
- Gerzson Kéri，[覆盖码界表](https://old.sztaki.hu/~keri/codes/index.htm)，[二元表 PDF](https://old.sztaki.hu/~keri/codes/2_tables.pdf)，长度 10、半径 1 的界为 107-120。
- R. Bertolo、P. R. J. Östergård、W. D. Weakley，[An updated table of binary/ternary mixed covering codes](https://doi.org/10.1002/jcd.20008)，*Journal of Combinatorial Designs* 12 (2004), 157–176；OEIS 将其列作下界 107 的来源。
- P. R. J. Östergård，[A new binary code of length 10 and covering radius 1](https://doi.org/10.1109/18.61135)，*IEEE Transactions on Information Theory* 37 (1991), 179–180。
- R. W. Hamming，[Error Detecting and Error Correcting Codes](https://doi.org/10.1002/j.1538-7305.1950.tb00463.x)，*Bell System Technical Journal* 29 (1950), 147–160。

## 复现

五个程序均使用 `MATHBENCH_CONFIG_ID=T068-C01`。测试命令：

```sh
.venv/bin/python -m pytest tasks/t068/test_task.py -q
```

初始程序返回全体 1024 个字。传统搜索使用贪心集合覆盖和冗余删除。两者均不读取对照文件。
