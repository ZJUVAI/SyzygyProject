# T019: Narrow admissible prime 343-tuples

## English

Return 343 distinct integers. For every prime `p`, at least one residue class modulo `p` must be absent. It is enough to check primes through 343. A prime greater than 343 has more residue classes than the tuple has entries. Minimize `max(tuple) - min(tuple)`. Negative integers and translations are allowed. The checker ignores claimed scores and checks all 68 primes through 343.

Thomas Engelsma's 2013 construction has diameter 2340. The task-local copy of the tuple is checked for distinctness, diameter, and admissibility. The cited source is [MathBases narrow admissible tuples](https://mathbases.org/d/narrow-admissible-tuples), with the downloadable tuple historically hosted at [MIT Prime Gaps](https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt). The source data marks rows through k=342 as optimal and leaves k=343 unmarked. That missing marker is not proof that diameter 2340 is optimal.

The simple seed uses 343 consecutive multiples of the primorial of all primes through 343. It is feasible because every entry is zero modulo each checked prime. The search baseline builds a tuple by greedy residue checks, then tries bounded randomized replacements. It reads no human or reference witness.

## 中文

输出 343 个互不相同的整数。对每个素数 `p`，模 `p` 的剩余类中至少有一类没有出现。只需检查不大于 343 的素数。大于 343 的素数有超过 343 个剩余类，因此不可能全部出现。目标是最小化 `max(tuple) - min(tuple)`。整数可以为负数，也可以整体平移。检查器忽略提交的分数，并检查不大于 343 的全部 68 个素数。

Thomas Engelsma 于 2013 年给出的构造直径为 2340。任务目录中的副本已检查互异性、直径和可容许性。来源为 [MathBases 可容许元组资料](https://mathbases.org/d/narrow-admissible-tuples)，历史下载文件见 [MIT Prime Gaps](https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt)。来源将 `k` 不大于 342 的记录标为最优，未标记 `k=343`。缺少标记不能证明直径 2340 最优。

简单种子取所有不大于 343 的素数之积，并输出其 343 个连续倍数。每个数对所有已检查素数都同余于 0，因此该构造可行。搜索基线先用贪心余数检查构造元组，再进行有界随机替换。它不读取人类或参考见证。

## Additional configurations

T019-C02 fixes `k=1000`; T019-C03 fixes `k=3000`. The linked MIT artifacts contain 1000 and 3000 integers with diameters 7802 and 26606. These exact same-parameter witnesses are saved in `data/human_1000.json` and `data/human_3000.json`; the original line-oriented files are also preserved. Exact checking verifies distinct integers, all primes `p <= k`, and the diameter. The MathBases database page says it covers the narrowest known tuple for every `k=2..5000` and marks proven entries. It was updated 2026-07-14. The new rows are not marked as proven optimal. The MathBases accepted log confirms current records: Engelsma submitted k=1000/H=7802; xfxie submitted k=3000/H=26606. Both rows are accepted, validation-passed, and marked currentRecord=yes. Their description fields are blank; proven rows use the explicit description `optimal` marker. The matching MIT tuple files are saved and independently checked exactly. New configurations are accepted by Sol on 2026-11-07.

C01 retains its accepted primorial-multiple seed. C02/C03 return the first `k` primes strictly greater than `k`. Every entry is odd, so residue 0 is absent modulo 2; the observed diameters are below 50,000 and scores remain finite in the runner. The new seed is self-contained and reads no reference data. For C01 the traditional baseline greedily accepts integers while preserving a missing residue. For C02/C03 it starts from the finite-span prime seed and tries three random replacements, keeping only exact admissible improvements. The evolution search uses interval residue masks, with configurable time and seed, and reads a warm start only when the runner explicitly provides one.

## 中文

T019-C02 固定 `k=1000`，T019-C03 固定 `k=3000`。MIT 文件分别提供 1000 个和 3000 个整数，直径为 7802 和 26606。相同参数的见证保存在 `data/human_1000.json` 和 `data/human_3000.json`，原始逐行文件也保留。精确检查验证互异性、所有 `p <= k` 的素数条件和直径。MathBases 页面说明数据库覆盖 `k=2..5000` 的已知最窄元组，并对已证明最优的条目标记。页面更新日期为 2026-07-14。新条目未标为已证明最优。MathBases accepted log 确认当前记录：Engelsma 提交 k=1000/H=7802，xfxie 提交 k=3000/H=26606。两行均为 accepted、validation-passed 和 currentRecord=yes。description 字段为空；已证明条目使用明确的 `optimal` 标记。对应 MIT 元组文件已保存并精确验算。新增配置已通过 Sol 验收（2026-11-07）。

C01 保留已验收的 primorial 倍数种子。C02/C03 取严格大于 `k` 的前 `k` 个素数。它们都是奇数，所以模 2 缺少余数 0；跨度低于 50,000，评分转换保持有限。新种子自包含且不读取参考数据。C01 传统基线逐个加入整数，并确保每个素数至少保留一个缺失余数；C02/C03 从有限跨度素数种子开始，尝试三次随机替换，只保留精确可容许的改进。演化搜索使用区间余数掩码，并支持固定时间和随机种子。它只在运行器显式提供热启动路径时读取该路径。
