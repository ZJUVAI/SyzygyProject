# T057: capacitated vehicle routing for X-n1001-k43

## Definition

The fixed instance has depot node 1 and 1000 customers, with TSPLIB node IDs 2 through 1001. Each customer has a positive integer demand. Every route starts and ends at node 1, and its total demand must not exceed the vehicle capacity 131. Every customer must appear once across all routes.

The number of routes is not fixed and has no upper bound in this benchmark definition. The `k43` suffix is part of the instance name. It is not a fleet limit. The official DIMACS rules state that no route-count restriction applies to any instance, and they explicitly accept 9 routes for E-n101-k8. Here total demand is 5557, so the capacity bound forces at least `ceil(5557/131)=43` routes. A solution may use more than 43.

The objective minimizes total travel distance. For consecutive nodes `i,j`, including depot legs, the edge cost is the TSPLIB `EUC_2D` nearest-integer distance:

`d(i,j) = nint(sqrt((x_i-x_j)^2 + (y_i-y_j)^2))`.

The checker computes this exactly. If `s=(x_i-x_j)^2+(y_i-y_j)^2` and `r=isqrt(s)`, it returns `r+1` exactly when `4s >= (2r+1)^2`; it uses no floating-point square roots.

The official TSPLIB `.vrp` source numbers its depot as 1 and customers as 2..1001. CVRPLIB `.sol` witnesses number customers as 1..1000. The reader maps each solution customer ID `c` to TSPLIB node ID `c+1`.

## Current public result and open status

CVRPLIB's current X-n1001-k43 bound-history page lists 72332 as BKS, submitted 2026-10-24 by Martín Vizzolini. The note says the result starts from published BKS solutions and improves them. The matching official solution file is saved and exactly rechecked. Its route count is 43 and its total demand respects capacity. The library instance table marks `Opt=no`, so 72332 is not a proved optimum. It also lists a historical 72355 solution from literature through 2025. That older witness is retained for comparison and is not called the current record.

The CVRPLib page does not report whether AI tools contributed to Vizzolini's 72332 result. We keep it as `best_public`, not as `best_human`. For a verified same-instance human-method baseline, `human.py` rebuilds the classic Clarke-Wright savings heuristic, published in 1964. This fixed deterministic construction has cost 77398. It is a weak method baseline, not a claim about the best human-only solution.

Primary sources checked 2026-11-06:

- [CVRPLIB instance listing](https://galgos.inf.puc-rio.br/cvrplib/en/cvrp/instances), row X-n1001-k43: 1000 customers, catalog route count 43, capacity 131, BKS 72332, `Opt=no`.
- [CVRPLIB bound history](https://galgos.inf.puc-rio.br/cvrplib/en/bounds/257), showing 72332 from 2026-10-24 and the older 72355 entry from 2025.
- [DIMACS CVRP rules](https://dimacs.rutgers.edu/programs/implementation-challenges/vehicle-routing/implementation-challenge-vehicle-routing/capacitated-vrp), which state route counts are unrestricted for all instances and explain TSPLIB/CVRPLIB formats.
- Uchoa et al., [New Benchmark Instances for the Capacitated Vehicle Routing Problem](https://doi.org/10.1016/j.ejor.2016.08.012), which introduced the X set.
- Clarke and Wright, [Scheduling of Vehicles from a Central Depot to a Number of Delivery Points](https://doi.org/10.1287/opre.12.4.568), Operations Research 12(4), 1964, pp. 568–581.
- Reinelt, [TSPLIB 95 specification](https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp95.pdf), §2.1, for the exact `EUC_2D` nearest-integer definition.

## Programs and limits

- `init_program.py` returns one customer on each route. Each individual demand is below 131, so this is valid without reading task files or importing task modules.
- `human.py` rebuilds deterministic parallel Clarke-Wright savings routes from the public instance. It starts with one route per customer and merges route endpoints in descending savings order when capacity allows.
- `baseline.py` runs six fixed-seed Clarke-Wright starts with randomized tie order among equal savings. It uses only the instance data, never the comparison solutions.
- With six default trials and seed 0, the search produced a 43-route solution of cost 77170. Its replayable witness and run metadata are in `best/T057-C01/`.
- `reference.py` replays the official 72332 witness. The 72355 historical witness is also saved under `data/reference/` but is not used by the reference program.
- `evaluator.py` uses the shared runner. Default limits are 300 seconds for generation, 60 seconds for verification, 4 GiB, and one thread.

Run from the repository root:

```sh
.venv/bin/python -m pytest tasks/t057/test_task.py -q
.venv/bin/python -m json.tool tasks/t057/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t057/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t057/records.json > /dev/null
```

## 定义

固定实例有仓库节点 1 和 1000 个客户。TSPLIB 输入中的客户编号为 2 到 1001。每个客户有正整数需求。每条路线从仓库出发并回到仓库，路线需求总和不超过容量 131。所有客户必须恰好出现一次。

路线数不固定，也没有上限。名称后缀 `k43` 只是实例名的一部分。官方 DIMACS 规则明确说所有实例的路线数都不受限制，并用 E-n101-k8 可以采用 9 条路线作例子。该实例总需求为 5557，容量约束要求至少 `ceil(5557/131)=43` 条路线，但可使用更多路线。

目标是最小化总路程。包括仓库连接在内，每条边 `i,j` 的成本为 TSPLIB `EUC_2D` 最近整数距离：

`d(i,j) = nint(sqrt((x_i-x_j)^2 + (y_i-y_j)^2))`。

评测器用整数精确计算。令 `s=(x_i-x_j)^2+(y_i-y_j)^2`、`r=isqrt(s)`。当且仅当 `4s >= (2r+1)^2` 时返回 `r+1`，否则返回 `r`，不使用浮点平方根。

官方 TSPLIB `.vrp` 将仓库记为 1，客户记为 2 至 1001。CVRPLIB `.sol` 文件将客户记为 1 至 1000。文件读取程序把 `.sol` 客户编号 `c` 转成 TSPLIB 节点编号 `c+1`。

## 当前公开值和开放状态

截至 2026-11-06，CVRPLIB 的 X-n1001-k43 bound history 页面将 72332 标为 BKS，提交日期为 2026-10-24，提交者 Martín Vizzolini。来源说明该结果从已发表的 BKS 解继续改进。对应官方解文件已保存并精确复算。此解有 43 条路线，且每条满足容量限制。实例表将 `Opt` 标为 `no`，因此 72332 不是已证明的最优值。页面还保留截至 2025 文献值 72355。这个历史见证仍作为对照，但不称为当前纪录。

CVRPLIB 页面没有说明 Vizzolini 是否使用 AI 工具。因此把 72332 记录为 `best_public`，不归为 `best_human`。任务使用经典 Clarke-Wright 节约值算法作为同参数人类方法基线。该方法发表于 1964 年。`human.py` 固定排序规则并从公开输入重建路线，成本为 77398。这是可复现的弱方法基线，不代表最佳纯人工结果。

上方英文列出了核查日期、主来源和实例来源。任务状态为已通过 Sol 验收（2026-11-06）。
