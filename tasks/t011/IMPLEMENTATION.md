# T011 implementation notes

The exact checker selects dimensions from the fixed configuration IDs. It rejects wrong dimensions, non-integer symbols, out-of-range symbols, duplicate words, and every conflicting pair. The objective is the validated number of words.

The standalone initial program uses only the configuration ID and emits `{0,2,4}^k`, of size 3^k. The baseline selects the corresponding dimension and performs randomized greedy construction. The legacy compiled evolution search remains specialized to C01; for C02 and C03 the evolution entry point uses the dimension-aware greedy baseline. Human and reference programs load only their explicitly named comparison witnesses.

C02's public record 108 is a reported result from the 2002 primary paper, not locally reproduced. The exact local traditional construction has 100 words. C03's pinned public 1120-word witness is AI-assisted, as stated in the primary paper. A separate traditional 1101-word product is the frozen human comparator. New configurations are accepted by Sol on 2026-11-07.
