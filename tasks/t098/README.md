# T098：38 阶本原简单完美平方正方形

## 数学目标

把一个整数边长正方形剖分为 38 个轴平行的小正方形。小正方形边长均为正整数且两两不同（完美）；任意真子矩形都不能由至少两个小正方形铺满（简单）；38 个边长的最大公约数为 1（本原）。目标是最小化外正方形边长。允许小正方形沿边接触。

固定配置为 `T098-C01`。验证器用整数坐标检查边界、面积、两两内部不相交、边长互异和本原性。它列举所有由小正方形边界确定的候选矩形，并检查其中是否有真子矩形被完整铺满。所有计算均为整数运算。

## 已知构造与开放状态

Squaring.net 的目录将 38 阶及以上标为不完整，并列出 Williams 2013 的 38 阶边长 352 构造。OEIS A129947 将 38–59 项称为上界，并给出 38 阶上界 352。因此 352 是已知可行上界，不能据此称为最优。我们在 2026-11-06 检查的来源没有给出 38 阶匹配下界或最优性证明；这不是穷尽式文献调查。

- Squaring.net：<https://www.squaring.net/sq/ss/spss/spss.html>，order 38 与 Williams 2013 条目。
- OEIS A129947：<https://oeis.org/A129947>，说明该段数据是 upper bounds。
- 原始研究软件及档案目录：<https://www.squaring.net/downloads/downloads.html>。

`human.py` 从公开的 `38 352A` Bouwkamp 代码重建 352 构造。这个过程按整数 skyline 放置方块。构造经本任务验证器复算。历史上的 Brooks 1950 边长 4920 只作为较弱旧纪录记载。

## 程序入口

五个程序都导出 `run_code()`。输出包含 `side` 和 38 个 `[x, y, side]` 整数三元组。

- `init_program.py` 返回独立网络搜索得到的边长 4755 构造。它把自身生成的方块坐标写在程序中，不读取对照文件。
- `baseline.py` 先精确改变一个小方块边长，并同时改变目标外边长，使总面积仍为完全平方数；然后打乱自有 B-code 分组并用 skyline 建造器尝试重建。默认 40 次，种子来自 `MATHBENCH_SEED`；`T098_SEARCH_ITERS` 可设为 0–1000。无法重建或未通过完整检查的候选会被跳过。无改进时返回4755保底构造。
- `human.py` 重建公开的 Williams 38 352A 构造。
- `reference.py` 从固定的对照文件重建同一构造。
- `evolution.py` 将传统搜索暴露为任务化入口。

边长 4755 的起点由一次独立研究搜索生成。使用的 Williams C++ 源码来自 [官方压缩包](https://squaring.net/downloads/jbwsrc.zip)，SHA-256 为 `80e780853283dbaea387e5eb44511903904a21e520baa1a70be89bedb55bd84b`。保存的元数据列出编译器版本和命令。搜索分别生成 `graphgen 23 14` 与 `graphgen 25 16` 的网络前缀，数量为 1,391,846 和 370,992，每段限时 60 秒，再按压缩包中的脚本排序并配对 M/F 网络。原始中间前缀没有保留，所以重放命令能重跑同一公开算法和参数，但不能保证复现这一个构造。已保存的坐标单独通过完整精确检查。基准初始程序固定返回此有效起点。

默认运行预算为生成 300 秒、验证 60 秒、4 GiB 内存和一个计算线程。基准不读取 human/reference 对照文件。模型不应访问 `data/` 对照资产。

## 评分与验证限制

目标分数是外正方形整数边长，越小越好。验证器完全忽略候选附带的 `objective`、`score` 和 `claimed_score`。有效构造才产生目标分数。边长 352 与 4755 均为构造分数，不代表已证明全局最优。

---

# T098: primitive simple perfect squared square of order 38

## Mathematical objective

Tile an integer-sided square with 38 axis-aligned integer-sided squares. The 38 positive side lengths must be distinct (perfect), their greatest common divisor must be 1 (primitive), and no proper rectangle may be tiled by a subset of at least two squares (simple). Minimize the outer square side.

The checker uses exact integer arithmetic. It checks containment, area, pairwise interior disjointness, distinct side lengths, primitivity, and every candidate rectangle whose sides lie on tile boundaries. A proper rectangle is tiled when the total area of its contained tiles equals its area.

## Sources and status

The squaring.net catalogue marks orders 38 and above incomplete and lists a Williams 2013 order-38 construction with side 352. OEIS A129947 labels the order-38-to-59 values as upper bounds and gives 352 for order 38. The sources checked on 2026-11-06 do not provide a matching lower bound or proof of optimality. This is not an exhaustive literature review.

The human entry rebuilds the public `38 352A` Bouwkamp code by exact integer skyline placement. The historical Brooks 1950 construction of side 4920 is recorded separately as a weaker result.

## Programs and limits

All five programs expose `run_code()`. `init_program.py` returns an independently generated side-4755 seed and reads no comparison files. `baseline.py` tries a fixed number of deterministic strip permutations of that seed. `human.py` reconstructs the published side-352 construction. `reference.py` reads the frozen comparison record. `evolution.py` exposes the search baseline.

Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB of memory, and one compute thread. The public comparison files are external assets and must not enter the model's initial context.
