> **2026-11-03修订：当前状态以[逐项核查汇总](confirmation_summary.md)为准。** 本文记录原题与任务家族的对应关系。对应关系不代表某个配置已通过选型。

# 已引用系统的任务覆盖审计

覆盖调研与纳入benchmark是两件事。这里逐项记录原任务的去向；不能说100项主表已完整包含AlphaEvolve全部数学原题。纯存在性、连续证书昂贵、已解校准和未找到同配置人类构造的项目明确保留或暂缓。

## SimpleTES 与 DREAM-RSI 数学核心

来源：[SimpleTES任务目录](https://github.com/wq-will/SimpleTES/blob/main/datasets/README.md)、[DREAM-RSI任务目录](https://github.com/google-research/dream-rsi/blob/main/tasks/README.md)。LASSO、GPU kernel等没有混入数学构造清单。

|数学任务|主表ID|原实例覆盖说明|
|---|---|---|
|AC1|T079|SimpleTES|
|AC2|T080|SimpleTES|
|AC3|T081|SimpleTES + DREAM-RSI|
|Erdős minimum overlap|T082|SimpleTES；正确固定f和g两者的支撑|
|Sum–difference I|T057|SimpleTES + DREAM-RSI；原集合大小/数值范围保持原配置|
|Circle packing sum radii|T005|SimpleTES + DREAM-RSI；n26与n32是两个配置，不是两个任务|
|Maximum determinant|T089|SimpleTES；n29是配置|

上述并集为7个任务家族、原始常见8个参数实例；这是数学定义的覆盖。原evaluator口径兼容和严格验证应分开审计，不照搬自报分数和容差漏洞。

## AlphaEvolve官方67项逐题去向

来源：[官方仓库](https://github.com/google-deepmind/alphaevolve_repository_of_problems)。本次主表对同源条目去重；这里明确部分覆盖、特例合并和暂缓原因。

|原题号|原题名|去向|备注|
|---:|---|---|---|
|1|[1. Kakeya and Nikodym sets in finite fields](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/1.html)|T056|主表先研究Kakeya，Nikodym另需完整实例化，不宣称两者均已就绪。|
|2|[2. An autocorrelation problem related to Sidon sets](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/2.html)|T079|候选定义已纳入；具体配置与human见证仍按主表审计。|
|3|[Second autocorrelation inequality](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/3.html)|T080|候选定义已纳入；具体配置与human见证仍按主表审计。|
|4|[4. An autocorrelation problem with functions that can take negative values](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/4.html)|T081|候选定义已纳入；具体配置与human见证仍按主表审计。|
|5|[5. Erdős minimum overlap problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/5.html)|T082|候选定义已纳入；具体配置与human见证仍按主表审计。|
|6|[6. An autocorrelation problem related to difference bases](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/6.html)|T083|候选定义已纳入；具体配置与human见证仍按主表审计。|
|7|[7. Difference Bases](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/7.html)|T049|候选定义已纳入；具体配置与human见证仍按主表审计。|
|8|[8. Kissing numbers](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/8.html)|储备 / 暂缓|与球面码有关联，但固定角度最大点数的原kissing任务另需配置与基线，未冒称主表Tammes已完全覆盖。|
|9|[9. Kakeya needle problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/9.html)|储备 / 暂缓|连续平面Kakeya：有限族构造的覆盖/转向证书需另定义。|
|10|[10. 3D Kakeya problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/10.html)|储备 / 暂缓|三维连续Kakeya：全方向证书成本高。|
|11|[11. Uncertainty principle](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/11.html)|T084|候选定义已纳入；具体配置与human见证仍按主表审计。|
|12|[12. Sphere Packing](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/12.html)|T090|仅格装填候选；非格周期/任意装填没有因此自动被覆盖。|
|13|[13. A Linear Programming Bound](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/13.html)|T085|候选定义已纳入；具体配置与human见证仍按主表审计。|
|14|[14. Hausdorff-Young Inequality](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/14.html)|储备 / 暂缓|Hausdorff–Young已有经典sharp Gaussian extremizer；可作校准扩展，本轮让位于开放构造。|
|15|[15. Gagliardo-Nirenberg Inequality](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/15.html)|T086|候选定义已纳入；具体配置与human见证仍按主表审计。|
|16|[16. Special Case of Gagliardo-Nirenberg Inequality](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/16.html)|T086|是GN的参数特例，不另计一个任务。|
|17|[17. Young's Convolution Inequality](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/17.html)|储备 / 暂缓|Young sharp convolution已有Gaussian人类基线；同属校准储备。|
|18|[18. Hardy-Littlewood Maximal Inequality](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/18.html)|储备 / 暂缓|Melas一维中心最大函数sharp常数已知；有限原子/阶梯可重算版本还需明确。|
|19|[19. The Ovals Problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/19.html)|T088|候选定义已纳入；具体配置与human见证仍按主表审计。|
|20|[20. Sendov's Conjecture](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/20.html)|排除，原 T091|2026年证明解决该极值问题；不再作为发现任务。见[证明综述](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)。|
|21|[21. Schmeisser's Conjecture](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/21.html)|T092|候选定义已纳入；具体配置与human见证仍按主表审计。|
|22|[22. Borcea's Conjecture](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/22.html)|T093|候选定义已纳入；具体配置与human见证仍按主表审计。|
|23|[23. Smale's Problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/23.html)|N002|研究跨次数的最优均值常数；保留经典有限多项式基线。2026年的反例推翻旧常数1猜想，最佳常数仍未知，须注明该新结果披露了AI辅助。|
|24|[24. de Bruin-Sharma Problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/24.html)|储备 / 暂缓|原始输出是二维可行区域；可以固定alpha优化beta，须公开这项任务变换及baseline。|
|25|[25. Crouzeix's Conjecture](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/25.html)|储备 / 暂缓|Crouzeix分母为numerical range上多项式的全域sup，精确认证较重。|
|26|[26. Sidorenko's Conjecture](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/26.html)|储备 / 暂缓|Sidorenko有自然homomorphism ratio，固定小H时可重算；graphon表示、基线与内层计数预算待定。|
|27|[27. The Prime Number Theorem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/27.html)|储备 / 暂缓|涉及全区间/无穷范围的素数定理界，不适合仅交有限构造的MVP。|
|28|[28. Golay's Merit Factor](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/28.html)|T073, T077, T078|主表保留L4/merit(与LABS同一任务)、sup、inf；width待补具体见证，不额外凑数。|
|29|[29. Block Stacking Problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/29.html)|储备 / 暂缓|论文是一块压一块的调和数已解任务；一般多排overhang是另一更丰富问题，不能混用经典最优值。|
|30|[30. The Arithmetic Kakeya Conjecture](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/30.html)|储备 / 暂缓|Arithmetic Kakeya是有限分布投影熵之比，有自然标量；原代理未明确这个版本，保留待单题审计。|
|31|[31. Furstenberg-Sárközy Problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/31.html)|T054|候选定义已纳入；具体配置与human见证仍按主表审计。|
|32|[32. Spherical Designs](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/32.html)|T011|候选定义已纳入；具体配置与human见证仍按主表审计。|
|33|[33. The Thomson Problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/33.html)|T010|候选定义已纳入；具体配置与human见证仍按主表审计。|
|34|[34. Tammes problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/34.html)|T009|候选定义已纳入；具体配置与human见证仍按主表审计。|
|35|[35. Packing in a dilate](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/35.html)|T001, T002, T003|不同形状列不同任务，尺寸/数量/容器为配置。|
|36|[36. Circle packing in a square / rectangle](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/36.html)|T005|原固定周长矩形扩展配置尚未固定人类见证，主轨单位正方形。|
|37|[37. The hypergraph Turán number of the tetrahedron](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/37.html)|T041|含K4^(3)为配置。|
|38|[38. Factoring $N!$ into $N$ numbers](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/38.html)|T100|候选定义已纳入；具体配置与human见证仍按主表审计。|
|39|[39. Beat the average game](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/39.html)|储备 / 暂缓|beat-the-average有概率目标；需要精确分布积分/求和版本，不以一次随机胜率排名。|
|40|[40. Erdős discrepancy problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/40.html)|T053|候选定义已纳入；具体配置与human见证仍按主表审计。|
|41|[41. Points on sphere maximizing the volume](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/41.html)|T012|候选定义已纳入；具体配置与human见证仍按主表审计。|
|42|[42. Sum-difference problem I](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/42.html)|T057|候选定义已纳入；具体配置与human见证仍按主表审计。|
|43|[43. Sum-difference problem II](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/43.html)|T058|候选定义已纳入；具体配置与human见证仍按主表审计。|
|44|[44. Sum-difference problem III](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/44.html)|T059|候选定义已纳入；具体配置与human见证仍按主表审计。|
|45|[45. Sum-product problems](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/45.html)|T055|候选定义已纳入；具体配置与human见证仍按主表审计。|
|46|[46. Minimal triangle density in graphs](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/46.html)|T043|候选定义已纳入；具体配置与human见证仍按主表审计。|
|47|[47. Matrix multiplications and AM-GM inequalities](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/47.html)|T094|候选定义已纳入；具体配置与human见证仍按主表审计。|
|48|[48. Heilbronn problem in a fixed bounding box](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/48.html)|T014|候选定义已纳入；具体配置与human见证仍按主表审计。|
|49|[49. Heilbronn problem in an arbitrary convex bounding box](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/49.html)|T013|候选定义已纳入；具体配置与human见证仍按主表审计。|
|50|[50. Max to min ratios](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/50.html)|T015|候选定义已纳入；具体配置与human见证仍按主表审计。|
|51|[51. Erdős–Gyárfás conjecture](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/51.html)|储备 / 暂缓|原问题为反例存在性；不把违反项数当正式新结果分。|
|52|[52. Erdős squarefree problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/52.html)|储备 / 暂缓|固定大小的平方自由条件构造，暂未定位有文献的优化参数及同配置human baseline。|
|53|[53. Equidistant points in convex polygons](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/53.html)|储备 / 暂缓|原陈述存在/反例性质为主；自然标量版本与人类baseline未确定。|
|54|[54. Pairwise touching cylinders](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/54.html)|储备 / 暂缓|无限柱体全局相切构造的存在性与严格空间几何验证较重。|
|55|[55. Erdős squares in a square problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/55.html)|T006|候选定义已纳入；具体配置与human见证仍按主表审计。|
|56|[56. Good asymptotic constructions of Szemerédi--Trotter](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/56.html)|储备 / 暂缓|点线关联数天然是标量；有限坐标约束与对应人类构造待固定，仍为强后备。|
|57|[57. Rudin problem for polynomials](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/57.html)|T087|候选定义已纳入；具体配置与human见证仍按主表审计。|
|58|[58. Erdős--Szekeres Happy Ending problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/58.html)|T019|明确区分一般凸k边形与empty k-gon。|
|59|[59. Subsets of the grid with no isosceles triangles](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/59.html)|储备 / 暂缓|整数格点禁等腰三角形最大基数是良好标量；本轮核到的显眼纪录含AI，纯人类见证待定位。|
|60|[60. The no 5 on a sphere problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/60.html)|储备 / 暂缓|禁5点共球/共面最大集有天然基数；需明确共面条件与历史构造数据。|
|61|[61. The Ring Loading Problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/61.html)|储备 / 暂缓|Ring loading原目标含对所有路由选择的内层最优性，须给内层证书。|
|62|[62. The moving sofa problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/62.html)|储备 / 暂缓|sofa面积可评分；完整连续路径验证较重，且已存在Baek的Gerver最优性预印本。|
|63|[63. The ambidextrous moving sofa problem](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/63.html)|储备 / 暂缓|双向sofa同样需要全路径证书，暂缓。|
|64|[64. The three-dimensional moving sofa problem with two perpendicular turns](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/64.html)|储备 / 暂缓|三维sofa连续可行性验证更重。|
|65|[65. Variant of IMO 2025, Problem 6](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/65.html)|储备 / 暂缓|IMO变体可把rectangle数量作为标量，但先作为已解校准储备，需固定原优化方向与任务约束。|
|66|[66. The function guessing game](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/66.html)|储备 / 暂缓|函数猜测交互游戏与当前有限数学构造范围不同。|
|67|[67. Logic puzzles](https://google-deepmind.github.io/alphaevolve_repository_of_problems/problems/67.html)|储备 / 暂缓|自然语言逻辑谜题生成不属于本次目标范围。|

本轮有39个官方编号映射到100项候选表（含同题特例、部分覆盖），其余28项的去向已列明；这两个数字不是独立任务计数，也不是已复现配置数量。
