# T077 implementation and verification record

## Configuration and status

- Configuration: `T077-C01`; set size 2 through 512; integer elements in `[-1000000,1000000]`.
- Objective: maximize `ln(|A-A|)/ln(|A+A|)`.
- Frozen human baseline: the explicitly instantiated m=6,L=5 construction, with 462 elements, 8008 sums, and 39733 differences.
- Stronger reproduced reference: a locally instantiated m=7,L=4 formula construction, translated into the configured interval, with 330 elements, 6435 sums, and 33111 differences.
- Reference score interval: `[1.186796554240681248176252398561366157419373951056860834599174878070530850367526991881, 1.186796554240681248176252398561366157419373951056860834599174878070530850367526998206]`.
- Status: `accepted_by_sol`.

## Source and finite construction

Gyarmati, Hennecart, and Ruzsa, [Sums and Differences of Finite Sets](https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf), manuscript dated 2008-05-30, Section 2 equations (13)-(15), define `V(m,L)` as the nonnegative m-vectors with coordinate sum at most L and give formulas for its size, sumset, and difference set. The projection weights satisfy `L_0=1`, `L_(j+1)=2L L_j+1`.

The explicitly given `m=6,L=5` baseline uses weights `[1,11,111,1111,11111,111111]`. Direct enumeration gives 462 distinct projected integers; the largest is 555555. Its closed forms give `|V|=C(11,6)=462`, `|2V|=C(16,6)=8008`, and `|V-V|=sum_(k=0)^6 C(6,k)^2 C(11-k,6)=39733`. Direct pair enumeration matches both counts. Its witness SHA-256 is `0a2b6d7e40a16688d66f6c5e4ad322edb5f7fa38b6015dc4c9a4ce475bc873c4`.

The stronger m=7,L=4 reference is a local instantiation of the same published general formula; the paper does not list it as a separate record. Its weights are `[1,9,73,585,4681,37449,299593]`. The projection has 330 elements in `[0,1198372]`; translating by `-599186` yields `[-599186,599186]`. The formulas give `|V|=C(11,7)=330`, `|2V|=C(15,7)=6435`, and `|V-V|=sum_(k=0)^7 C(7,k)^2 C(11-k,7)=33111`. Exact pair enumeration matches both counts. Its witness SHA-256 is `916221446c05549172b608ad38361ee4008e9b4a5a9516cced3eace4ffbbfa8b`. The score `ln(33111)/ln(6435)` is enclosed by the reference interval above. This is a derived construction, not a separate result claimed by the paper.

The finite scores are computed from these counts. They are not asymptotic exponents. The source's separate `1.27155...` statement is for a different construction and condition. The checked source gives no proof of a maximum for this task's finite cardinality and interval bounds.

## T012 comparison and ranking reversal

T012 uses `ln(|A+A|/|A|)/ln(|A-A|/|A|)`. T077 uses `ln(|A-A|)/ln(|A+A|)`. I verified both with a pair of sets within T012's cardinality and coordinate bounds. For `A={0,2,3,4,7,11,12,14}`, the counts are `(n,s,d)=(8,26,25)`. For `B=A union (A+1000)`, they are `(16,78,75)`. Both satisfy T012's checker precondition `s>d>n`.

The certified scores are:

- T012: `A=1.0344212156259981...`, `B=1.0253872280449059...`, so `A>B`.
- T077: `A=0.9879620776439305...`, `B=0.9909976280918725...`, so `A<B`.

The exact sets are pinned in `data/source/t012_order_reversal_examples.json`, SHA-256 `39f9c9ce2f89088028b20d3ddbf6612c96a694f9725f615593bccd11b3220bf2`. Tests recompute their integer sets and compare outward-rounded score intervals. This verifies that the objectives do not preserve rankings.

## Programs

- `check.py` validates cardinality, integer types, uniqueness, and bounds. It computes both finite sets with exact integer arithmetic. It then uses 80-digit outward-rounded `mpmath.iv` logarithm intervals. The reported maximization objective is the interval's lower endpoint; `details` records both endpoints. Declared candidate scores do not alter the returned result.
- `init_program.py` is standalone and returns `{0,1,3}`.
- `baseline.py` performs seeded one-element replacement, addition, or removal hill climbing from the simple set.
- `evolution.py` performs seeded elitist population search from the same simple set.
- Search uses ordinary floating point only for proposal ranking. Search programs do not load source or witness data.
- `human.py` generates the frozen m=6,L=5 projection from the published formula. `reference.py` replays the stronger saved m=7,L=4 translated construction.
- `evaluator.py` uses the shared evaluator adapter. The task registry remains unchanged until Sol review.

## Checks performed

Tests cover the m=6,L=5 baseline and m=7,L=4 formula counts, all five program entries, the T012/T077 ranking reversal, cardinality endpoints 2 and 512, coordinate endpoints, duplicate elements, bool/float/NaN/infinity inputs, wrong cardinality and configuration, forged scores, interval containment, runner errors, and timeouts.

Commands:

```sh
.venv/bin/python -m pytest tasks/t077 -q
.venv/bin/python -m json.tool tasks/t077/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t077/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t077/records.json > /dev/null
.venv/bin/python -m json.tool tasks/t077/data/source/source_notes.json > /dev/null
.venv/bin/python -m json.tool tasks/t077/data/source/t012_order_reversal_examples.json > /dev/null
```

Results on CPython 3.13.12, Linux x86_64:

- `.venv/bin/python -m pytest tasks/t077 -q`: 8 passed in 4.01 seconds on the final correction run.
- JSON parsing and `git diff --check` passed for the task files.
- Seed 0, default fixed budgets, no time cutoff: initial set `{0,1,3}` scored `1.0860331325...`; baseline after 500 iterations returned 7 elements with 28 sums and 43 differences, certified score `1.128742279835580183801165884128509936558262846009138578600021615215852105461740443719`, in 0.006 seconds; evolution after 60 generations returned the same score in 0.001 seconds.
- `human.py` returned the frozen 462-element m=6,L=5 baseline with 8008 sums and 39733 differences. `reference.py` returned 330 translated m=7,L=4 elements with 6435 sums, 33111 differences, and the reference score interval above.
- The n=512 boundary test recomputed the 512-element interval set's 1023 sums and 1023 differences.
- Runner defaults remain 300 seconds for generation, 60 seconds for verification, 4 GiB memory, and one thread. Tests exercise `_run` error and timeout paths. The full repository suite was not run.

This implementation has not been accepted by Sol. It remains `accepted_by_sol`.
