# T069: Mona Lisa 100K Euclidean TSP

## Definition

Use the fixed `mona-lisa100K` set of 100,000 integer-coordinate cities. Return one closed Hamiltonian cycle. Each city must occur exactly once; the last city connects back to the first. Minimize the sum of the 100,000 TSPLIB `EUC_2D` edge weights. For coordinate difference `(dx,dy)`, the edge weight is the nearest integer to `sqrt(dx*dx+dy*dy)`.

The exact checker uses integer square roots and the threshold comparison `4*squared >= (2*floor_sqrt+1)^2`. It verifies a full permutation and recomputes every edge, including the return edge. Floating-point distance sums are not used.

## Fixed data and current status

The official Waterloo challenge page defines the 100K instance and currently lists a tour of 5,757,191, a lower bound of 5,757,084, and a gap of 107. Its March 17, 2009 log credits Yuichi Nagata's genetic algorithm and links the tour. The local input and tour are pinned by SHA-256 in `sota.json`.

Cook, Helsgaun, Hougardy and Schroeder's 2024 paper, §3.1, says that `mona-lisa100k` has not been solved to proven optimality. The selected finite instance therefore remains open in the sources checked on 2026-11-06. The reported lower bound is recorded as published; this task does not re-certify Concorde's proof file.

The same-parameter public Nagata tour is the human-method and fixed reference witness. `human.py` and `reference.py` read separate frozen copies. The source attributes the tour to a genetic algorithm, not generative AI. T069 is an unconstrained Hamiltonian cycle problem. It has no vehicle capacity or route-count constraint; T057 is a separate CVRP model.

## Search entries

The simple initial program returns city IDs in input order. The fixed-seed traditional baseline sorts cities by 100-unit horizontal coordinate bands, reverses alternate bands, then attempts a fixed number of local random 2-opt exchanges. It reads the public coordinate instance only. It does not read either comparison tour. The bounded search uses 20,000 exchange proposals by default; `MATHBENCH_SEARCH_SECONDS` can set an exploratory wall-clock cutoff.

## Sources

- [Mona Lisa TSP Challenge](https://www.math.uwaterloo.ca/tsp/data/ml/monalisa.html): official instance, current tour and bound, computation log, and Nagata tour link.
- [Official 100K TSPLIB instance](https://www.math.uwaterloo.ca/tsp/data/ml/mona-lisa100K.tsp).
- [Local elimination in the traveling salesman problem](https://link.springer.com/article/10.1007/s12532-024-00262-y), Mathematical Programming Computation 16 (2024), §3.1: lists this instance among those not solved to proven optimality.

## Reproduction

Set `MATHBENCH_CONFIG_ID=T069-C01` and run any of the five `run_code()` entries. Run the task checks with:

```sh
.venv/bin/python -m pytest tasks/t069/test_task.py -q
```

---

# T069：Mona Lisa 100K 欧氏旅行商问题

## 定义

固定使用 `mona-lisa100K` 的 100,000 个整数坐标城市。输出一个闭合 Hamilton 圈。每个城市恰好出现一次，最后一个城市连接回第一个城市。最小化 100,000 条 TSPLIB `EUC_2D` 边权之和。对坐标差 `(dx,dy)`，边权是 `sqrt(dx*dx+dy*dy)` 四舍五入到最近整数。

精确检查器用整数平方根和阈值 `4*squared >= (2*floor_sqrt+1)^2` 判断舍入结果。它检查全排列，并重算包括回边在内的每条边。目标值不使用浮点距离和。

## 固定数据与当前状态

Waterloo 官方挑战页定义该 100K 实例，并列出长度 5,757,191 的圈、下界 5,757,084 和差距 107。2009 年 3 月 17 日记录将该圈归于 Yuichi Nagata 的遗传算法，并链接旅程文件。本地实例与旅程的 SHA-256 保存在 `sota.json`。

Cook、Helsgaun、Hougardy 和 Schroeder 2024 年论文第 3.1 节称 `mona-lisa100k` 尚未证明最优。因此，截至 2026-11-06 检查的来源，这个固定实例仍开放。已发表下界按来源记录，本任务不重新证明 Concorde 证书。

同参数公开 Nagata 旅程同时作为人类方法和固定参考见证。`human.py` 与 `reference.py` 分别读取独立冻结副本。来源说明该旅程由遗传算法找到，没有生成式 AI 参与信息。T069 是无容量限制的 Hamilton 圈问题，没有车辆容量或车辆数限制；T057 是不同的 CVRP 模型。

## 搜索入口

简单初始程序按输入顺序返回城市编号。固定种子的传统基线先按 100 单位高的水平坐标带排序，并反转相邻带的扫描方向，再尝试固定次数的局部随机 2-opt 交换。它只读取公开坐标实例，不读取对照旅程。默认尝试 20,000 次交换；可用 `MATHBENCH_SEARCH_SECONDS` 设置探索时限。

## 来源

- [Mona Lisa TSP Challenge](https://www.math.uwaterloo.ca/tsp/data/ml/monalisa.html)：官方实例、当前旅程和下界、计算记录及 Nagata 旅程链接。
- [官方 100K TSPLIB 实例](https://www.math.uwaterloo.ca/tsp/data/ml/mona-lisa100K.tsp)。
- [Local elimination in the traveling salesman problem](https://link.springer.com/article/10.1007/s12532-024-00262-y)，*Mathematical Programming Computation* 16 (2024), 第 3.1 节：将该实例列为尚未证明最优的实例。

## 复现

设置 `MATHBENCH_CONFIG_ID=T069-C01` 并运行五个 `run_code()` 入口之一。运行任务测试：

```sh
.venv/bin/python -m pytest tasks/t069/test_task.py -q
```
