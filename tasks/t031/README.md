# T031：七符号最短超排列

## 中文

本任务固定字母表 `1` 至 `7`。候选须返回一个字符串，使每个七符号排列都至少出现一次，且必须作为长度为 7 的连续子串出现。目标是最小化字符串长度。校验器检查所有长度为 7 的窗口，并精确重算长度。重复出现的排列允许；声明分数不会用于评分。

唯一配置为 T031-C01，共有 5040 个目标排列。配置状态为“已通过 Sol 验收（2026-11-06）”。

公开来源中，Andrei Teodorescu 于 2026-08-17 发布了长度 5905 的字符串及搜索代码线索。Andrew Balint 报告检查了全部 5040 个排列。我们下载其中一个附件，并独立重算出 5905 个字符和 5040 个排列。公开来源没有说明是否使用 AI，因此记录为来源未披露。

Ashlock 与 Tillotson 的递归构造可重建长度 5913 的同参数人类方法基线。`human.py` 从底层递归规则生成见证，保存于 `data/reference/human_ashlock_tillotson_5913.txt`，并由校验器逐窗口复核。公开的 5905 见证保存于 `data/reference/public_5905_attachment.txt`。这两个文件仅供对照，不进入简单初始程序或传统搜索。这个值不是公开纪录。

最优性尚未确定。当前 5901 下界包标明部分 Lean 方程尚未求值，且多项搜索计数依赖单一程序。本任务不把它作为完整复核的证明。另一份公开 Lean 工件给出下界 5898，但依赖本机原生求值与编译工具链。最佳公开上界 5905 与下界之间仍有缺口。

初始程序独立拼接 5040 个排列，不读取比较见证。传统基线对所有排列做带种子的最大重叠贪心搜索，也不读取比较见证。

## English

This task fixes the alphabet `1` through `7`. A candidate returns a string that contains every permutation of the seven symbols at least once. Each permutation must occur as a contiguous substring of length 7. The objective is to minimize the string length. The checker reads every length-7 window and recomputes the length. A permutation may occur more than once. The checker ignores claimed scores.

The only configuration is T031-C01. It requires all 5,040 permutations. Its status is accepted by Sol on 2026-11-06.

Andrei Teodorescu posted a 5,905-symbol string and search-code details on 2026-08-17. Andrew Balint reported checking all 5,040 permutations. We downloaded one attachment and independently counted 5,905 symbols and all 5,040 permutations. The public source does not say whether AI contributed. The record marks its AI provenance as undisclosed.

Ashlock and Tillotson's recursive construction can be rebuilt as a same-parameter human-method baseline of length 5,913. `human.py` generates the witness from the recursive rule. The saved witness is `data/reference/human_ashlock_tillotson_5913.txt`. The public 5,905 witness is saved in `data/reference/public_5905_attachment.txt`. These files are comparison assets. The initial program and traditional search do not read them. The checker verifies every window. This value is not the public record.

Optimality is unknown. The current package for the 5,901 lower bound says that some Lean equations have not been evaluated. Many search counts rely on one program. This task does not treat that result as a fully replayed proof. A separate public Lean artifact gives a lower bound of 5,898, with a native evaluator and compiler toolchain in its trust base. A gap remains between the 5,905 public construction and the lower bound.

The initial program concatenates all 5,040 permutations. It does not read comparison witnesses. The traditional baseline uses a seeded maximum-overlap greedy search over all permutations. It also does not read comparison witnesses.
