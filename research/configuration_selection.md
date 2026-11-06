# 首批20个任务的配置选型

核查与验收日期：2026-11-04。

**10类、20个任务、35个配置已实现并通过Sol验收。每题1–3个，均不超过5个。**

本轮由7个独立Luna任务代理实现14个新增配置。Sol逐配置运行四类程序，复算关键量，检查破坏样例、声明分数和冷启动导出。初始21个配置保留。完整模型对比实验尚未开展。

规范见[AGENTS.md](../AGENTS.md)。机器清单见[configuration_selection.json](configuration_selection.json)。成绩见[验收报告](../reports/acceptance.md)及[本轮扩展报告](../reports/configuration_expansion.md)。

## 配置清单

| ID | 任务 | 配置数 | 所选参数 | 已验收/待实现 |
|---|---|---:|---|---|
| T001 | 等圆装入正方形 | 3 | {"n": 26, "container": "unit square"}；n=32；n=50 | 3/0 |
| T002 | 单位正方形装入正方形 | 3 | {"n": 26}；n=29；n=38 | 3/0 |
| T005 | 变半径圆装填 | 2 | {"n": 26, "container": "unit square", "radii": "variable"}；{"n": 32, "container": "unit square", "radii": "variable"} | 2/0 |
| T009 | Tammes 球面码 | 3 | {"n": 16, "space": "S2", "objective": "minimum pairwise angular separation in radians"}；n=17；n=19 | 3/0 |
| T014 | 正方形中的 Heilbronn 问题 | 3 | {"n": 11}；n=12；n=16 | 3/0 |
| T035 | 最小笼图 | 1 | {"degree": 4, "girth": 10} | 1/0 |
| T044 | 最短 Golomb ruler | 3 | {"marks": 29}；30个刻度；32个刻度 | 3/0 |
| T060 | 覆盖设计 | 1 | {"v": 24, "k": 14, "t": 4} | 1/0 |
| T066 | 线性码最小距离 | 1 | {"n": 68, "k": 15, "q": 2} | 1/0 |
| T067 | 二元码最大规模 | 1 | {"n": 17, "distance": 6} | 1/0 |
| N001 | 奇环强积独立集 | 1 | {"q": 7, "power": 5} | 1/0 |
| T057 | 和差问题 I | 1 | {"max_cardinality": 512, "integer_interval": [-1000000, 1000000]} | 1/0 |
| T073 | 低自相关二元序列（LABS） | 3 | {"L": 100}；L=80；L=120 | 3/0 |
| T079 | 自卷积不等式 AC1 | 1 | {"steps": 208, "support": ["-1/4", "1/4"], "nonnegative": true} | 1/0 |
| T080 | 自卷积不等式 AC2 | 1 | {"steps": 20, "support": ["-1/4", "1/4"], "nonnegative": true} | 1/0 |
| T081 | 允许负值的自卷积 AC3 | 1 | {"steps": 208, "support": ["-1/4", "1/4"], "signed_values_allowed": true, "integral": 1} | 1/0 |
| T082 | Erdős 最小重叠 | 1 | {"steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1} | 1/0 |
| T089 | 符号矩阵最大行列式 | 1 | {"n": 29, "entries": "±1"} | 1/0 |
| T099 | 窄可容许素数元组 | 1 | {"k": 343} | 1/0 |
| T097 | 最短加法链 | 3 | {"target": "2^192-2^64-3"}；目标2^221−5；目标2^521−3 | 3/0 |

## 选择规则

- 每题选1–5个配置。参数、结构和验证成本决定数量。随机种子与重复运行不另算配置。
- 每个配置有一个标量数学目标、固定方向和已复算的人类构造对照。人类对照可以弱于公开纪录。
- 已证最优的配置排除。新发现的证明须记录退役原因，旧ID不复用。
- 来源中的纪录值与实际构造成绩分开。精确值或保守认证值用于正式评分。
- 配置参数公开。逐配置搜索和统一程序跨配置评测分开报告。
- 汇总先在任务内进行，再对任务等权。具体公式尚未冻结，当前只报告逐配置成绩。

## 任务说明与证据

### T001 等圆装入正方形

26、32、50个圆覆盖三个规模；32圆可复用已保存的等圆对照资产。避免只取相邻数量。

**T001-C01：已通过Sol验收。** 参数 `{"n": 26, "container": "unit square"}`。

- 已复算人类对照：`96362339/1000000000`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t001/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T001/T001-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://packomania.com/csq/csq26.html)；[来源2](https://packomania.com/csq/)；[来源3](https://packomania.com/csq/txt/csq26.txt)。

**T001-C02：已通过Sol验收。** 参数 `{"n": 32, "container": "unit square"}`。

- 已复算人类对照：`10982269511/125000000000`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t001/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T001/T001-C02/human/solution.json)。
- 开放状态证据：来源以最佳已知构造列出。表格用粗体表示已证最优；发布前须保存该行原始标记并再次核查。
- 主来源：[来源1](https://packomania.com/csq/)；[来源2](https://packomania.com/csq/csq32.html)。

**T001-C03：已通过Sol验收。** 参数 `{"n": 50, "container": "unit square"}`。

- 已复算人类对照：`14275420753/200000000000`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t001/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T001/T001-C03/human/solution.json)。
- 开放状态证据：最佳已知表包含该实例；未发现最优性证明。原始粗体标记与作者归属尚须归档。
- 主来源：[来源1](https://packomania.com/csq/)；[来源2](https://packomania.com/csq/csq50.html)。

### T002 单位正方形装入正方形

26、29、38个正方形覆盖不同构造；17个配置因公开最优性证明及重建记录退役。38个采用Göbel公开斜带构造。

**T002-C01：已通过Sol验收。** 参数 `{"n": 26}`。

- 已复算人类对照：`7/2+3/2*sqrt2`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t002/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T002/T002-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://erich-friedman.github.io/papers/squares/squares.html)；[来源2](https://squaremath.org/cases/26.html)。

**T002-C03：已通过Sol验收。** 参数 `{"n": 29}`。

- 已复算人类对照：`2966942899906512939318226046481160904289990651293931822604648091421/500000000000000000000000000000000000000000000000000000000000000000`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t002/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T002/T002-C03/human/solution.json)。
- 开放状态证据：当前实例页明确标记open，并分别给上下界。
- 主来源：[来源1](https://erich-friedman.github.io/papers/squares/squares.html)；[来源2](https://squaremath.org/cases/29.html)；[来源3](https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record)。

**T002-C04：已通过Sol验收。** 参数 `{"n": 38}`。

- 已复算人类对照：`6+1/2*sqrt2`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t002/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T002/T002-C04/human/solution.json)。
- 开放状态证据：当前38点实例页明确标记open，所列上下界有差距。
- 主来源：[来源1](https://erich-friedman.github.io/papers/squares/squares.html)；[来源2](https://squaremath.org/cases/38.html)。

### T005 变半径圆装填

保留26和32两个已验收配置。先补强变半径公开纪录见证，不再扩数量。

**T005-C01：已通过Sol验收。** 参数 `{"n": 26, "container": "unit square", "radii": "variable"}`。

- 已复算人类对照：`125271039413/50000000000`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t005/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T005/T005-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://packomania.com/csq/txt/csq26.txt)；[来源2](https://www.packomania.com/csqv/csqv.html)。

**T005-C02：已通过Sol验收。** 参数 `{"n": 32, "container": "unit square", "radii": "variable"}`。

- 已复算人类对照：`10982269511/3906250000`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t005/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T005/T005-C02/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://packomania.com/csq/txt/csq26.txt)；[来源2](https://www.packomania.com/csqv/csqv.html)。

### T009 Tammes 球面码

16、17、19点均有传统文献与坐标。15点及24点带最优性证明标记，排除。

**T009-C02：已通过Sol验收。** 参数 `{"n": 16, "space": "S2", "objective": "minimum pairwise angular separation in radians"}`。

- 已复算人类对照：`0.9118367215999161`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t009/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T009/T009-C02/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://spherical-codes.org/)。

**T009-C03：已通过Sol验收。** 参数 `{"n": 17, "space": "S2", "objective": "minimum pairwise angular separation in radians"}`。

- 已复算人类对照：`0.8916944491515696`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t009/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T009/T009-C03/human/solution.json)。
- 开放状态证据：表中3维17点未带最优标记*；这是来源证据，不构成穷尽全部证明的声明。
- 主来源：[来源1](https://spherical-codes.org/)；[来源2](https://doi.org/10.1016/0012-365X(86)90002-6)；[来源3](https://spherical-codes.org/data/3/17)。

**T009-C04：已通过Sol验收。** 参数 `{"n": 19, "space": "S2", "objective": "minimum pairwise angular separation in radians"}`。

- 已复算人类对照：`0.8323809277763071`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t009/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T009/T009-C04/human/solution.json)。
- 开放状态证据：表中3维19点未带最优标记*；发布前再次核查。
- 主来源：[来源1](https://spherical-codes.org/)；[来源2](https://spherical-codes.org/data/3/19)。

### T014 正方形中的 Heilbronn 问题

11、12、16点有不同公开构造，三角形枚举仍很小。不选已证最优的小规模。

**T014-C01：已通过Sol验收。** 参数 `{"n": 11}`。

- 已复算人类对照：`1/27`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t014/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T014/T014-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://math.tejstead.com/heilbronn/square/11/points.txt)。

**T014-C02：已通过Sol验收。** 参数 `{"n": 12}`。

- 已复算人类对照：`101871433411936556933637520697548102056943915772631725289/3125000000000000000000000000000000000000000000000000000000`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t014/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T014/T014-C02/human/solution.json)。
- 开放状态证据：来源将n≥11列为最佳已知构造，未宣称最优。
- 主来源：[来源1](https://math.tejstead.com/heilbronn/square/)；[来源2](https://math.tejstead.com/heilbronn/square/12/points.txt)。

**T014-C03：已通过Sol验收。** 参数 `{"n": 16}`。

- 已复算人类对照：`7/341`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t014/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T014/T014-C03/human/solution.json)。
- 开放状态证据：来源将该实例标记为record，未宣称最优。
- 主来源：[来源1](https://math.tejstead.com/heilbronn/square/)；[来源2](https://math.tejstead.com/heilbronn/square/16/points.txt)。

### T035 最小笼图

保留(4,10)。初始图已较大，先改善起点和搜索；其他参数须另查开放性与见证。

**T035-C01：已通过Sol验收。** 参数 `{"degree": 4, "girth": 10}`。

- 已复算人类对照：`320`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t035/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T035/T035-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/abs/2511.07247v2)；[来源2](https://houseofgraphs.org/meta-directory/cages)；[来源3](https://github.com/AGT-Kulak/smallRegGirthGraphs/blob/main/genLifts/data/graphs/cage/n320_k4_g10.g6)。

### T044 最短 Golomb ruler

29、30、32刻度具有公开代数构造，可精确验证。避免已证最优的较小刻度数。

**T044-C01：已通过Sol验收。** 参数 `{"marks": 29}`。

- 已复算人类对照：`623`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t044/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T044/T044-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://cube20.org/golomb/)。

**T044-C02：已通过Sol验收。** 参数 `{"marks": 30}`。

- 已复算人类对照：`680`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t044/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T044/T044-C02/human/solution.json)。
- 开放状态证据：来源将较大规模称为possibly optimal，未提供30刻度的全局最优证明。旧页面的OGR-28进度已过时，不用作当前证明状态。
- 主来源：[来源1](https://cube20.org/golomb/)。

**T044-C03：已通过Sol验收。** 参数 `{"marks": 32}`。

- 已复算人类对照：`784`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t044/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T044/T044-C03/human/solution.json)。
- 开放状态证据：来源未对32刻度证明最优；发布前核对最新证明状态。
- 主来源：[来源1](https://cube20.org/golomb/)。

### T060 覆盖设计

仅C(24,14,4)。先取得更强的23块公开构造，再考虑增加配置。

**T060-C01：已通过Sol验收。** 参数 `{"v": 24, "k": 14, "t": 4}`。

- 已复算人类对照：`62`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t060/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T060/T060-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/html/math/9502238)；[来源2](https://ljcr.dmgordon.org/cover.html)。

### T066 线性码最小距离

仅二元[68,15]。先取得距离24矩阵；维数改变会使最小距离验证呈指数增长。

**T066-C01：已通过Sol验收。** 参数 `{"n": 68, "k": 15, "q": 2}`。

- 已复算人类对照：`8`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t066/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T066/T066-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2)；[来源2](https://ocw.mit.edu/courses/6-451-principles-of-digital-communication-ii-spring-2005/bb895c1dee9ce0b39d6846e0aa984981_MIT6_451S05_FullLecNotes.pdf)。

### T067 二元码最大规模

仅A(17,6)。先取得258码字见证，不再增加尚未复现的纪录缺口。

**T067-C01：已通过Sol验收。** 参数 `{"n": 17, "distance": 6}`。

- 已复算人类对照：`128`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t067/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T067/T067-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://aeb.win.tue.nl/codes/binary-1.html)；[来源2](https://www.encyclopediaofmath.org/wiki/BCH_code)。

### N001 奇环强积独立集

仅C7强积5次。367点构造来源清楚；其他幂可能已解决或大幅增加搜索成本。

**N001-C01：已通过Sol验收。** 参数 `{"q": 7, "power": 5}`。

- 已复算人类对照：`367`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/n001/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/N001/N001-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/abs/1808.07438)。

