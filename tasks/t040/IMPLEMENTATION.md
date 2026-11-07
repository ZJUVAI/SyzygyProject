# T040 implementation record

**Status: accepted by Sol on 2026-11-06.**

## Scope

- Configuration: T040-C01, 11 distinct points on S², maximize convex-hull volume.
- Exact feasibility: all coordinates are rational and each point has squared norm exactly 1.
- Exact score: enumerate all 165 triples, test supporting half-spaces with `Fraction`, merge each coplanar plane by a canonical integer quadruple, form the exact projected polygon hull, and triangulate each face once.
- Frozen reference: exact rational reconstruction of the Hardin–Sloane–Smith source decimals. The rational score is about 2.3546344950686153. It is not the unrounded source score.
- Search: a Fibonacci-sphere seed and fixed 400-step, seed-0 coordinate perturbation search. SciPy volume is search feedback only. The search does not read reference or witness files.
- Budgets: task configuration records 300 s generation, 60 s verification, 4 GiB, and one numerical thread. Local direct test environment: Python 3.13.12, Linux x86_64.

## Research checks

The [Hardin–Sloane–Smith results page](https://neilsloane.com/maxvolumes/index.html) attributes its putatively optimal arrangements and volume table to R. H. Hardin, N. J. A. Sloane, and W. D. Smith, copyright February 1994. Its dimension-3, 11-point row reports `2.354634495069`. The original coordinate archive is saved as `data/maxvol.3.11.txt`; its SHA-256 is `5add684454391c037f97c1d1dd05374387fd3c7b3a12cf13708ebbc7808727e3`. The reconstructed witness is saved as `data/reference/sloane11_rational_stereographic.json`; its SHA-256 is `69e632317609db1f28ee4f055e1e32ced068718a81568e3a246c097314918b9a`. Its exact score is `2.3546344950686153`, which agrees at the source's reported precision. The `2.35462915` value from Mutoh's 2003 paper is retained as a weaker historical local candidate.

The arXiv history for [2608.04392](https://arxiv.org/abs/2608.04392) listed only v1, submitted 2026-08-05, when checked on 2026-11-06. Its full text says N=10, N=11, and all N≥13 remain open, and says N=10 has a forthcoming separate paper. Table 1 lists N=11 without a known maximizer or value. Searches for later closure work found no 11-point proof. The task therefore remains an open optimization problem, not a claim of global optimality.

## Validation

- `.venv/bin/python -m pytest tasks/t040/test_task.py -q` — 14 passed.
- The tests include the human and reference entries, a valid initial construction, deterministic bounded search, full-result invariance under changed `objective`, `score`, and `claimed_score` fields, malformed size, duplicate points, non-unit points, booleans, non-finite values, invalid rational strings, a four-vertex coplanar facet, a north-pole chart point, and `mathbench.evaluate._run` program-error and timeout paths.
- The human witness checker independently recomputes 18 support planes, 18 triangulated boundary faces, and exact volume `198893207780365769546079296068126608395399333218703055137820126205188303595151289289727146422929302157468452876518718396242714712605660095116722166715365377366230003031600792644897607640044633803089561356572370392531912813965534618945846612941731068419196618544/50445172460346349448931641996860021144264476728999599176187408572976212835152631647619651442094323827977099413655298851423455071595216816503133422619261915629737015532132820244223007249160881159274735569209765278159373027141806695314634921970384094889105909787`.
- `.venv/bin/python -m json.tool tasks/t040/task.json >/dev/null` and the same command for `records.json` and `sota.json` — passed.
- Direct local checker runs take under 0.1 s for the large rational reference witness on the recorded environment.

## Review limits

The shared registry does not yet list T040. The task agent did not edit shared files. The runner's `_run` program-error and timeout controls are tested directly without registry access. End-to-end `evaluate(program_path)` still needs Sol's temporary registry admission and review. The runner remains a resource limiter, not a security boundary.


## Additional sizes

C02 has 13 points and C03 has 15 points. The Hardin–Sloane–Smith author table reports volumes 2.612834152060 and 2.804379381835. Its displayed decimal coordinates are saved locally. The human and fixed reference programs use exact rational stereographic points reconstructed from these archives. The checker verifies the sphere equation, distinct points, and exact supporting-plane volume. The author table treats these volumes as putative optima. The new configurations are accepted by Sol on 2026-11-07.

新增 C02 为13点，C03 为15点。公开报告体积分别为2.612834152060和2.804379381835。用存档坐标重建有理球面点，再精确计算凸包体积。公开报告与精确复算分开记录。新增配置已通过 Sol 验收（2026-11-07）。
