# T011: Independent sets in strong powers of C7

For each fixed power `k`, maximize the number of distinct words in an independent set of the strong power `C7^k`. A word is a vector in `{0,...,6}^k`. Two words conflict when their cyclic distance is at most one in every coordinate. The checker verifies every unordered pair exactly. No selected power is claimed to be solved.

| Configuration | Power | Frozen human comparator H | Public same-parameter result | Local replay |
|---|---:|---:|---:|---:|
| T011-C01 | 5 | 367 | 367 (Polak–Schrijver) | 367 |
| T011-C02 | 4 | 100 | 108 (Vesel–Žerovnik, 2002) | 100; the published 108 witness is not transcribed here |
| T011-C03 | 6 | 1101 | 1120 (AI-assisted, Itty et al., 2026) | 1120 from the pinned repository file |

C02 and C03 passed independent Sol review. The 100-word C02 comparator is the Cartesian square of a 10-word independent set in `C7^2`. The cited 2002 paper reports 108, but its figure was not converted into a machine-readable witness. The 2026 paper states that `alpha(C7^4)` remains unknown.

The C03 human comparator is the product of the published 367-word `C7^5` witness and `{0,2,4}`. The 1120-word public witness is marked AI-assisted because the paper says it was found through iterative LLM interaction. Its source file is pinned by commit and SHA256 in `data/source_manifest.json`.
