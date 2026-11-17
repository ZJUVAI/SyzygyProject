# T073: Low-autocorrelation binary sequence energy

## 中文

给定配置长度 `L`，构造恰好 `L` 个整数符号，每项为−1或+1。最小化非周期自相关能量 `E=Σ(k=1..L−1)(Σ(i=0..L−1−k)s[i]s[i+k])²`。检查器用整数精确计算。正式配置的长度为 100。

Dantus 公开表给出 L=100 的游程编码，能量为578。已展开该见证，并用整数运算精确重算成绩。来源未说明发现者。该记录没有证明全局最优。

简单起点是交替符号序列。传统搜索使用固定种子的单符号翻转模拟退火，不读取人类见证。配置从 `MATHBENCH_CONFIG_ID` 读取。

## English

For the selected length `L`, return exactly `L` integer signs, each −1 or +1. Minimize the aperiodic autocorrelation energy `E=sum(C[k]**2,k=1..L-1)`, where `C[k]=sum(s[i]*s[i+k],i=0..L-1-k)`. The checker uses exact integer arithmetic. The official length is 100.

The public Dantus table gives a run-length encoding for L=100 with energy 578. The witness was expanded and its energy was recomputed with integer arithmetic. The source does not name the discoverer. This record is not a proof of global optimality.

The simple seed is an alternating sign sequence. The classical baseline uses seeded single-sign-flip simulated annealing and does not read human witnesses. Select a configuration with `MATHBENCH_CONFIG_ID`.