### T057 和差问题 I

保持集合大小上限512和整数范围。任意改上限可能只转移同一个见证，未必增加结构差异。

**T057-C01：已通过Sol验收。** 参数 `{"max_cardinality": 512, "integer_interval": [-1000000, 1000000]}`。

- 已复算人类对照：`1.059793094547245377600002106026027810995517075670792756303442005379263930059059337409`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t057/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T057/T057-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/abs/math/0608131)。

### T073 低自相关二元序列（LABS）

80、100、120项有可展开的公开序列，覆盖规模变化，精确验证为二次成本。

**T073-C01：已通过Sol验收。** 参数 `{"L": 100}`。

- 已复算人类对照：`578`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t073/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T073/T073-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm)；[来源2](https://militzer.berkeley.edu/sequences.html)。

**T073-C02：已通过Sol验收。** 参数 `{"L": 80}`。

- 已复算人类对照：`352`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t073/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T073/T073-C02/human/solution.json)。
- 开放状态证据：来源将80标*，说明该记录未通过穷举确定最优。旧表的状态须在发布前更新。
- 主来源：[来源1](https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm)。

**T073-C03：已通过Sol验收。** 参数 `{"L": 120}`。

- 已复算人类对照：`872`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t073/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T073/T073-C03/human/solution.json)。
- 开放状态证据：来源将120标*，未声称全局最优。
- 主来源：[来源1](https://www2.chemistry.msu.edu/faculty/dantus/merit_factor_records.htm)。

### T079 自卷积不等式 AC1

仅208分段。加倍网格可以复制同一函数，不能据此虚增独立数学实例。

**T079-C01：已通过Sol验收。** 参数 `{"steps": 208, "support": ["-1/4", "1/4"], "nonnegative": true}`。

- 已复算人类对照：`6280435861361744576/4160000022692211721`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t079/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T079/T079-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/abs/0907.1379)。

