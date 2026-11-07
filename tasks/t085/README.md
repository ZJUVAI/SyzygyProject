# T085：21 个单位圆覆盖最大圆

## 定义

在平面上选择 21 个半径为 1 的圆心，使其圆盘并集覆盖以原点为圆心的闭圆盘。最大化被覆盖圆盘的半径。圆心可重复。

形式输入使用有理圆心坐标和正有理目标半径。该范围没有大小或分母上限。其与实数模型有相同上确界：把任意可行布局的圆心和目标盘以小于 1 的有理比例向原点缩放，单位覆盖圆的半径不变而覆盖余量增加；随后以有理点近似圆心，并把目标半径有理逼近到缩小后的值。

## 精确覆盖证书

覆盖函数是到最近圆心的距离。它在每个 Voronoi 区域中等于到该区域圆心的距离。有限个圆心把目标盘分成凸的 Voronoi 区域；区域极值只能出现在区域顶点或边界圆弧的极值处。程序逐一检查三圆心等距的内部顶点、两圆心平分线与目标圆的交点、目标圆边界上的各圆心径向极值，并检查轴向代表点以覆盖原点圆心的常值情形。候选点可能包含非 Voronoi 的额外点，这只增加检查，不会漏掉极值。

边界交点含一个平方根。检查器直接判定 `a+b√d` 的符号，其中 `a,b,d` 是有理数。所有判定均精确，不用像素、浮点容差或随机采样。

## 来源与基线

Friedman 的 *Circles Covering Circles* 页面在 2026-11-06 列出 n=21 半径 `3.804+`，归于 Jeremy Tan 2018；该项标为 found。n=11 到 n=20 的新证明不适用于 n=21。该来源没有给出 n=21 最优性证明。页面图保存在 `data/source/`。

已复现的人类方法基线为经典三角格圆覆盖的有限六边形补丁。Kershner 1939 证明平面最薄单位圆格覆盖由三角格达到；这里把标准三角格间距略微缩小，取半径二的 19 个格点，并加两个允许重复的原点圆心。精确检查器验证所得 21 个单位圆覆盖半径 `7/2` 的圆盘。该有限补丁是传统格方法的本地重建，不冒称为 Kershner 的有限实例纪录。冻结人类基线 H=3.5。

## English

Choose 21 unit disks to cover a closed disk centered at the origin. Maximize the target radius. Repeated covering centers are allowed.

The task input uses arbitrary rational centers and a positive rational target radius, with no coordinate or denominator cap. This domain has the same supremum as the real model. Contract all centers and the target disk by a rational factor below one. The unit covering disks stay unchanged, so this creates slack. Approximate the contracted centers by rational points and choose a rational radius that approaches the contracted target radius.

The exact checker uses restricted Voronoi geometry. It checks all interior Voronoi vertices, intersections of pair bisectors with the target circle, smooth boundary distance extrema, and fixed axis points for the constant-distance case. Boundary tests reduce to exact signs of `a+b*sqrt(d)` for rational `a`, `b`, and nonnegative rational `d`. No sampling or floating-point tolerance is used.

Friedman's *Circles Covering Circles* page lists the n=21 construction with radius `3.804+`, credits Jeremy Tan in 2018, and labels it found. The current page still lists n=21 as found; proofs for n=11 through n=20 do not close n=21. The reported n=21 record is not reproduced here. The reproduced baseline is a finite patch of the classical triangular-lattice circle covering. Kershner proved the optimal density of the infinite plane covering in 1939. This task-local finite patch takes 19 lattice sites and two repeated origin centers and exactly covers a radius-3.5 disk. It is a reconstructed traditional method, not a claim that Kershner published this finite witness.

## Files

- `instruction.txt`: model-facing prompt.
- `check.py`: exact continuous coverage checker.
- `init_program.py`: standalone radius-1 seed.
- `baseline.py` and `evolution.py`: seeded center mutation searches with no comparison-data access.
- `human.py`: traditional triangular-lattice patch reconstruction.
- `reference.py`: fixed archived witness.
- `IMPLEMENTATION.md`: sources, proof method, test results, and replay details.
