# T073 implementation record

Status: `accepted_by_sol`.

The configuration minimizes the number of distinct equal-weight points on the unit sphere `S^3 ⊂ R^4` that integrate every polynomial through total degree five exactly. The checker verifies a common real algebraic field by checking that its integer polynomial is primitive, irreducible over `Q`, and has exactly one real root in the supplied rational interval. It then verifies all unit norms and all 126 monomial moments with exact rational field arithmetic. It has no arbitrary field-degree or coefficient-size limit.

The 24-cell witness uses eight signed coordinate axes and all 16 half-cube sign points. The local witness `data/reference/d4_24cell.json` has SHA-256 `d33b99a4eab8ae059a0ced13a5265e1090ff111cf638ece1cb12c7c1005cc381`. A separately retained exact rational certificate `data/reference/d4_rational24_independent_certificate.json` has SHA-256 `f7332f8bf9ffe3cec5d59f5140570de63645d5ec2863240d2cd4d16a55e94a85`; tests compare all of its rational coordinates with the frozen witness.

The classical source gives `22 ≤ N(3,5) ≤ 24`. A 2025 paper still describes the 24-point design as putatively optimal. The 2026 minimum-design paper concerns strength four on `S^2`; the 2026 odd-dimensional construction paper does not prove a matching lower bound for this `S^3`, strength-five case. The configuration remains open in the sources checked on 2026-11-06.

The standalone initial program returns a 96-point signed-permutation orbit of `(1,1,2,0)/sqrt(6)`. The fixed-seed baseline shuffles a finite list of integer patterns, then uses the fourth-moment identity to select a signed-permutation orbit. Seed 0 examined one pattern and found a valid 24-point design in 0.000464 seconds. The exact witness is saved in `best/seed-0.json`, with the run record in `best/seed-0.metadata.json`. The baseline reads no human or reference witness.

The chosen real-algebraic coordinate model does not restrict the finite minimum over real coordinates. For each fixed point count, the sphere constraints, moment equations, and point-distinctness inequalities form a semialgebraic set over `Q`. Any nonempty such set has a real algebraic point by real-closed-field transfer; finitely many real algebraic coordinates lie in one common primitive number field.

Validation command:

```sh
.venv/bin/python -m pytest tasks/t073/test_task.py -q
```

The tests cover all five entries, the D4 witness and its independent rational certificate, a nonrational `Q(sqrt(6))` valid 96-point design, wrong norms, duplicate points, a valid-norm moment failure, malformed/reducible fields, invalid coordinate types, ignored score claims, and runner error/timeout controls through `mathbench.evaluate._run`. Default generation and verification limits are 300 and 60 seconds, with 4 GiB and one thread.

Result: 11 passed in 12.33 seconds on Python 3.13.12, Linux x86_64. JSON syntax checks passed for the task definition, SOTA, records, and saved run metadata. `git diff --check -- tasks/t073` passed.
