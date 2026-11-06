# T001：正方形中的等圆装填

给定单位正方形，放置指定数量的等半径圆，最大化共同半径。精确有理数检查器验证圆到边界的距离和所有圆心对距离。可行构造给出下界，不证明最优。

T001-C01（26圆）、C02（32圆）和C03（50圆）均通过Sol验收，并已加入正式运行清单。见 [扩展记录](EXPANSION.md)。简单初始程序使用精确网格；传统搜索使用有界的 SLSQP 多起点搜索，并用精确检查器复核改进结果。人类和参考程序只读取本任务的数据副本。

来源：[Packomania 等圆记录表](https://packomania.com/csq/)。各配置的坐标来源、半径缩减、归属缺口和复现结果见扩展记录及 [记录档案](records_expansion.json)。

# T001: Equal circles in a unit square

Place the configured number of equal circles in the unit square and maximize their common radius. The exact rational checker validates all square clearances and all center pairs. A feasible construction gives a lower bound; it does not prove optimality.

C01 (26 circles), C02 (32), and C03 (50) passed Sol review and are in the run registry. See [expansion notes](EXPANSION.md). The simple seed uses an exact grid. The traditional baseline uses bounded SLSQP multistart search and checks every improvement with exact arithmetic. Human and reference programs read local copies only.

Source: [Packomania equal-circle table](https://packomania.com/csq/). Coordinate provenance, radius reductions, attribution gaps, and reproduction results are in the [expansion notes](EXPANSION.md) and [record archive](records_expansion.json).