### T080 自卷积不等式 AC2

仅20分段。其他网格的文献成绩不可直接混用，先保持同参数可比。

**T080-C01：已通过Sol验收。** 参数 `{"steps": 20, "support": ["-1/4", "1/4"], "nonnegative": true}`。

- 已复算人类对照：`108065664771600646574507764702/121527759800529249872686490775`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t080/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T080/T080-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/pdf/0907.1379)；[来源2](https://arxiv.org/abs/2604.19341)。

### T081 允许负值的自卷积 AC3

仅208分段。先补强真正有符号的人类对照，不将不同网格或正峰值问题混入。

**T081-C02：已通过Sol验收。** 参数 `{"steps": 208, "support": ["-1/4", "1/4"], "signed_values_allowed": true, "integral": 1}`。

- 已复算人类对照：`6280435861361744576/4160000022692211721`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t081/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T081/T081-C02/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/abs/0907.1379)。

### T082 Erdős 最小重叠

仅51分段。该人类构造与参数对应明确，优先保持严格全域验证。

**T082-C01：已通过Sol验收。** 参数 `{"steps": 51, "support": "[0,2]", "range": "0≤f≤1", "integral": 1}`。

- 已复算人类对照：`64757565083624785688821235069923/170000000000000000000000000000000`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t082/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T082/T082-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/abs/1609.08000)。

