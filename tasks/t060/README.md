# T060: M61 的整数复杂度

## 中文

配置 `T060-C01` 固定目标为 `M61 = 2^61 - 1 = 2305843009213693951`。目标是在表达式树中用最少个 `1` 精确表示该整数。允许的叶子只有 `1`，内部节点只有 `+` 与 `*`。重复写出的子表达式各自计数；不允许共享子树、减法或幂。

评测器用整数栈解析表达式，并从完整字符串重新计算值和 `1` 的数量。它不读取候选声称的分数。Selfridge 定理给出精确下界 116：最多用 115 个 `1` 可表示的最大整数是 `1801135623563989452`，小于 M61。此配置尚无已知最优性证明。

解析器的 100,000 字符上限是输入资源限制，不是数学目标或“任意冗余文本均可接受”的保证。含 `k` 个叶子的二叉表达式可规范化为完全括号化形式，长度至多 `4k−3`；153 个叶子对应 609 字符。本任务保存的三进制表达式为 505 字符。去掉空格和多余括号不会改变表达式树或叶子数。

冻结人类基线为 153。`human.py` 按三进制位展开，用 Horner 法从高位向低位重建表达式。M61 有 39 个三进制位；每步乘以 `1+1+1`，再按当前位加 0、1 或 2 个 `1`。这是对传统整数复杂度表达方法的重建，不是公开最优纪录。Altman 的整数复杂度综述回顾了该问题、Selfridge 界及 Horner 表示。[论文](https://msp.org/cnt/2019/8-3/moscow-v8-n3-p01-s.pdf)

固定参考构造使用 127 个 `1`。该表达式来自 EventCompute 的公开页面及 board 的 PR #4，SHA-256 为 `946a56e064e60422f49c98aeeb0ceae0a99c22d5070318a7b84fcbca28699449`。页面明确说明其研究过程使用生成式 AI 助手，因此记为 AI 辅助公开结果，不归作纯人工发现。[结果与来源说明](https://eventcompute.com/en/challenges/integer-complexity-m61/) · [board PR #4](https://github.com/math-market/integer-complexity-m61/pull/4)

Board 自己的 150 表达式只是挑战基线，不是纪录；来源未说明该构造是否使用 AI。公开页面截至 2026-10-13 报告 127 构造、下界 116，未给出精确复杂度。我们在 2026-11-06 复查了该页面、board 主仓库和 PR 状态；没有发现 M61 精确最优性证明或更短的同参见证。该检查限于所引来源，不表示穷尽所有公开资料。

简单起点用二进制 Horner 法独立生成。传统搜索枚举固定基数 Horner 表达式；进化入口用固定种子搜索混合基数展开。它们都只从目标整数构造，不读取人类或参考文件。正式结果以 `check.py` 的精确重算为准。

## English

Configuration `T060-C01` fixes `M61 = 2^61 - 1 = 2305843009213693951`. The objective is to minimize the number of `1` leaves in an expression tree that equals this integer. The only leaves are `1`; the only internal nodes are `+` and `*`. Repeated text is counted as separate tree nodes. Shared subtrees, subtraction, and exponentiation are not allowed.

The checker parses the full expression with integer stacks, then recomputes its value and leaf count. It ignores every score supplied by a candidate. Selfridge's theorem gives an exact lower bound of 116: the largest integer that uses at most 115 ones is `1801135623563989452`, below M61. No proof of the exact complexity is known in the sources checked for this task.

The 100,000-character parser limit is an input resource bound, not part of the mathematical objective and not a promise to accept arbitrary redundant text. A binary expression tree with `k` leaves has a fully parenthesized form of at most `4k−3` characters; for 153 leaves this is 609 characters. The saved base-3 expression is 505 characters. Spaces and redundant parentheses can be removed without changing its tree or leaf count.

The frozen human baseline is 153. `human.py` rebuilds a base-3 Horner expression from the digits of M61. M61 has 39 base-3 digits. Each step multiplies by `1+1+1` and adds zero, one, or two ones for the next digit. This is a reconstruction of a traditional integer-complexity method, not a reported optimum. Altman's survey reviews integer complexity, Selfridge's bound, and Horner representations. [Paper](https://msp.org/cnt/2019/8-3/moscow-v8-n3-p01-s.pdf)

The fixed reference uses 127 ones. The expression is published by EventCompute and in board PR #4. Its SHA-256 is `946a56e064e60422f49c98aeeb0ceae0a99c22d5070318a7b84fcbca28699449`. The page states that generative AI assistants were used in the research, so this is recorded as an AI-assisted public result, not as a human-only discovery. [Result and provenance](https://eventcompute.com/en/challenges/integer-complexity-m61/) · [Board PR #4](https://github.com/math-market/integer-complexity-m61/pull/4)

The board's 150 expression is a challenge baseline, not a record. Its AI provenance is unstated. The public result page, checked on 2026-10-13, reports the 127 construction and lower bound 116, with no exact complexity. We rechecked that page, the board repository, and PR status on 2026-11-06. We found no proof of the exact value or a shorter same-parameter witness. This review covers the cited sources and is not an exhaustive survey.

The simple seed uses binary Horner expansion and is generated from the target alone. The classical baseline enumerates fixed-base Horner expressions. The evolution entry searches mixed-base expansions with a fixed seed. Neither search reads human or reference files. The checker recomputes all formal results with exact integer arithmetic.
