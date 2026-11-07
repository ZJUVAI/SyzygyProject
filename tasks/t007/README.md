# T007：Golomb 尺长度

给定固定数量的整数标记。任意两标记之间的正差必须互不相同。目标是最小化尺长，即最大标记减最小标记。平移不改变尺长，检查器会按此定义计分。

已接入的 C01 使用 29 个标记，公开人类基准长度为 623。C02、C03均通过Sol验收，分别有30、32个标记。cube20.org 的公开 `rulers-all-00` 数据给出长度 680、784 的构造；对应公开元数据记录射影平面模尺，素数幂29、31，乘数71、116。检查器会分别检查435、496个差。这些是可行构造，不是最优性证明。三个配置均已加入运行目录。

初始程序按 `MATHBENCH_CONFIG_ID` 读取标记数，从 0 开始，每次追加使新差不重复的最小位置。搜索基线用固定种子生成差集有效尺，并受时间预算限制。

# T007: Golomb ruler length

Choose the configured number of integer marks. Every positive pairwise difference must be unique. Minimize ruler length, defined as the largest mark minus the smallest. Translation does not change the score; the checker uses this definition.

Accepted C01 uses 29 marks and has a public human baseline of length 623. C02 and C03 passed Sol review, with 30 and 32 marks. The public cube20.org `rulers-all-00` data gives feasible rulers of lengths 680 and 784. Its metadata records projective-plane modular rulers with prime powers 29 and 31, and multipliers 71 and 116. The checker checks 435 and 496 differences. These constructions do not prove optimality. All three configurations are in the run registry.

The initializer reads the mark count from `MATHBENCH_CONFIG_ID`. It starts at zero and repeatedly adds the smallest position whose new differences are fresh. The search baseline uses a fixed seed to generate valid rulers under a time budget.