### T089 符号矩阵最大行列式

仅29阶。许多其他阶数已达到已证上界；未逐项核实前不扩张。

**T089-C01：已通过Sol验收。** 参数 `{"n": 29, "entries": "±1"}`。

- 已复算人类对照：`1188957517256767569920`。方向：`maximize`。
- 纪录与来源：[任务档案](../tasks/t089/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T089/T089-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://arxiv.org/abs/math/0304410)；[来源2](https://maths-people.anu.edu.au/~brent/maxdet/order29/)。

### T099 窄可容许素数元组

仅343元组。有完整公开见证；新增规模须逐一核对是否已证明最优。

**T099-C01：已通过Sol验收。** 参数 `{"k": 343}`。

- 已复算人类对照：`2340`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t099/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T099/T099-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://mathbases.org/d/narrow-admissible-tuples)；[来源2](https://math.mit.edu/~primegaps/tuples/admissible_343_2340.txt)。

### T097 最短加法链

三个明确大整数覆盖192、221、521位；公开链可精确逐步验证，避免已解小目标。

**T097-C01：已通过Sol验收。** 参数 `{"target": "2^192-2^64-3"}`。

- 已复算人类对照：`202`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t097/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T097/T097-C01/human/solution.json)。
- 开放状态证据：沿用首批配置级研究记录与Sol验收；发布前仍须核对最新最优性证明。
- 主来源：[来源1](https://additionchains.com/LargeChains.html)。

**T097-C02：已通过Sol验收。** 参数 `{"target": "2^221-5"}`。

- 已复算人类对照：`230`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t097/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T097/T097-C02/human/solution.json)。
- 开放状态证据：表中链长上界与small-step下界有差距，未给最优性证明。
- 主来源：[来源1](https://additionchains.com/LargeChains.html)。

**T097-C03：已通过Sol验收。** 参数 `{"target": "2^521-3"}`。

- 已复算人类对照：`532`。方向：`minimize`。
- 纪录与来源：[任务档案](../tasks/t097/records.json)。
- 保存构造：[human/solution.json](../reports/witnesses/T097/T097-C03/human/solution.json)。
- 开放状态证据：表列small-step下界10及所供链12，未给最优性证明。
- 主来源：[来源1](https://additionchains.com/LargeChains.html)。

## 本轮配置修订与限制

T002-C02（17个正方形）退役。[Lean证明仓库](https://github.com/ofitzharding/sq17-lean)报告全源重建通过及全局最优性。本项目未完整重放该证明，按发现轨规则保守排除。T002-C04（38个）替换该配置，保留历史记录，不复用C02。

T002的29个正方形对照改用Schadt的2025年传统模拟退火构造，经后续有理化得到精确见证。早期Gensane–Ryckelynck构造仍作来源历史。当前公开最好值比本项目复现值更小。

等圆对照半径作保守缩小。Heilbronn的12点构造按公开十进制坐标作有理数解释。LABS采用可重建的历史人类搜索结果，未声称刷新纪录。详细来源和差异见各任务档案。

T005、T060、T066、T067、T081的公开纪录见证仍有补强空间；现有可验证的人类对照已单独列明。
