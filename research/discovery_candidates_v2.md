> 当前状态和首批建议见 [逐项核查汇总](confirmation_summary.md)。本文保留原候选池；候选数不代表已确认数。

# 仅发现轨：任务选型修订 v2

110是候选池，不是110项均已证实开放且human baseline复现完毕；15是配置研究记录，不是发布配置数。首批20项需由配置审计重选。

本轮从旧100项整题删除3项，并补充13个不同任务家族，形成110个候选。所有已解校准配置均不再准入；未锁定开放参数的家族保留在研究池，不算正式benchmark。公开上下界有差距也不保证现纪录可以突破。

## 整题删除

- **T018**：最大无空凸六边形点集=29；h(6)=30已在2024证明并形式验证。旧表误将精确30归于Gerken/Nicolas；两人2006证明的是存在有限阈值。 来源：[1](https://arxiv.org/abs/2403.00737)、[2](https://arxiv.org/abs/2403.17370)
- **T050**：当前定义为有限阿贝尔群；Green–Ruzsa已确定每个有限阿贝尔群的最大sum-free子集大小。 来源：[1](https://arxiv.org/abs/math/0307142)
- **T091**：2026年Sendov证明使当前标量C(n)=1；z^n−1已取等号。该定义下所有次数无纪录提升空间。 来源：[1](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)、[2](https://github.com/teorth/sendov)

## 删除的配置组

|任务|配置|原因|
|---|---|---|
|T044|Golomb标记数m<=28，包括上一版m=10,12|已证明最优，排除。m>28仅作替代候选，需逐项定位现纪录。|
|T073|LABS能量长度N<=66，包括上一版N=66,E=257|Packebusch–Mertens给出精确最优结果；排除。更大长度是否近期已解另查。|
|T009|Tammes球面S²点数N=8、12|已证明最优；排除。|
|T060|C(8,4,3)=14，C(10,4,3)=30|Steiner四元系达到计数下界；排除，不能把构造库所有行都当未解。|
|T066|二元[23,12,7] Golay码，[15,7,5] BCH码|这些参数最优最小距离已确定；排除。|
|T014|上一版Heilbronn正方形n=7、8|已知最优，排除。较新n=9状态需核查，不自动当open。|
|T090/T085|维数8、24的最优球装填/匹配Cohn–Elkies上界|E8、Leech格已达最优；排除这些配置。|
|T075/T076|奇素数p≡3 mod4的Legendre周期序列已达到能量p−1或PSL=1的情形|匹配奇长度非零周期自相关绝对值至少1的下界；排除这些配置。|
|T099|MIT表k<=342标为optimal的配置，特别上一版k=50和100|公开数据JS的comments明确optimal；不能把已重算见证当作待突破纪录。未标optimal的行另查开放状态。|
|T032|order=21, primitive side=112|唯一最小阶简单完美平方分割；移除这一配置，order55另审。|
|T038|n=30,F={C4}边85；n=30,F={C3,C4}边76|Afzaly–McKay对应项标为精确极值，并非仅构造下界；移除这些小配置。|
|T084|正号sign uncertainty维数12的已知sharp配置|已达精确常数；不能把另一符号、不同维数或不同平方约定的值混用。|

## 有具体参数的优先复核记录

以下不是已发布的配置。每一行仍要保存原始见证、核对最新纪录并独立重算；最新纪录与历史人类基线分列。

|任务|配置|标量|人类基线|开放证据与缺口|
|---|---|---|---|---|
|T001|{"n": 26, "container": "unit square"}|common radius ↑|Nurmela–Östergård 1999: 0.096362339010|record row not marked proved optimal; no matching numerical upper bound frozen|
|T001|{"n": 32, "container": "unit square"}|common radius ↑|Boll et al. 2000: 0.087858157088|same caveat|
|T002|{"n": 26}|unit-square container side ↓|Friedman 1997: (7+3sqrt(2))/2 ≈5.62132034356|maintained project reports verified interval [5.545,5.62132034356]; lower proof replay not repeated here|
|T014|{"n": 11, "domain": "unit square"}|minimum triangle area ↑|Goldberg 1972: 1/27|record construction; unrestricted optimum not established by checked page|
|T014|{"n": 12, "domain": "unit square"}|minimum triangle area ↑|Comellas–Yebra 2001: 0.0325988586918196…|record construction; unrestricted optimum not established by checked page|
|T029|{"n": 25}|number of unit-distance pairs ↑|Engel et al. human construction:72|agent reports current interval72–73; current certificate ledger needs root replay and provenance freeze|
|T032|{"order": 55}|primitive outer side ↓|Bernard Moss 2020:740|smallest known, not proved minimum; Bouwkamp file located not replayed|
|T035|{"degree": 4, "girth": 10}|vertex count ↓|Exoo et al. 2025/2026:320|paper interval243–320; obtain320-vertex graph before admitting|
|T060|{"v": 24, "k": 14, "t": 4}|block count ↓|historical covering repository construction:23; contributor/blocklist pending|2026 Lean project reports20–23; lower proof AI-assisted; root read source but did not replay|
|T060|{"v": 25, "k": 15, "t": 5}|block count ↓|historical upper bound42; blocklist pending|same project reports34–42; human witness provenance pending|
|T066|{"n": 68, "k": 15, "q": 2}|minimum Hamming distance ↑|Grassl construction [68,15,24]|root read table24–26; explicit construction chain exists, generator not reconstructed|
|T067|{"n": 17, "distance": 6}|number of codewords ↑|Milshtein 2019:258|root read Brouwer258–340; archive codeword list and newer-record search pending|
|T089|{"n": 29}|absolute determinant ↑|Orrick et al.:2^28·7^12·320|Brent conjectures optimality; historicalupper329·7^12·2^28; high risk incumbent already optimal|
|N001|{"q": 7, "power": 5}|number of independent words ↑|Polak–Schrijver 2018/2019:367|published367–401;2026 capacity gains at other powers do not close this configuration|
|N010|{"chromatic_number": 4, "girth_at_least": 6}|vertex count ↓|Exoo–Goedgebeur 2019:66|2026 paper29–64; latest64 provenance must be separately recorded; non3-colourability requires certificate|

## 新增13个家族

### N001 Shannon capacity: independent sets in strong powers of odd cycles

- 标量：number of independent words（maximize）。
- 人类基线：Polak–Schrijver (2018/2019)给出367词，原论文附录显式列出；不是2026全局Shannon容量现纪录。
- 状态：2018论文的367是人类基线；2026容量改进来自第10/200/500幂，不可移作第五幂分数。没有全局证明367非最优，gap不保证368存在。
- 来源：[1](https://arxiv.org/abs/1808.07438)、[2](https://arxiv.org/html/1808.07438)、[3](https://arxiv.org/html/2607.21517v1)、[4](https://arxiv.org/abs/2608.30273)

### N002 Smale mean value extremal constant

- 标量：min_{p′(ζ)=0} |p(ζ)−p(a)|/(|p′(a)| |ζ−a|)（maximize）。
- 人类基线：经典p(z)=z^n−z,a=0达到1−1/n；Smale猜想其最优。2026年Tao讨论Sendov后仍列该问题及现有上界。
- 状态：经典极难且现baseline被猜测已最优。没有证据说明能突破；仅补充研究池，不列MVP；具体未解次数未锁定。
- 来源：[1](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)

### N003 Spherical cap covering / minimizing covering radius

- 标量：minimize maximum angular distance from any sphere point to its nearest selected center（minimize）。
- 人类基线：[{"dimension": 3, "n": 26, "human_baseline": "Hardin, Sloane and Smith (1994), covering radius 25.8449223 degrees"}, {"dimension": 3, "n": 27, "human_baseline": "Hardin, Sloane and Smith (1994), covering radius 25.2509549 degrees"}]
- 状态：Maintained source calls entries putatively optimal, not proved globally optimal; exact optimum remains unverified/open.
- 来源：[1](https://neilsloane.com/coverings/index.html)、[2](https://cohn.mit.edu/sloane/)

### N004 Lattice sphere covering density

- 标量：minimize covering density among lattice coverings of R^d by congruent Euclidean balls（minimize）。
- 人类基线：[{"dimension": 6, "human_baseline": "Schürmann and Vallentin best-known lattice covering density 2.900024; exact optimum not known, since exact lattice covering values are reported through dimension 5"}]
- 状态：Dimension 6 is explicitly unresolved; source table provides an incumbent. A rigorous lower bound/gap and exact generator matrix were not checked here.
- 来源：[1](https://app.icerm.brown.edu/materials/Slides/sp-s18-w3/Lattice_Coverings_%5D_Mathieu_Dutour_Sikiric%2C_Institut_Rudjer_Boskovic.pdf)、[2](https://arxiv.org/abs/2508.06446)

### N005 Lattice quantizer normalized second moment

- 标量：minimize normalized second moment G = (1/(d Vol(V)^(1+2/d))) integral_V ||x||^2 dx over full-rank d-dimensional lattices and their Voronoi cells（minimize）。
- 人类基线：[{"dimension": 13, "human_baseline": "Agrell and Allen (2023), K12 tensor Z product lattice NSM 0.071034583; previous reported record 0.074873919; conjectured lower bound 0.068721956"}, {"dimension": 14, "human_baseline": "Agrell and Allen (2023), K12 tensor A2 product lattice NSM 0.071455542; conjectured lower bound 0.068308096"}]
- 状态：Paper says optimality proofs only known through d=3. Lower bounds in table are conjectural, not certificates; incumbent lattice constructions and numerical NSM values are explicit.
- 来源：[1](https://arxiv.org/abs/2202.09605)

### N006 Exact tensor rank of 3x3 matrix multiplication over Q

- 标量：number r of rank-one terms in the submitted exact decomposition（minimize）。
- 人类基线：{"status": "historical human construction plus later AI-assisted formal lower bound", "value": "Laderman 1976 gives rank ≤23 over every field; Bläser 2003 classical human lower bound ≥19. A 2026 Lean formalization by Andrey Ivanov, explicitly disclosing substantial ChatGPT/Codex assistance, reports ≥21 over every field; this lower-bound proof has not yet been independently re-audited by the parent reviewer. Current reported Q interval [21,23]. Tomar 2026 proves rank 23 over F2 and integer-coefficient algorithms, but not rank 23 over Q."}
- 状态：Natural scalar and reported [21,23] Q interval, but the all-fields lower bound remains conditional on proof audit.
- 来源：[1](https://www.ams.org/journals/bull/1976-82-01/S0002-9904-1976-13988-2/S0002-9904-1976-13988-2.pdf)、[2](https://doi.org/10.1016/S0885-064X(02)00007-9)、[3](https://github.com/AIV5/mmrank21)、[4](https://arxiv.org/abs/2610.11823)

### N007 Border rank of 3x3 matrix multiplication over C

- 标量：number r of terms in the submitted valid algebraic degeneration（minimize）。
- 人类基线：{"status": "historical human bounds", "value": "Conner, Harper & Landsberg (2019) lower bound 17; Smirnov construction gives upper bound 20 (the upper bound is explicitly cited in Landsberg–Ottaviani 2015). Current sourced interval [17,20]."}
- 状态：Distinct natural scalar from exact rank; existing human interval and constructions.
- 来源：[1](https://theoryofcomputing.org/articles/v011a011/v011a011.pdf)、[2](https://arxiv.org/abs/1911.07981)

### N008 Addition count for rank-23 3x3 matrix multiplication schemes

- 标量：number of scalar additions/subtractions（minimize）。
- 人类基线：{"status": "historical published schemes; AI provenance unknown unless explicitly disclosed", "value": "Nielsen 2026 reports 52 additions with Karstadt–Schwartz-style basis change (AI provenance undisclosed); Stapleton–Perminov report a 51-addition alternative-basis kernel plus five conversion additions =56 ordinary coordinates. Sidebottom 2026 reports 55 without basis change via human-directed AI-assisted search. Sun 2026 had 56. Sun cites older 60→59→58 progression. Scores use distinct basis/count conventions."}
- 状态：Natural scalar and exact published schemes, but score convention and human/AI provenance must be separated.
- 来源：[1](https://arxiv.org/abs/2609.06588)、[2](https://arxiv.org/abs/2609.32388)、[3](https://arxiv.org/abs/2610.27451)、[4](https://arxiv.org/abs/2604.27645)

### N009 Waring rank of generic 4x4 determinant

- 标量：number r of fourth-power terms in the submitted exact identity（minimize）。
- 人类基线：{"status": "historical human bounds", "value": "Derksen-Teitler 2015 lower bound 50. Johns-Teitler 2020 explicit d·d! construction gives upper bound 96 for d=4; interval [50,96]."}
- 状态：Strong natural scalar interval with exact witness verification; current-record search still needed.
- 来源：[1](https://doi.org/10.1016/j.jpaa.2015.03.001)、[2](https://arxiv.org/abs/2004.06158)

### N010 Minimum order n_6(4) of a 4-chromatic girth-at-least-6 graph

- 标量：number of vertices（minimize）。
- 人类基线：Exoo–Goedgebeur 2019给出66顶点显式见证；2026新文给64顶点见证，不能将新64说成人类baseline。
- 状态：这是确有新标量目标且与regular cage不同的开放配置；只用旧人类上界时有66-29 gap。
- 来源：[1](https://arxiv.org/abs/1901.04881)、[2](https://arxiv.org/abs/2608.23652)

### N011 Perfect hash families PHF(N;k,v,t)

- 标量：number of rows N（minimize）。
- 人类基线：Walker II and Colbourn (2007) give an explicit PHF(5;10,3,3) construction (their figure/table and online PHF tables), with tabu-search and recursive/direct constructions reported. Their article describes the tables as best-known upper bounds and notes exact PHF numbers are generally unknown.
- 状态：Named, natural scalar and explicit human instance, but current open gap and witness artifact need row-level verification before use.
- 来源：[1](https://doi.org/10.1515/jmc.2007.008)、[2](https://www.phftables.com/)、[3](https://www.degruyterbrill.com/document/doi/10.1515/JMC.2007.008/html)

### N012 d-disjunct / d-cover-free binary matrices

- 标量：number of rows (tests)（minimize）。
- 人类基线：Van den Berg, Candès, Chinn, Levin, Olcott and Sing-Long (PNAS 2013) table a 4-disjunct 64-by-400 construction, obtained by shortening a covering-design-derived code; they also table a 2-disjunct 44-by-1600 construction from a standard code. The article gives explicit constructions/references and matching table context.
- 状态：Has a natural numerical rows objective and concrete historical constructions; pending newer row-specific records and lower bounds.
- 来源：[1](https://pmc.ncbi.nlm.nih.gov/articles/PMC3725070/)、[2](https://doi.org/10.1073/pnas.1216318110)、[3](https://arxiv.org/abs/1507.07368)

### N013 Global postage-stamp problem / extremal additive h-basis

- 标量：largest R such that all integers 0..R are sums of at most h submitted denominations（maximize）。
- 人类基线：Kohonen (2015), arXiv:1503.03416, states unrestricted n_2(k) is known only through k=24; Sloane's OEIS A001212 records n_2(24)=212 and authorship/history. Kohonen separately enumerates all extremal restricted bases through k=47, with n*_2(47)=734 and explicit bases. Do not treat 734 as a baseline for unrestricted n_2(47). The GStamps public library (Colisson Palais, Dumas, Galan, Grenet, Maignan, Roche; 2026) implements local/global search and basis construction but this audit did not extract a verified best unrestricted k=25 witness/value from its benchmark files.
- 状态：A well-defined open named optimization problem and public human computation record; k=25 is the natural next general configuration, but freeze only after extracting a specific current human basis and numeric range from a primary artifact.
- 来源：[1](https://arxiv.org/abs/1503.03416)、[2](https://oeis.org/A001212)、[3](https://arxiv.org/abs/2601.21423)、[4](https://github.com/jgdumas/GStamps)

## 候选池索引（110项，不能当成110项已准入）

|ID|类别|任务|标量方向|状态|
|---|---|---|---|---|
|T001|几何装填与覆盖|Equal-circle packing in fixed containers|maximize|specific_configuration_evidence_located_not_replayed|
|T002|几何装填与覆盖|Packing unit squares in squares|minimize|specific_configuration_evidence_located_not_replayed|
|T003|几何装填与覆盖|Equilateral-triangle packing in a square|minimize|pending_open_configuration_audit|
|T004|几何装填与覆盖|Maximum polygon packing (CG:SHOP 2024)|maximize|pending_open_configuration_audit|
|T005|几何装填与覆盖|Unequal-circle packing: maximum sum of radii|maximize|pending_open_configuration_audit|
|T006|几何装填与覆盖|Erdős unequal squares: maximum total side length|maximize|pending_open_configuration_audit|
|T007|几何装填与覆盖|Circles covering circles|maximize|pending_open_configuration_audit|
|T008|几何装填与覆盖|Covering a square with unit squares|maximize|pending_open_configuration_audit|
|T009|球面与极值点集|Tammes problem / spherical codes|maximize|pending_open_configuration_audit|
|T010|球面与极值点集|Riesz energy minimization on the sphere (Thomson at s=1)|minimize|pending_open_configuration_audit|
|T011|球面与极值点集|Minimum-size spherical t-design|minimize|pending_open_configuration_audit|
|T012|球面与极值点集|Maximum-volume polytope with N vertices on a sphere|maximize|pending_open_configuration_audit|
|T013|球面与极值点集|Heilbronn problem for a free convex region|maximize|pending_open_configuration_audit|
|T014|球面与极值点集|Heilbronn triangle problem in a square|maximize|specific_configuration_evidence_located_not_replayed|
|T015|球面与极值点集|Minimum maximum-to-minimum pair-distance ratio|minimize|pending_open_configuration_audit|
|T016|球面与极值点集|Largest small n-gon|maximize|pending_open_configuration_audit|
|T017|球面与极值点集|Erdős minimum distinct-distance problem|minimize|pending_open_configuration_audit|
|T019|球面与极值点集|Erdős–Szekeres happy-ending number f(k)|maximize|pending_open_configuration_audit|
|T020|几何图与计算几何|Minimum-dilation triangulation|minimize|pending_open_configuration_audit|
|T021|几何图与计算几何|Minimum-weight triangulation|minimize|pending_open_configuration_audit|
|T022|几何图与计算几何|Minimum convex partition of a point set|minimize|pending_open_configuration_audit|
|T023|几何图与计算几何|Minimum coverage by convex polygons (CG:SHOP 2023)|minimize|pending_open_configuration_audit|
|T024|几何图与计算几何|Minimum partition into plane subgraphs (CG:SHOP 2022)|minimize|pending_open_configuration_audit|
|T025|几何图与计算几何|Minimum non-obtuse triangulation (CG:SHOP 2025)|minimize|pending_open_configuration_audit|
|T026|几何图与计算几何|Minimum-area simple polygonalization|minimize|pending_open_configuration_audit|
|T027|几何图与计算几何|Maximum-area simple polygonalization|maximize|pending_open_configuration_audit|
|T028|几何图与计算几何|Rectilinear crossing number of K_n|minimize|pending_open_configuration_audit|
|T029|几何图与计算几何|Erdős maximum unit distances for n planar points|maximize|specific_configuration_evidence_located_not_replayed|
|T030|几何图与计算几何|Orchard planting / maximum 3-rich lines|maximize|pending_open_configuration_audit|
|T031|几何图与计算几何|No-three-in-line maximum on an n×n grid|maximize|pending_open_configuration_audit|
|T032|铺砌与分割|Simple perfect squared squares: minimum primitive side at fixed order|minimize|specific_configuration_evidence_located_not_replayed|
|T033|铺砌与分割|Mrs. Perkins’s quilt|minimize|pending_open_configuration_audit|
|T034|铺砌与分割|Klarner order of a polyomino|minimize|pending_open_configuration_audit|
|T035|极值图与超图|(d,g)-cage order|minimize|specific_configuration_evidence_located_not_replayed|
|T036|极值图与超图|Degree–diameter problem|maximize|pending_open_configuration_audit|
|T037|极值图与超图|Zarankiewicz number Z_{s,t}(m,n)|maximize|pending_open_configuration_audit|
|T038|极值图与超图|Forbidden-subgraph extremal number ex(n,F)|maximize|pending_open_configuration_audit|
|T039|极值图与超图|Graph saturation number sat(n,F)|minimize|pending_open_configuration_audit|
|T040|极值图与超图|Classical Ramsey number lower-bound construction|maximize|pending_open_configuration_audit|
|T041|极值图与超图|Hypergraph Turán number ex_r(n,F)|maximize|pending_open_configuration_audit|
|T042|极值图与超图|Erdős–Rogers function f_{s,t}(n)|minimize|pending_open_configuration_audit|
|T043|极值图与超图|Minimum triangles at fixed edge count|minimize|pending_open_configuration_audit|
|T044|加法组合与离散构造|Optimal Golomb ruler length|minimize|pending_open_configuration_audit|
|T045|加法组合与离散构造|Minimum diameter of a B_h set of integers, h≥3|minimize|pending_open_configuration_audit|
|T046|加法组合与离散构造|Difference triangle sets|minimize|pending_open_configuration_audit|
|T047|加法组合与离散构造|Maximum cap set in F_3^n|maximize|pending_open_configuration_audit|
|T048|加法组合与离散构造|Largest 3-term-progression-free subset of [n]|maximize|pending_open_configuration_audit|
|T049|加法组合与离散构造|Minimum difference basis for [n]|minimize|pending_open_configuration_audit|
|T051|加法组合与离散构造|Schur number S(k) lower-bound coloring|maximize|pending_open_configuration_audit|
|T052|加法组合与离散构造|van der Waerden number lower-bound coloring|maximize|pending_open_configuration_audit|
|T053|加法组合与离散构造|Longest finite sequence with discrepancy at most C|maximize|pending_open_configuration_audit|
|T054|加法组合与离散构造|Largest square-difference-free subset of [N]|maximize|pending_open_configuration_audit|
|T055|加法组合与离散构造|Finite-set sum–product growth minimization|minimize|pending_open_configuration_audit|
|T056|加法组合与离散构造|Minimum finite-field Kakeya set size|minimize|pending_open_configuration_audit|
|T057|加法组合与离散构造|Sum–difference I: normalized logarithmic ratio|maximize|pending_open_configuration_audit|
|T058|加法组合与离散构造|Sum–difference II: unnormalized logarithmic ratio|maximize|pending_open_configuration_audit|
|T059|加法组合与离散构造|Sum–difference III: finite certificate for asymptotic exponent|maximize|pending_open_configuration_audit|
|T060|组合设计|Covering number C(v,k,t)|minimize|specific_configuration_evidence_located_not_replayed|
|T061|组合设计|Covering array CAN(t,k,v)|minimize|pending_open_configuration_audit|
|T062|组合设计|Orthogonal array minimum-run construction|minimize|pending_open_configuration_audit|
|T063|组合设计|Packing number D(v,k,t)|maximize|pending_open_configuration_audit|
|T064|组合设计|Social golfer maximum schedule length|maximize|pending_open_configuration_audit|
|T065|组合设计|Maximum number of mutually orthogonal Latin squares|maximize|pending_open_configuration_audit|
|T066|编码理论|Best minimum distance of linear codes|maximize|specific_configuration_evidence_located_not_replayed|
|T067|编码理论|Maximum size of a binary code A(n,d)|maximize|specific_configuration_evidence_located_not_replayed|
|T068|编码理论|Constant-weight code A(n,d,w)|maximize|pending_open_configuration_audit|
|T069|编码理论|Constant-dimension subspace code A_q(n,d;k)|maximize|pending_open_configuration_audit|
|T070|编码理论|Covering code size|minimize|pending_open_configuration_audit|
|T071|编码理论|Maximum permutation code size|maximize|pending_open_configuration_audit|
|T072|编码理论|Maximum deletion-correcting code size|maximize|pending_open_configuration_audit|
|T073|序列与平坦多项式|LABS minimum aperiodic autocorrelation energy|minimize|pending_open_configuration_audit|
|T074|序列与平坦多项式|LABS peak sidelobe level (PSL)|minimize|pending_open_configuration_audit|
|T075|序列与平坦多项式|Periodic binary autocorrelation energy|minimize|pending_open_configuration_audit|
|T076|序列与平坦多项式|Binary sequence maximum out-of-phase autocorrelation (periodic merit)|minimize|pending_open_configuration_audit|
|T077|序列与平坦多项式|Littlewood polynomials: minimum supremum modulus|minimize|pending_open_configuration_audit|
|T078|序列与平坦多项式|Littlewood polynomials: maximum infimum modulus|maximize|pending_open_configuration_audit|
|T079|极值分析|First Autocorrelation Inequality (AC1)|minimize|pending_open_configuration_audit|
|T080|极值分析|Second Autocorrelation Inequality (AC2)|maximize|pending_open_configuration_audit|
|T081|极值分析|Third Autocorrelation Inequality (AC3)|minimize|pending_open_configuration_audit|
|T082|极值分析|Erdős Minimum Overlap|minimize|pending_open_configuration_audit|
|T083|极值分析|Autocorrelation lower envelope for difference bases|maximize|pending_open_configuration_audit|
|T084|极值分析|Sign uncertainty principle (Fourier sign changes)|minimize|pending_open_configuration_audit|
|T085|极值分析|Cohn–Elkies linear-programming bound for sphere packing|minimize|pending_open_configuration_audit|
|T086|极值分析|General one-dimensional Gagliardo–Nirenberg sharp constant|maximize|pending_open_configuration_audit|
|T087|极值分析|Rudin spherical harmonic Lp extremizer|maximize|pending_open_configuration_audit|
|T088|极值分析|Ovals curvature Schrödinger eigenvalue|minimize|pending_open_configuration_audit|
|T089|矩阵、格与代数极值|Maximum determinant of sign matrices|maximize|specific_configuration_evidence_located_not_replayed|
|T090|矩阵、格与代数极值|Minkowski lattice packing density|maximize|pending_open_configuration_audit|
|T092|矩阵、格与代数极值|Schmeisser polynomial critical-point barycenter constant|maximize|pending_open_configuration_audit|
|T093|矩阵、格与代数极值|Borcea p-moment critical-point distance constant|maximize|pending_open_configuration_audit|
|T094|矩阵、格与代数极值|Noncommutative matrix AM–GM ratio|minimize|pending_open_configuration_audit|
|T095|矩阵、格与代数极值|Minimum Mahler measure of noncyclotomic integer polynomials|minimize|pending_open_configuration_audit|
|T096|矩阵、格与代数极值|Integer Chebyshev polynomial construction|minimize|pending_open_configuration_audit|
|T097|数论与算术构造|Shortest addition chain|minimize|pending_open_configuration_audit|
|T098|数论与算术构造|Integer complexity|minimize|pending_open_configuration_audit|
|T099|数论与算术构造|Narrow admissible prime k-tuples|minimize|pending_open_configuration_audit|
|T100|数论与算术构造|Factoring N! into N balanced factors|maximize|pending_open_configuration_audit|
|N001|极值图与超图|Shannon capacity: independent sets in strong powers of odd cycles|maximize|open_configuration_evidence|
|N002|矩阵、格与代数极值|Smale mean value extremal constant|maximize|high_risk_conjectured_optimal_pending_configuration|
|N003|球面与极值点集|Spherical cap covering / minimizing covering radius|minimize|candidate_pending_configuration_and_current_record_audit|
|N004|矩阵、格与代数极值|Lattice sphere covering density|minimize|candidate_pending_configuration_and_current_record_audit|
|N005|矩阵、格与代数极值|Lattice quantizer normalized second moment|minimize|candidate_pending_configuration_and_current_record_audit|
|N006|矩阵、格与代数极值|Exact tensor rank of 3x3 matrix multiplication over Q|minimize|candidate_pending_configuration_and_current_record_audit|
|N007|矩阵、格与代数极值|Border rank of 3x3 matrix multiplication over C|minimize|candidate_pending_configuration_and_current_record_audit|
|N008|矩阵、格与代数极值|Addition count for rank-23 3x3 matrix multiplication schemes|minimize|candidate_pending_configuration_and_current_record_audit|
|N009|矩阵、格与代数极值|Waring rank of generic 4x4 determinant|minimize|candidate_pending_configuration_and_current_record_audit|
|N010|极值图与超图|Minimum order n_6(4) of a 4-chromatic girth-at-least-6 graph|minimize|candidate_pending_configuration_and_current_record_audit|
|N011|组合设计|Perfect hash families PHF(N;k,v,t)|minimize|candidate_pending_configuration_and_current_record_audit|
|N012|组合设计|d-disjunct / d-cover-free binary matrices|minimize|candidate_pending_configuration_and_current_record_audit|
|N013|加法组合与离散构造|Global postage-stamp problem / extremal additive h-basis|maximize|candidate_pending_configuration_and_current_record_audit|

## 深入资料

- [几何开放配置审计](open_geometry_revision.md)
- [离散开放配置审计](open_discrete_revision.md)
- [代数与分析开放配置审计](open_algebra_revision.md)
- [完整CSV](discovery_candidates_v2.csv)
- [完整JSON](discovery_candidates_v2.json)

旧版含校准题的100项清单仅作历史索引；已保存在archive/v1。SimpleTES/DREAM-RSI/AlphaEvolve覆盖应与开放参数准入分开：SOTA用过的已解配置也必须删。
