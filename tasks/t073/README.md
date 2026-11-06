# T073: Low-autocorrelation binary sequence energy

## 中文

给定配置长度 `L`，构造恰好 `L` 个整数符号，每项为−1或+1。最小化非周期自相关能量 `E=Σ(k=1..L−1)(Σ(i=0..L−1−k)s[i]s[i+k])²`。检查器用整数精确计算。L=80、100、120三个配置均通过Sol验收，已加入正式运行目录。

Dantus 公开表给出三个长度的游程编码。L=100 的能量为578。新增行分别给出 L=80、E=352 和 L=120、E=872。新增见证已展开并逐项精确重算。表格未署这两行的个人发现者，归属记为未知。来源给80和120都标了星号，并说明这些长度未由穷举确定，可能存在更高 merit factor（即更低能量）。因此这些数值是已复现的公开构造，不是最优性证明。

简单起点是交替符号序列。传统搜索使用固定种子的单符号翻转模拟退火，不读取人类见证。配置从 `MATHBENCH_CONFIG_ID` 读取。

## English

For the selected length `L`, return exactly `L` integer signs, each −1 or +1. Minimize the aperiodic autocorrelation energy `E=sum(C[k]**2,k=1..L-1)`, where `C[k]=sum(s[i]*s[i+k],i=0..L-1-k)`. The checker uses exact integer arithmetic. The L=80, L=100, and L=120 configurations passed Sol review and are in the run registry.

The public Dantus table gives run-length encodings at all three lengths. The L=100 row has energy 578. The added rows give energy 352 at L=80 and 872 at L=120. The new witnesses were expanded and their energies were recomputed with integer arithmetic. The table gives no individual discoverer for these rows, so attribution is unknown. It marks both new lengths with an asterisk and says they were not determined by exhaustive methods; larger merit factors, and thus lower energies, may exist. These are reproduced public constructions, not proofs of optimality.

The simple seed is an alternating sign sequence. The classical baseline uses seeded single-sign-flip simulated annealing and does not read human witnesses. Select a configuration with `MATHBENCH_CONFIG_ID`.
