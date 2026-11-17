# T088: Shortest addition chain for the P-192 exponent

## English

Return a strictly increasing list of positive integers. It must start at 1 and end at the configured target. Each later entry must be the sum of two earlier entries. The same earlier entry may be used twice. The objective is to minimize `len(chain) - 1`. Subtraction and modular reduction are not allowed.

T088-C01 uses target `2^192 - 2^64 - 3`. The verified public chain uses 202 additions.

## 中文

请返回严格递增的正整数列表。列表从 1 开始，以所选配置的目标结束。每个后续数必须等于两个较早数之和。两个加数可以相同。目标是最小化 `len(chain) - 1`。不允许减法或模约简。

T088-C01 的目标是 `2^192 - 2^64 - 3`。公开链经复算需要 202 次加法。
