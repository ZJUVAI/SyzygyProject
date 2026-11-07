# T035: Erdős–Szekeres 点集，不含凸七边形

## 中文

给定平面上的互异点。任意三点不得共线。目标是最大化点数，并要求任取七点都不处于凸位置。禁用的凸七边形无需为空；其它提交点可以在其凸包内。配置 T035-C01 固定禁止的凸多边形顶点数为 7。得分是点数。

本任务优化可行点集的大小，不直接输出未知数 `ES(7)`。Erdős–Szekeres 与 Szekeres 的经典构造给出 32 点下界。Duque、Fabila-Monroy 与 Hidalgo-Toscano 解释了该构造的整数坐标实现；本文按论文中的递归构造重新生成坐标，没有从图像估读坐标。公开实现入口为 [PyDCG](https://github.com/rfabila/PyDCG)。来源版本和文件摘要见 `data/source_hashes.json`。

递归构造产生 32 个整点。评测器使用整数行列式检查一般位置，并精确搜索任意七点凸集。坐标接受整数或有理数字符串（如 `"3/5"`）；浮点数会被拒绝。已报告的区间为 `33 ≤ ES(7) ≤ 81`；`ES(7)=33` 仍是猜想。上界来自 Schroeder 于 2026-09-19 发布的预印本，本任务未重做其上界证明。Dumitru 的 2025 年笔记称 ES(7) 是首个未解决的平面情形。没有把点集大小限制为 32；更大的可行见证可以提交。

初始程序给出抛物线上的 6 点。传统基线使用固定种子 0，对当前集合尝试加入整数点；它不读取公开见证。默认生成预算 300 秒，正式检查预算 60 秒。当前状态：已通过 Sol 验收（2026-11-06）。

主来源：

- Erdős and Szekeres, “On some extremum problems in elementary geometry” (1961), [paper](https://sziami.cs.bme.hu/~geza/erdosszekeres61.pdf).
- Duque, Fabila-Monroy, and Hidalgo-Toscano, “Point Sets with Small Integer Coordinates and with Small Convex Polygons,” arXiv:1602.03075v2 (2017-07-12), [paper](https://arxiv.org/abs/1602.03075v2), [source code cited by the paper](https://github.com/rfabila/PyDCG).
- Dumitru, “Notes on the 33-point Erdős–Szekeres problem,” arXiv:2512.24061v1 (2025), [paper](https://arxiv.org/abs/2512.24061).
- Schroeder, “Upper Bounds for Convex Heptagons and Octagons,” version 1 (2026-09-19), [paper and proof materials](https://michaelschroeder.ai/research/ErdosSzekeres/companion).

## English

Given distinct points in the plane, require that no three are collinear. Maximize the number of points while forbidding every seven-point subset from being in convex position. A forbidden convex seven-gon need not be empty; other submitted points may lie inside its hull. Configuration T035-C01 fixes the forbidden polygon size at 7. The score is the number of points.

This task maximizes the size of a feasible point set. It does not return the unknown threshold `ES(7)`. The classical Erdős–Szekeres construction gives a 32-point lower bound. Duque, Fabila-Monroy, and Hidalgo-Toscano describe an integer-coordinate realization. This task rebuilds the recursive construction and does not estimate coordinates from a figure. The public implementation entry point is [PyDCG](https://github.com/rfabila/PyDCG). Source versions and hashes are in `data/source_hashes.json`.

The recursive construction produces 32 integer points. The checker uses integer determinants for general position and an exact search for any convex seven-point subset. Coordinates may be integers or rational strings such as `"3/5"`; floats are rejected. The reported interval is `33 ≤ ES(7) ≤ 81`; `ES(7)=33` remains a conjecture. The upper bound is from Schroeder's preprint dated 2026-09-19. This task has not reproduced that upper-bound proof. Dumitru's 2025 notes identify ES(7) as the first open planar case. The input is not capped at 32; larger feasible witnesses are allowed.

The initial program returns six points on a parabola. The traditional baseline uses fixed seed 0 and tries to add integer points to the current set. It does not read the public witness. The default generation budget is 300 seconds. The formal check budget is 60 seconds. Status: accepted by Sol on 2026-11-06.

Primary sources:

- Erdős and Szekeres, “On some extremum problems in elementary geometry” (1961), [paper](https://sziami.cs.bme.hu/~geza/erdosszekeres61.pdf).
- Duque, Fabila-Monroy, and Hidalgo-Toscano, “Point Sets with Small Integer Coordinates and with Small Convex Polygons,” arXiv:1602.03075v2 (2017-07-12), [paper](https://arxiv.org/abs/1602.03075v2), [source code cited by the paper](https://github.com/rfabila/PyDCG).
- Dumitru, “Notes on the 33-point Erdős–Szekeres problem,” arXiv:2512.24061v1 (2025), [paper](https://arxiv.org/abs/2512.24061).
- Schroeder, “Upper Bounds for Convex Heptagons and Octagons,” version 1 (2026-09-19), [paper and proof materials](https://michaelschroeder.ai/research/ErdosSzekeres/companion).
