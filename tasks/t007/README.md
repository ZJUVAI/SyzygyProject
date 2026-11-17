# T007：Golomb 尺长度

给定固定数量的整数标记。任意两标记之间的正差必须互不相同。目标是最小化尺长，即最大标记减最小标记。平移不改变尺长，检查器会按此定义计分。

T007-C01 使用 29 个标记，公开人类基准长度为 623。

初始程序固定生成 29 个标记，从 0 开始，每次追加使新差不重复的最小位置。搜索基线用固定种子生成差集有效尺，并受时间预算限制。

# T007: Golomb ruler length

Choose the configured number of integer marks. Every positive pairwise difference must be unique. Minimize ruler length, defined as the largest mark minus the smallest. Translation does not change the score; the checker uses this definition.

T007-C01 uses 29 marks. The public human baseline has length 623.

The initializer uses 29 marks. It starts at zero and repeatedly adds the smallest position whose new differences are fresh. The search baseline uses a fixed seed to generate valid rulers under a time budget.
