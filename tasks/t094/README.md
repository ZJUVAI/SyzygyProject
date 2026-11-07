# 正 120 边形的最小伸长三角剖分

## 定义

输入是顶点按逆时针编号的正 120 边形。构造只能使用这些顶点。输出须包含全部 120 条边界边和 117 条对角线，且内部没有相交边。

对每一对不同顶点，计算三角剖分图中的最短路长度，再除以这两点的欧氏弦长。目标是最小化所有顶点对中最大的比值。评分器以有理区间认证每条弦长和最短路；返回区间上端作为保守目标值。搜索可以使用浮点数作反馈，但浮点值不作为正式证书。

## 来源与状态

Fekete、Keldenich、Perk 的 2026 年论文给出了正 n 边形在 4≤n≤100 范围内的最优解。120 不在该范围内。2026-11-06 查阅的来源没有给出 120 边形的闭合最优性证明。

UBC 的 Theory Problem Solving Group 页面给出 n 能被 6 整除时的 6-fan 构造：先画内接等边三角形，再将其余顶点连向最近的三角形顶点；等距顶点连向两端。该页证明其伸长率随 n 增大趋近 1.45595。这里按该公式构造正 120 边形见证，并用本地认证评分器重算，得到区间

`[2890016242467687188760789/1993834667466255952395547, 481669373744614531460135/332305777911042658732591]`，

上端约为 1.4494763731539935。记录中的兼容对照值向上舍入为 1.449476373154。

Sattari 与 Izadi 证明任意正多边形的顶点有一组三角剖分，其伸长率小于 1.4482。这是公开理论上界；本任务没有重建其正 120 边形具体见证。该界不是本任务的冻结人类参考分数。

## 运行

使用 `MATHBENCH_CONFIG_ID=T094-C01`。简单起点是从顶点 0 发出的扇形三角剖分。传统搜索随机生成递归分割三角剖分，并按浮点评分保留较优结果；默认 6 次，种子来自 `MATHBENCH_SEED`。人类和固定参考入口均返回 6-fan 见证。

```sh
.venv/bin/python -m pytest tasks/t094/test_task.py -q
```

本配置已通过 Sol 验收（2026-11-06）。

## English

### Definition

The input is a regular convex 120-gon. Its vertices have counterclockwise labels 0 to 119. A valid output contains all 120 boundary edges and 117 diagonals. No two edges may cross in their interiors.

For each pair of distinct vertices, divide the shortest path length in the triangulation by the Euclidean chord length. The objective is to minimize the maximum ratio. The checker uses rational intervals for chord lengths and shortest paths. It returns a conservative upper bound. Floating-point scores may guide search, but they are not certificates.

### Sources and status

Fekete, Keldenich, and Perk (2026) report optimal regular n-gon triangulations for 4≤n≤100. This range does not include 120. Sources checked on 2026-11-06 did not show a proof that closes the 120-gon case.

The UBC Theory Problem Solving Group describes the 6-fan for n divisible by six: inscribe an equilateral triangle, then connect each other vertex to its closest triangle vertex. Connect both vertices in a tie. The page gives an asymptotic dilation near 1.45595. We rebuilt this construction for n=120 and certified its score. Its interval is

`[2890016242467687188760789/1993834667466255952395547, 481669373744614531460135/332305777911042658732591]`.

The upper endpoint is about 1.4494763731539935. The compatibility reference is rounded up to 1.449476373154.

Sattari and Izadi prove an upper bound below 1.4482 for every regular polygon. We did not rebuild their specific 120-gon witness. This theorem bound is not the frozen human reference score.

### Run

Set `MATHBENCH_CONFIG_ID=T094-C01`. The simple seed is a fan from vertex 0. The conventional search samples recursive split triangulations and keeps the best floating-point feedback score. It uses six trials by default and reads the seed from `MATHBENCH_SEED`. The human and fixed-reference entries return the 6-fan witness.

Status: accepted by Sol on 2026-11-06.
