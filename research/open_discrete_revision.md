# 离散候选开放实例修订

日期：2026-11-03。范围：主表 T035–T078；只保留“自然数值目标 + 已发表/公开人类见证 + 当前仍有定量纪录差距”的实例建议。数值是可行见证上界/下界，不把可行解说成最优。公开记录可能在本轮之后变化，应冻结资料快照。

## 现有任务中仍可考虑的配置

| 任务 | 可考虑的具体配置和当前证据 | 结论 |
|---|---|---|
| **T044 Golomb ruler** | 最短 (m)-标尺长度 (G(m))。已证明最优范围止于 (m=28)，(G(28)=585)；MathWorld/Shearer表说明 (m>28) 未知，分布式搜索在2022证明了28最优。[定义、状态及证明史](https://mathworld.wolfram.com/GolombRuler.html)。29标尺的公开构造记录约为长度623，需锁定标尺坐标文件和归属后才能设为正式baseline；[Projective/affine construction资料](https://cube20.org/golomb/indexp2.html)有可生成记录的元数据。 | **条件接受**：推荐探索 (m=29)，但必须先存档一条实际29-mark witness；只拿585或28标尺作已解校准项没有发现空间。不得承诺能证明最优，OGR29证下界代价巨大。 |
| **T060 covering design** | (C(v,k,t)) 最小化块数。最扎实的开放配置为 (C(24,14,4))：人类最佳已知cover为23块；2026年Lean辅助下界提升到20，故当前区间20–23（20、21、22、23任一值尚未确定）。另 (C(25,15,5)le42) 的公开人类cover，2026 Schönheim推导给下界34；但需再核对cover原始列表。来源：[Chang项目/Lean仓库](https://github.com/jamesyc/covering)（镜像抓取显示同内容，[源项目页](https://tvwatch.su/jamesyc/covering)），[2026 Covering Repository快照说明](https://irsi.ai/tables.html)。 | **接受一个具体配置，条件接受第二个**：24/14/4有明确可量化3的区间且有历史人类上界；需把区块见证作者和原始库条目保存。删除 MVP 中已达简单计数下界的 Steiner 校准例 (C(8,4,3)=14,C(10,4,3)=30)，它们没有纪录空间。 |
| **T061 covering array** | NIST IPOG-F旧数组 (CA(3,10,2)le18)、(CA(3,20,2)le25) 是公开人类算法生成的有效上界，但NIST明确说明其页面仅给upper bounds，不能据此称最优。[NIST定义](https://math.nist.gov/coveringarrays/coveringarray.html)、[数组和下载表](https://math.nist.gov/coveringarrays/ipof/tables/table.3.2.html)。更强的可选具体记录：IRSI 2026表列出 (CAN(3,15,12)le2891)，旧公开表为3486；论文明确这些是新upper bound而非最优证明；其构造包含LLM/agent搜索，不能当成人类baseline。[日期/逐项表/证书归属](https://irsi.ai/tables.html)。 | **条件接受**：优先用 (CA(3,15,12)) 作为“对冻结人类纪录3486改进”的历史挑战，但排行榜必须显式标注2026 agent结果2891，且当前lower bound未在已查材料中核实。NIST 18/25只作历史calibration，非已确认open-gap配置。 |
| **T066 线性码最小距离** | 不要挑表中下界=上界的参数。Grassl/BKLC提供构造、日期和上下界。具体仍开配置示例 ([68,15]_2)：最佳已知距离至少24、理论/数据库上界26，差2；表项源自 Grassl 的在线BKLC表。[参数表数据库](https://www.codetables.de/BKLC/BKLC.php?k=15&n=68&q=2)，[维护说明/贡献者](https://docs.magma-maths.org/CodingTheory/LinearCodes/best-codes.html)。表中给的是人类构造代码下界；应下载生成矩阵再做重算。 | **接受**：用固定 ((n,k,q)=(68,15,2)) 输出生成矩阵、最大化最小距离；当前24–26是真正上下界gap。T066中若数据库上下界相等的行移为校准集。 |
| **T067 unrestricted binary code** | Brouwer表给 (258\le A(17,6)\le340)。下界258来自 M. Milshtein 两误纠错构造（2019）；上界是表中已知界。历史表页还列 (A(18,6)=512–673)、(A(20,6)=2048–2279)，但版本时间较旧，需要查新后再用。[Brouwer binary table](https://aeb.win.tue.nl/codes/binary-1.html)，[Milshtein DOI](https://doi.org/10.1007/s12095-019-00365-7)。 | **条件接受**：17/6 有明确82的数字差距，但只在确认当前上界/下界来源仍有效、拿到代码字列表后进入挑战。构造数量巨大，verification为逐对Hamming距离，外加大小下界证明之外的上界优化困难。 |
| **T068 constant-weight code** | 2026公开构造将 (A(23,6,10)\ge2979)、(A(24,6,10)\ge4214)，相较此前人类显式码2969/4174纪录有进步；构造文作者说明其搜索由AI agent自主发现，故这不是人类baseline。已核来源只给lower bounds，没从权威表中核到最新上界数值。[原始论文](https://arxiv.org/abs/2607.19550)、[Brouwer online table](https://aeb.win.tue.nl/codes/Andw.html)。 | **当前不进入首批**：纪录仍可能有空间，但必须先补齐当前upper bound、可下载码字和人类/AI归属；不要把“插入最大/局部不可改进”误称全局最优。 |
| **T035 cage** | (n(4,10)le320) 是 Exoo、Goedgebeur、Jooken、Stubbe、Van den Eede 的显式4正则、girth-10构造；当前论文表给下界243、上界320。Moore树界242，文中较强的下界是243。 [原始论文/版本](https://arxiv.org/abs/2511.07247)。 | **条件接受**：自然目标是最小顶点数，区间243–320；要加入需获取该320图的实际边表/数据仓库。没有找到“288已知”原始出处，不能沿用。 |
| **T038 forbidden-subgraph ex** | Afzaly–McKay数据库的裸表项目精确到一部分小n，例如 (ex(30,C_4)=85)、(ex(30,\{C_3,C_4\})=76)，都已有sparse6 extremizer；大n项前缀“≥”时只代表构造下界，不证明最大值。页面称其为Afzaly与McKay联合工作。[表的精确/非精确标记说明及图文件](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)。 | **具体 n=30 仅calibration，不能作为突破目标**。已查大n项不少只是无上界认证的best lower bound，但本次未逐项找到一个已锁定数据文件且有数值上界差的可准入新配置。 |

## T035–078 的清理建议

- 删除或降为校准：任何已证明最优的小Golomb ruler；MVP里的 Steiner covering designs（达到 (\binom vt/\binom kt) 计数界）；线性码上下界重合的表项；Afzaly–McKay标为exact的极值图参数；已确定的小covering arrays。参数/禁图族变化是实例，不是额外任务。
- T050固定有限阿贝尔群的最大sum-free子集不再作为开放家族：Green–Ruzsa证明每个有限阿贝尔群的精确最大值，任务可由定理直接判定。不要把非阿贝尔群泛化冒充同一已研究任务。[原论文](https://arxiv.org/abs/math/0307142)。
- T045整数 (B_h) / Sidon集任务和Golomb ruler高度重叠：(B_2) 正是有限Sidon集/Golomb ruler，MathWorld明确给出有限集合的等价关系。不要再把“最大整数Sidon集”加成新任务。[Sidon/Golomb等价和已知区间](https://mathworld.wolfram.com/SidonSet.html)。
- T061数据库表随时间漂移且数据清理有风险。Colbourn旧站点已不可用；IRSI 2026表把“晚2024对比”与最新agent构造分开记录，明确其表格尚未经原表维护者确认，并指出部分单元的旧值可能不是真正最好值。[方法、日期、局限和公开证书](https://irsi.ai/tables.html)。冻结版本并显式记录来源归属。
- T066/067/068/069/070/071/072统称coding不是单一任务。候选数值只要上下界同值就从突破赛中去除；保留资料校验集即可。检查BKLC/Grassl当前页，别凭旧离线表宣称现状。

## 新任务审查（主表T001–T100无同名对象）

按要求审了8个可能新增家族；严格符合“具体open参数 + 公开数值上下界 + 人类见证可复算”的只有第1项。其余不是因泛化空间被排除，就是与现有任务重复或缺一项必要证据，故没有凑足8个可推荐任务。

1. **最小高色数高围长图阶 (n_g(k))**（与cage区别：增加精确色数约束，不是正则度/围长）：2026预印本给 (29\le n_6(4)\le64)，提供64顶点、152边、4色图，图属性和非3-可着色证书已形式核验；作者给出公开论文。[Exoo–Goedgebeur 2019旧界](https://arxiv.org/abs/1901.04881)，[2026新界和证书](https://arxiv.org/abs/2608.23652)。**conditional/推荐候选**，但新64图由2026论文发现，不是旧人类baseline；人类构造上界66可由Exoo–Goedgebeur文章直接下载，首次benchmark应以其66为人类起点并将新64结果单列。下界证书计算成本较高。
2. **(k)-critical图的最大边数 (f_k(n))**：定义是在n顶点、色数k且每个真子图可(k−1)-染色的图中最大化边数。Luo–Ma–Yang 2023指出该问题对所有 (k\ge4) 广泛未解，给足够大n的解析上界；Toft构造对4-critical图有 (n^2/16+n) 边并给明晰结构。[原论文](https://arxiv.org/abs/2301.01656)。**暂不准入**：该来源没有给具体n上可直接配对的当前数值upper/lower interval和下载见证；只说渐近定理不满足本轮实例门槛。
3. **最小边数的k-critical图**：数值目标是固定n,k最小化边数。Kostochka–Stiebitz对k≥6、n≥k+2给解析下界，Toft/Dirac有构造。[Kostochka–Stiebitz 2003](https://doi.org/10.1016/S0095-8956(02)00035-7)。**暂不准入**：没有找到权威公开表给一个新具体(n,k)配对区间及人类图文件；它也和第2项是同一临界图极值谱的另一方向，不建议在100任务里拆成两个。
4. **最少单色三角形的多色完全图 Ramsey multiplicity**：固定q色K_n，最小化单色三角数。2色情形Goodman已给精确公式，n=6最优值2，是calibration而非开放记录；3/4色有近期定量研究但本次未核到可复算的有限n最优值和明确上下界差。[3色问题论文](https://www.math.cmu.edu/users/jcumming/papers/monotri.pdf)、[4色渐近结果](https://arxiv.org/abs/2312.08049)。**不准入本轮**，且与T043最少三角形目标的边界容易混淆，必须把任务定义限定为完整q色 (K_n)。
5. **整数区间中最大Sidon集合**：虽然是自然标量，实为Golomb ruler的逆函数 (R(N)=\max\{m:G(m)\le N-1\})，不是新家族；已知G(m)到28就决定N≤586。[MathWorld](https://mathworld.wolfram.com/SidonSet.html)。**拒绝为新增任务（重复）**。
6. **(K_{m,n}) 普通交叉数**：任务不同于T028的rectilinear交叉数，曾有未解参数；但本次检索发现2026年公开页面声称完整证明Zarankiewicz交叉数猜想，若经正式同行评审确认，则不应再按open记录纳入。旧综述有 (K_{7,9}) 仍开放的陈述，但现状冲突。[2019综述](https://www.researchgate.net/publication/311507856_Topological_Drawings_of_Complete_Bipartite_Graphs)、[2026新页面](https://wcook04.github.io/plectis-atlas/papers/The-crossing-number-of-complete-bipartite-graphs-September-23-2026.html)。**待核/暂缓**：不可用过期open陈述。
7. **线性超图边色数的最大值**（Erdős–Faber–Lovász数值版本）：固定顶点数n，最大化n顶点线性超图的边色数。EFL猜想主张≤n，但Kang等2023已证明充分大的n成立；剩余有限n问题和对象范围需认真核定。[Illinois问题页](https://www.dwest.web.illinois.edu/regs/efl.html)。**不准入**：缺少一个具体未解n的best-known数值和公开达到该值的hypergraph witness；仅以猜想状态不足以选任务。
8. **整数区间中的最大2-basis / additive basis**：理论上可取固定N，把A+A覆盖[0,N]所需的最小基数作为标量；但此轮未找到一套当前公开的精确/上下界表与可下载人类基集记录，且它易退化为覆盖设计/有限加法基变种。**待核，不准入**，不能仅凭“经典加法基”名词认定有benchmark资料。

### 新任务结论

按“至少8个未入库的新家族都要有具体配置数值、上下界gap和人类见证”的标准，本轮**没有足够证据支持8个**。这不是凑数失败，而是主动挡住同题换参数、渐近问题没有可复算有限实例、以及证书成本不明的候选。唯一新增的较强方向是 (n_6(4))，但2026 best-known 64是agent/SAT结果，不能冒充人类baseline；若严格只收人类最好构造，benchmark起点应为2019的66顶点图，指标仍有2顶点改进空间。

## 补充研究池：三类哈希/基问题（2026-11-03）

以下是主审点名的三类新家族，作为**研究池**追加，当前不算正式open benchmark配置。

| 家族 | 具体文献实例 / 人类baseline | 当前可确认的开放度 | 暂定结论 |
|---|---|---|---|
| **Perfect hash family** (PHF(N;k,v,t)) | Walker II–Colbourn (2007) 定义为N行、k列、v元阵列：任意t列至少有一行t个符号两两不同。原文给出显式 (PHF(5;10,3,3)) 并发布表格/构造；文章称这些是best-known上界，精确最小N一般未知。[论文 DOI](https://doi.org/10.1515/jmc.2007.008)、[PHF tables](https://www.phftables.com/)。 | 固定k=10,v=t=3时，已有N=5的人类构造；本轮没核到该条的匹配下界，也没确认表格目前仍是best-known。 | **待核**：对象可用“最大化k”或“最小化N”作为标量，但取得表格档案、完整构造和现行bound前不进入正式名单。 |
| **d-disjunct / d-cover-free binary matrices** | van den Berg、Candès、Chinn、Levin、Olcott、Sing-Long (PNAS 2013) 给出 (d=4,n=400,m=64) 人类构造，以及 (d=2,n=1600,m=44) 构造；前者由覆盖设计导出的码缩短而来。论文表列best-known矩阵并说明具体码的来源。[原文与表](https://pmc.ncbi.nlm.nih.gov/articles/PMC3725070/)、[DOI](https://doi.org/10.1073/pnas.1216318110)。 | 自然标量为固定(n,d)最小行数m。可核到的人类历史上界是64/44；本轮没有取到同参数的当前数值下界和最新行数纪录，故不能称有已量化的open gap。 | **待核**：明确区分disjunct、separable、错误容忍版本。若只做验证，矩阵列必须满足任一列不被任意d个其他列的OR覆盖。 |
| **Global postage-stamp problem / additive h-basis** | Kohonen (2015) 说明一般两邮票目标 (n_2(k)) 只已解决到k=24；OEIS给 (n_2(24)=212) 及历史归属。Kohonen另证restricted目标到k=47，(n_2^*(47)=734)，并列表中给显式restricted基；这个734不能挪作一般目标baseline。[Kohonen原文](https://arxiv.org/abs/1503.03416)、[OEIS A001212](https://oeis.org/A001212)。2026年 Colisson Palais、Dumas、Galan、Grenet、Maignan、Roche 的GStamps库实现local/global算法和basis输出，但此轮未提取到一个可引用的 unrestricted k=25 基及范围数值。[论文](https://arxiv.org/abs/2601.21423)、[GStamps数据/算法库](https://github.com/jgdumas/GStamps)。 | (k=25,s=2) 是一般问题在2015截断后的自然开放配置，但当前具体best-known数值上界及构造尚未核实。restricted (k≤47) 是另一项问题。 | **待核**：与T049“差基”目标不同；但正式实例前必须锁定unrestricted k=25当前基集/范围，不可只以k=24已知或restricted k=47结果做baseline。 |

这些条目已有原始研究和公开构造体系，但眼下尚不具备一致、可复核的“具体参数 + 当前数值纪录 + 上下界差”。因此追加到研究池而非正式候选集。
