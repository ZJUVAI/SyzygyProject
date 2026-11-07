# T099: order of the P1 11-omino

## Definition

The fixed tile is the 11-cell polyomino `11P1` shown in the source. A candidate tiles any axis-aligned rectangle with congruent copies. Translations, quarter-turn rotations, and reflections are allowed. The rectangle size is part of the construction and is not fixed. Minimize the number of tiles.

Each tile has 11 cells, so a valid rectangle has area `11 * tile_count`. The exact checker applies each D4 orientation to the fixed cell set, checks that tile cells stay within the rectangle, rejects overlaps, and confirms that the union covers every rectangle cell.

## Human result and open status

The source gives a 54 by 55 rectangle filled by 270 copies. I decoded its SVG and checked all 2,970 cells exactly. The source attributes this tiling to Michael Reid's 11-omino page; the MIT Tiling Search archive also lists a 270-copy 54 by 55 construction and cites the 1997 Dahlke/Wichmann construction record.

The current polyominoes.org page labels the order `<= 270` and calls 54 by 55 the smallest known rectangle. It does not give a proof that no rectangle can be tiled with fewer than 270 copies. The 270 tiling is therefore a verified upper bound, not a proved minimum. No proof closing this gap was found in the sources checked through 2026-11-06.

## Independent seed and search

An offline single-thread exact-cover search used only the fixed 11-cell shape and the 54 by 55 board dimensions. It found a separate 270-tile tiling in 477.481 seconds with seed `20261106`. The saved result is in `best/independent_cpsat_seed_270.json`. The initial program repeats this self-generated tiling twice to give a valid 540-tile seed on a 54 by 110 rectangle. The traditional search checks tile-aligned rectangular cuts and finds a 270-tile subrectangle. The evolutionary search mutates rectangle symmetries and keeps lower-count cut candidates. Neither search reads the human or reference witness.

The Reid source also lists a 47 by 99 rectangle with 423 copies. This is a weaker reported construction and does not change the highest checked feasible result of 270.

## Sources

- [Polyominoes.org: P1 11-omino](https://polyominoes.org/data/11P1)
- [Michael Reid: Primes of the 11-omino](https://sicherman.net/mikereid/11omino7_rect.html)
- [MIT Tiling Search: 11-omino, order 270, 54 by 55](https://tilingsearch.mit.edu/HTML/data113/K12.html)

The shape cells, source page hash, symmetry convention, and verified public tiling are recorded under `data/source` and `data/reference`. The configuration remains `accepted_by_sol`.

# T099：P1 11 连方格最小铺砌阶数

## 定义

固定方块为来源中的 11 格多连方格 `11P1`。用它的平移、旋转和镜像复制铺满任意轴对齐整数矩形。矩形尺寸由构造决定。目标是最小化方块数量。

每块含 11 格，因此矩形面积必须等于 `11 × 方块数`。精确检查器应用全部 8 种 D4 对称，检查方块没有越界或重叠，并确认矩形每格都被覆盖。

## 人类结果与开放状态

来源给出 54×55 矩形的 270 块铺砌。我们解码 SVG，并逐格复核了 2,970 格。来源将此构造归于 Michael Reid 的 11 连方格页面。MIT Tiling Search 也列出 54×55、270 块的构造，并引用 1997 年 Dahlke/Wichmann 记录。

当前 polyominoes.org 页面标记阶数为 `<= 270`，并称 54×55 是当前已知最小矩形。页面没有证明少于 270 块无法铺满其他矩形。因此 270 是已验证的可行上界，不是已证最小值。我们在截至 2026-11-06 检查的来源中没有找到闭合此差距的证明。

## 独立起点与搜索

离线单线程精确覆盖搜索只使用固定的 11 格形状与 54×55 矩形尺寸。随机种子 `20261106` 在 477.481 秒后找到另一份 270 块铺砌，保存在 `best/independent_cpsat_seed_270.json`。初始程序将这份自有铺砌复制两次，得到 54×110 矩形的 540 块有效起点。传统搜索检查与方块边界对齐的矩形切口，并找到 270 块子矩形。演化搜索改变矩形对称和切口，并保留块数较少的候选。两种搜索都不读取人类或参考见证。

Reid 来源还列出 47×99 矩形的 423 块构造。该构造较弱，不改变本配置已核实的最高可行结果 270。

## 来源

- [Polyominoes.org：P1 11 连方格](https://polyominoes.org/data/11P1)
- [Michael Reid：11 连方格素数铺砌](https://sicherman.net/mikereid/11omino7_rect.html)
- [MIT Tiling Search：11 连方格，270 阶，54×55](https://tilingsearch.mit.edu/HTML/data113/K12.html)

形状格点、来源页面哈希、对称定义和已验证公开铺砌保存在 `data/source` 与 `data/reference`。当前状态为 `accepted_by_sol`。
