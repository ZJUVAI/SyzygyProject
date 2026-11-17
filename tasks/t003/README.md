# T003: Unequal-circle packing in a unit square

## 中文

给定 32 个圆。每个圆的半径可变。所有圆必须完整位于单位正方形内，且圆的内部不能相交。目标是最大化半径总和。

正式配置为 T003-C02。输出格式为 `{"circles":[{"x":...,"y":...,"r":...}]}`，其中 `x`、`y` 是圆心坐标，`r` 是半径。校验器把整数、有限浮点数和有理数字符串精确转换为有理数。严格模式会精确验证全部墙面和两两距离约束。

公开等圆坐标见 `data/csq32.txt`。人类见证将圆心平移到单位正方形。每个半径减小 `1/10^9`，以覆盖坐标舍入误差。复算半径和为 2.811460994816。

`evolution.py` 从规则网格冷启动，不读取人类或参考见证。搜索维护多个持久链，每代为每条链生成一个候选，并对轮换的一条链运行一次有界 SLSQP，最多 20 次迭代，使用解析约束梯度。约四分之一的局部求解不带坐标扰动，用于纯局部优化。链可按退火概率接受较差候选；单独保存的全局最佳可行构造不会被替换。连续 100 次局部求解未改进全局最佳后，程序会从随机打乱的规则网格重启最弱链。停滞时扩大中心扰动到最多边长的 8%，改进后逐步缩小到至少 0.2%。程序将结果舍入到十亿分之一坐标格，再用向下取整的整数平方根和精确有理数半径修复重叠，墙面保留十个格点的安全距离。初始网格在 5 列和 6 列布局间选择，以改变接触结构。环境变量 `MATHBENCH_SEED` 固定随机种子；`MATHBENCH_EVOLUTION_GENERATIONS`（默认 12，范围 1–2000）和 `MATHBENCH_EVOLUTION_POPULATION`（默认 6，范围 4–48）控制代数和链数。每代候选槽位数等于链数，局部求解次数不超过代数。输出含算法版本、求解次数、重启数、重启修复数、向下接受数和逐代精确最佳分数，可用相同环境变量重放。精确检查只证明返回构造可行，不证明全局最优；最终结果仍须由独立评测器验证。

## English

Pack 32 circles in the unit square. The radii may vary. Each circle must stay inside the square, and circle interiors must be disjoint. Maximize the sum of the radii.

The configuration is T003-C02. Return `{"circles":[{"x":...,"y":...,"r":...}]}`, where `x` and `y` are center coordinates and `r` is the radius. The checker converts integers, finite floats, and rational strings to exact rational values. Strict mode checks every wall and pairwise distance constraint exactly.

The public equal-circle coordinates are in `data/csq32.txt`. The human witness translates the centers into the unit square and reduces each radius by `1/10^9` to cover decimal rounding. Its exact radius sum is 2.811460994816.

`evolution.py` starts from regular grids and does not read human or reference witnesses. It keeps several persistent chains. Each generation makes one proposal per chain and applies one bounded SLSQP solve to a rotating chain, with at most 20 iterations and analytic constraint gradients. About one quarter of the solves polish without a coordinate perturbation. A chain can accept a lower score with an annealed probability. A separate global incumbent preserves the best feasible construction. After 100 local solves without a new global best, the search restarts its weakest chain from a shuffled regular grid. Center perturbations grow during stagnation up to 8% of the square side and shrink after progress to a 0.2% floor. Initial grids use either five or six columns to vary contact structure. The program rounds proposals to a 1e-9 coordinate grid, then repairs overlaps with downward-rounded integer square roots and exact rational radii, with a 10-grid-unit wall margin. `MATHBENCH_SEED` fixes the random seed. `MATHBENCH_EVOLUTION_GENERATIONS` (default 12, range 1–2000) and `MATHBENCH_EVOLUTION_POPULATION` (default 6, range 4–48) set generations and chain count. Candidate slots per generation equal the chain count. The number of local solves does not exceed the generation count. Output metadata records the algorithm version, solver calls, restarts and their extra repair count, downhill accepts, and the best exact score by generation. Replay with the same environment values. Exact checks establish feasibility; they do not prove global optimality. The independent evaluator must still verify the final construction.
