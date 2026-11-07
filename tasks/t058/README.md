# T058: Social Golfer schedule for 35 players in groups of 5

## Definition

Schedule 35 players in 7 groups of 5 for each round. Every player must appear once in every round. Any pair of players may share a group at most once. The objective is to maximize the number of rounds.

For one player, each round uses 4 previously unseen partners. There are 34 other players, so the number of rounds is at most `floor(34/4)=8`.

The reproduced 7-round reference is the resolvable transversal design `RTD(5,7)`. Label players by pairs `(a,b)` with `a in {0,...,4}` and `b in F_7`. For each `t,c in F_7`, form one group from `(a, t*a+c mod 7)` for all five values of `a`. For each fixed `t`, each player occurs in exactly one of the seven groups. Two points with different first coordinates meet for at most one value of `t`; two points with the same first coordinate never meet. Thus the seven rounds satisfy the exact pair condition.

## Current result and open status

Miller, Valkov, and Abel's 2026 supplementary Table 4 lists the `(v=35,k=5)` case with `MAX=8`, construction `RTD(5,7)`, and `r=7`. Their paper uses “optimal” for the best currently known schedule. It uses “maximal” for a schedule that reaches the theoretical upper bound. The 7-round schedule is therefore a reproduced lower bound. The row does not prove that 8 rounds are impossible.

The OEIS entry for `T(7,5)` currently says the maximum is either 7 or 8. We checked it on 2026-11-06; we did not check its entry revision history. The checked sources give a 7-round construction and an upper bound of 8. We found no 8-round construction or proof that rules one out. The configuration remains open on that evidence.

The 2021 paper's Lemma 3 proves the bound is not attained for the separate case of 20 players in groups of 4, and its 32-player, groups-of-4 example reaches 10 rounds. Those cases are excluded here. This configuration is 35 players and groups of 5.

Primary sources checked 2026-11-06:

- Miller, Valkov, and Abel, [Combinatorial Solutions to the Social Golfer Problem and the Social Golfer Problem with Adjacent Group Sizes](https://doi.org/10.3390/sym18020269), 2026. The [supplementary material](https://eprints.gla.ac.uk/377866/4/377866_suppl.pdf), Table 4, lists the exact parameters, 7-round RTD construction, and upper bound 8.
- [OEIS A107431](https://oeis.org/A107431), checked 2026-11-06, currently states that `T(7,5)` is 7 or 8. The entry revision history was not checked.
- Miller et al., [Breakout group allocation schedules and the social golfer problem with adjacent group sizes](https://doi.org/10.3390/sym13010013), 2021, Lemma 3, for the excluded 20-player, groups-of-four case.

## Programs and limits

- `init_program.py` returns one valid round in contiguous groups. It imports no task modules and reads no comparison data.
- `baseline.py` builds rounds by randomized greedy partitions. The default is eight restarts and at most 5000 random partitions for each added round. It uses only the fixed rules and seed.
- `human.py` rebuilds the published RTD construction over the finite field `F_7`.
- `reference.py` reads the fixed 7-round witness saved under `data/reference/`.
- `evaluator.py` uses the shared runner. Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread.

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t058/test_task.py -q
.venv/bin/python -m json.tool tasks/t058/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t058/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t058/records.json > /dev/null
```

## 定义

每轮把 35 人分成 7 组，每组 5 人。每轮中每人恰好出现一次。任何两人最多同组一次。目标是最大化轮数。

对固定的一人，每轮会遇到 4 个新搭档。其余共有 34 人，所以轮数上限是 `floor(34/4)=8`。

已复现的 7 轮构造是可解横截设计 `RTD(5,7)`。用 `(a,b)` 表示球员，其中 `a` 取 0 至 4，`b` 属于有限域 `F_7`。对每个 `t,c in F_7`，将五个 `(a, t*a+c mod 7)` 放入同一组。固定 `t` 后，每人恰好进入七组中的一组。首坐标不同的两点最多在一个 `t` 下同组，首坐标相同的两点不会同组。因此七轮满足精确的搭档约束。

## 当前结果和开放状态

Miller、Valkov 和 Abel 的 2026 年附表 4 对 `(v=35,k=5)` 列出 `MAX=8`、构造 `RTD(5,7)` 和 `r=7`。论文用 “optimal” 表示当前已知的最佳构造，用 “maximal” 表示达到理论上界。七轮是已复现的下界。表中没有证明八轮不可能。

OEIS 的 `T(7,5)` 条目当前说明最大轮数是 7 或 8。本次于 2026-11-06 核对了条目内容，没有核对条目修订历史。当前来源给出七轮构造和八轮上界。未发现八轮见证或排除八轮的证明，因此按这些来源该参数仍开放。

2021 年论文引理 3 证明了 20 人、每组 4 人的另一参数无法达到其轮数上界；其 32 人、每组 4 人示例达到 10 轮。这两种情况不在本配置中。本配置固定 35 人、每组 5 人。

上方英文列出了核查日期和来源。任务状态为已通过 Sol 验收（2026-11-06）。
