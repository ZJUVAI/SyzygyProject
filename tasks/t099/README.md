# T099: Narrow admissible prime 343-tuples

## English

Return 343 distinct integers. For every prime `p`, at least one residue class modulo `p` must be absent. It is enough to check primes through 343. A prime greater than 343 has more residue classes than the tuple has entries. Minimize `max(tuple) - min(tuple)`. Negative integers and translations are allowed. The checker ignores claimed scores and checks all 68 primes through 343.

Thomas Engelsma's 2013 construction has diameter 2340. The task-local copy of the tuple is checked for distinctness, diameter, and admissibility. The cited source is [MathBases narrow admissible tuples](https://mathbases.org/d/narrow-admissible-tuples), with the downloadable tuple historically hosted at [MIT Prime Gaps](https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt). The source data marks rows through k=342 as optimal and leaves k=343 unmarked. That missing marker is not proof that diameter 2340 is optimal.

The simple seed uses 343 consecutive multiples of the primorial of all primes through 343. It is feasible because every entry is zero modulo each checked prime. The search baseline builds a tuple by greedy residue checks, then tries bounded randomized replacements. It reads no human or reference witness.

## 中文

输出 343 个互不相同的整数。对每个素数 `p`，模 `p` 的剩余类中至少有一类没有出现。只需检查不大于 343 的素数。大于 343 的素数有超过 343 个剩余类，因此不可能全部出现。目标是最小化 `max(tuple) - min(tuple)`。整数可以为负数，也可以整体平移。检查器忽略提交的分数，并检查不大于 343 的全部 68 个素数。

Thomas Engelsma 于 2013 年给出的构造直径为 2340。任务目录中的副本已检查互异性、直径和可容许性。来源为 [MathBases 可容许元组资料](https://mathbases.org/d/narrow-admissible-tuples)，历史下载文件见 [MIT Prime Gaps](https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt)。来源将 `k` 不大于 342 的记录标为最优，未标记 `k=343`。缺少标记不能证明直径 2340 最优。

简单种子取所有不大于 343 的素数之积，并输出其 343 个连续倍数。每个数对所有已检查素数都同余于 0，因此该构造可行。搜索基线先用贪心余数检查构造元组，再进行有界随机替换。它不读取人类或参考见证。
