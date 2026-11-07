# T053: Balance the factors of 100000!

## English

For this fixed instance, split `100000!` into exactly 100000 positive integers. Maximize the smallest factor. Do not optimize the ratio between the largest and smallest factors.

The pinned public data file reports the interval `(33641, 33649)` for `t(100000)`. Its lower endpoint is a reported constructive lower bound; the data file does not include its factorization witness. The paper says lower bounds from its numerical factorization work are explicit and checked, but this particular data row has not been independently reproduced here. The reported LP upper endpoint is not a certified bound: the paper says those figure upper bounds were not verified. The published theorem `t(N) <= N/e` gives the rigorous upper bound `t(100000) <= 36787`. The exact value remains open in the sources checked.

The frozen human reference is 33330. `human.py` reconstructs the repository's Sutherland greedy method and converts its subfactorization into exactly 100000 factors of the full factorial. The exact witness is saved under `data/reference/`. `init_program.py`, `baseline.py`, and `evolution.py` start from `1, 2, ..., 100000`; they do not load the human or public witness.

## 中文

本配置固定 `N=100000`。将 `100000!` 分成恰好 100000 个正整数因子，并最大化最小因子。目标不是最大因子与最小因子的比值。

固定版本的公开数据文件报告 `t(100000)` 的区间 `(33641, 33649)`。下端点是公开报告的构造下界，但数据文件没有附上该参数的因子证书。论文说明相关数值下界来自明确因子分解并经过检查；本配置的具体证书尚未由本任务独立复现。报告的 LP 上端点没有经过验证，论文明确指出这些图中的上界尚未验证。已发表定理 `t(N) <= N/e` 给出严格上界 `t(100000) <= 36787`。已核查的来源没有给出该参数的精确值。

冻结的人类参考值为 33330。`human.py` 重建仓库中的 Sutherland 贪心方法，并把子因子分解补成恰好 100000 个因子、乘积为完整阶乘。精确见证保存在 `data/reference/`。`init_program.py`、`baseline.py` 和 `evolution.py` 均从 `1, 2, ..., 100000` 开始，不读取人类或公开见证。
