# T012 和差问题 I

目标是在整数区间 `[-1000000,1000000]` 中选取 2 至 512 个不同整数，最大化 `log(|A+A|/|A|)/log(|A-A|/|A|)`。验证器用整数精确计算和集与差集，并用向外舍入区间给出目标值下界。

已复现的人类参考来自 Martin 与 O'Bryant 对 Pigarev-Freiman 构造的重列：17 元集合的和集大小为 59，差集大小为 55。来源：[arXiv:math/0608131](https://arxiv.org/abs/math/0608131)。同参数的当前最佳可复现公开构造来自 SimpleTES。其 506 元见证的和集大小为 3551，差集大小为 2775。本地精确复算得 1.144886859713313…，与论文四舍五入值 1.144887 一致。见 [sota.json](sota.json) 与 [sota_witness.json](sota_witness.json)。Dream-RSI 的论文和项目页另报告 1.145427。其公开代码仓库任务说明及抓取脚本确认它使用相同目标和约束，但没有发布该结果的见证，所以该值尚未复现。

# T012 Sum-difference I

Choose 2 to 512 distinct integers in `[-1000000,1000000]` to maximize `log(|A+A|/|A|)/log(|A-A|/|A|)`. The verifier computes both sets exactly and uses outward-rounded intervals to report a conservative objective lower bound.

The reproduced human reference is the 17-element Pigarev-Freiman construction reproduced by Martin and O'Bryant: sumset size 59 and difference-set size 55. Source: [arXiv:math/0608131](https://arxiv.org/abs/math/0608131). The best reproducible public construction found for these parameters is the 506-element SimpleTES witness. It has sumset size 3551 and difference-set size 2775. Exact local recomputation gives 1.144886859713313…, which rounds to the paper's 1.144887. See [sota.json](sota.json) and [sota_witness.json](sota_witness.json). Dream-RSI's paper and project page report a higher score, 1.145427. Its code repository's task README and fetch script confirm the same objective and constraints, but the public repositories do not release that witness, so this score is not reproduced.
