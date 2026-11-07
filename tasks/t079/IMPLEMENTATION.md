# T079 implementation notes

Status: `accepted_by_sol`.

## Fixed problem and sources

- Configuration `T079-C01` fixes `F_31^3` and all 993 projective directions. A candidate supplies one origin for each canonical direction. The objective is the number of distinct points on the supplied lines, minimized.
- `check.py` canonicalizes directions with the last nonzero coordinate equal to one. It requires every canonical direction once, validates all coordinates as non-boolean integers in `0..30`, generates all 31 points per line modulo 31, and counts the full union exactly.
- The traditional human baseline uses the odd-field quadratic-residue almost-Kakeya construction and the full plane `t=0`, as described in Bukh and Chao, *Sharp density bounds on the finite field Kakeya problem* (2021), Section 4. Its line witnesses have been reconstructed and exactly checked: 8,641 points.
- The best directly sourced same-parameter result in this review is the Station construction in Chung, Du, and Wesley, *Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment*, arXiv:2608.23691v2 (2026-09-14), Section 6.1, Theorem 2.1. For `p=31`, their formula gives `(2*31^3 + 7*31^2 + 3)/8 = 8,289`. The paper discloses AI multi-agent discovery and external GPT-5.5 assistance in formal verification. The first-party verification notebook gives the construction and checks the formula and line witnesses for odd primes through 47. This task rebuilt the p=31 line witnesses and independently checked all 993 lines and the exact 8,289-point union.
- Georgiev et al., arXiv:2511.02864v3, Section 6.1, describes AlphaEvolve finite-field Kakeya work. A secondary public record list attributes 8,290 at p=31 to AlphaEvolve. The exact number was not found in the inspected primary paper or official notebook, and this task has not reconstructed that witness. It is weaker than the reproduced 8,289 result.
- Bukh-Chao Theorem 1 gives the finite lower bound `|K| >= 31^5/61^2 = 28,629,151/3,721`, so integer cardinality is at least 7,694. This does not close the gap to 8,289. No finite optimum proof at p=31 was found in the bounded source review as of 2026-11-06. A non-primary online 8,288 claim had no identified witness or primary derivation, so it is not used as the reliable record.
- Source versions, locations, and provenance notes are in `data/source/source_manifest.json`. Human and public/reproduced witnesses are stored separately under `data/human/` and `data/reference/`.

## Programs and search isolation

- `init_program.py` is standalone and has no task-package import. It places every line through the origin. This covers the full space and gives a valid simple starting construction of 29,791 points.
- `baseline.py` and `evolution.py` start from that same simple anchor assignment. They run a seeded randomized greedy coordinate search. Each candidate anchor is scored by an exact occupancy-count update. The search code does not load or import human, reference, or public comparison witnesses.
- `human.py` generates the classical quadratic-residue line witnesses from the published formula. `reference.py` reconstructs the Station's published 8,289-point line system. Neither of these is read by the search programs.
- The saved task-local evolution result is seed 0, eight full sweeps and 127,104 evaluated anchors. It has 15,534 points. It was generated and checked through the shared runner with 300-second generation, 60-second verification, 4 GiB memory and one thread. Its actual result and environment are in `best/T079-C01/result.json`; its witness hash and replay command are in `best/T079-C01/provenance.json`.

## Validation

Run:

```sh
.venv/bin/python -m pytest tasks/t079/test_task.py -q
```

The suite checks the 993-direction count, the exact human and public/reproduced constructions, the full-space boundary seed, malformed and duplicate inputs, configuration checks, ignored claimed scores, all five program entries, search reproducibility and isolation, a clean-export initializer, evaluator integration with a temporary registry patch, and runner error and timeout paths. The complete local run returned `30 passed in 12.20s`.
