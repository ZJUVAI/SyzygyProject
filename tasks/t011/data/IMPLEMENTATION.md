# T011 implementation notes

The exact checker accepts the fixed configuration T011-C01 (`q=7`, `power=5`). It rejects wrong dimensions, non-integer symbols, out-of-range symbols, duplicate words, and every conflicting pair. The objective is the validated number of words.

The standalone initial program uses only the configuration ID and emits `{0,2,4}^5`, of size 243. The baseline performs randomized greedy construction. The compiled evolution search is specialized to C01. Human and reference programs load only the explicitly named C01 comparison witness.

The C01 public 367-word construction is reproduced from Polak and Schrijver and validated by the exact checker. This is a verified lower bound; optimality is not proved.
