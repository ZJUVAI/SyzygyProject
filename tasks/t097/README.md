# T097: Shortest addition chain for the P-192 exponent

## English

Return a strictly increasing list of positive integers. It must start at 1 and end at the configured target. Each later entry must be the sum of two earlier entries. The same earlier entry may be used twice. The objective is to minimize `len(chain) - 1`. Subtraction and modular reduction are not allowed.

The original configuration is `T097-C01`, target `2^192 - 2^64 - 3`. The added configurations are `T097-C02`, target `2^221 - 5`, and `T097-C03`, target `2^521 - 3`. Their public chains have 230 and 532 steps. These chains are constructions, not proofs of minimum length. The checker verifies every addition and the endpoint with exact integer arithmetic.

## 中文

请返回严格递增的正整数列表。列表从 1 开始，以所选配置的目标结束。每个后续数必须等于两个较早数之和。两个加数可以相同。目标是最小化 `len(chain) - 1`。不允许减法或模约简。

正式配置 `T097-C01` 的目标是 `2^192 - 2^64 - 3`。新增配置 `T097-C02` 和 `T097-C03` 的目标分别为 `2^221 - 5` 和 `2^521 - 3`。公开链长度分别为 202、230 和 532 步。这些链是构造，不是最短性证明。检查器会用精确整数运算验证每一步和终点。

All three configurations passed Sol review. 三个配置均通过Sol验收。
