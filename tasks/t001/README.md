# T001：正方形中的等圆装填

给定单位正方形，放置指定数量的等半径圆，最大化共同半径。精确有理数检查器验证圆到边界的距离和所有圆心对距离。可行构造给出下界，不证明最优。

T001-C01 固定为 26 个圆。简单初始程序使用精确网格；传统搜索使用有界的 SLSQP 多起点搜索，并用精确检查器复核改进结果。人类和参考程序只读取本任务的数据副本。

来源：[Packomania 等圆记录表](https://packomania.com/csq/)。坐标来源、半径缩减和复算结果见[来源记录](data/bestknown.json)。

# T001: Equal circles in a unit square

Place the configured number of equal circles in the unit square and maximize their common radius. The exact rational checker validates all square clearances and all center pairs. A feasible construction gives a lower bound; it does not prove optimality.

T001-C01 uses 26 circles. The simple seed uses an exact grid. The traditional baseline uses bounded SLSQP multistart search and checks every improvement with exact arithmetic. Human and reference programs read local copies only.

Source: [Packomania equal-circle table](https://packomania.com/csq/). Coordinate provenance, radius reductions, attribution gaps, and reproduction results are in the [source records](data/bestknown.json).
