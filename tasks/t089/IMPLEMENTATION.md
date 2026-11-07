# T089 implementation record

Status: **已通过 Sol 验收（2026-11-06）**.

## Frozen configuration and score

`T089-C01` uses finite rational polynomials `p(t)` with `t=pi*x^2`, without a configured degree cap. The checker derives the Fourier polynomial exactly from

`t^k exp(-pi*x^2) -> sum_r (-1)^r (2k)! 4^(r-k) / ((k-r)! (2r)!) t^r exp(-pi*x^2)`.

It requires both constant terms to be strictly negative and both leading terms to be positive. It uses SymPy's exact rational real-root isolation to locate the final negative-to-positive root. It tests the signs in every root-free gap, so a later even-multiplicity contact does not enlarge the radius. The raw product is enclosed with exact rational root intervals and a Machin-series rational interval for pi. The runner ranks by the conservative upper endpoint.

The frozen human polynomial is `p(t)=t^2-3t/2-1/1000`. Since `H_4(sqrt(2t))/64=t^2-3t/2+3/16`, this is an H4 Gaussian plus a rational H0 term. Both Fourier eigenvalues are +1. Its final positive root is `3/4+sqrt(1127/2000)`, giving raw product `(3/4+sqrt(1127/2000))/pi`, about `0.4776769416361765`.

## Source review

- Gonçalves, Oliveira e Silva, and Steinerberger, 2017, for the human Hermite-Gaussian construction: <https://doi.org/10.1016/j.jmaa.2017.02.030>.
- Georgiev et al., 2025, report the announced human result `0.3102` and AlphaEvolve `0.321591`: <https://arxiv.org/abs/2511.02864v1>.
- Station v2 reports `0.3089` from an exact rational degree-226 polynomial-Gaussian witness. The source states that the discovery came from its AI-agent system; the paper's method section describes GPT-5.5, Claude Opus 4.8, and Gemini 3.1 Pro agents: <https://arxiv.org/abs/2608.23691>.
- The exact public witness coefficients are retained under `data/source/station_0_3089_source_witness.json`. Their origin is pinned in `data/source/station_source_pin.json` to commit `a4ae9192fa75b7ffc6909ed018a712510062378b`; the compressed upstream bundle SHA-256 is `04440bb9d0239a68ed38b7d780462380c2b698fdf54f0917c628ff7df35b9826`.
- The public 226-degree certificate was not replayed by this implementation. It is reported as the strongest public bound found, not as the reproduced reference score. The frozen reference is the independently verified human Hermite construction.
- Tomar's October 2026 preprint narrows the unrestricted constant to squared radii `(0.30272004, 0.30349081]` using a mixture of Gaussians. This is a different witness family and is recorded separately: <https://www.mefyi.com/papers/sign-uncertainty-constant/>.
- No optimality proof for this configuration was found in sources checked through 2026-11-06.

## Program isolation and budgets

`init_program.py` returns a low-degree H4 seed. `baseline.py` and `evolution.py` search independently over short H4/H8 self-Fourier combinations using seeded random coefficient changes. They do not read `data/source/` or the human/reference programs. `human.py` rebuilds the exact H4 example. `reference.py` returns the same frozen reproduced human witness.

Search defaults are fixed at 80 iterations for `baseline.py` and 300 for `evolution.py`. The seed comes from `MATHBENCH_SEED`. The shared runner defaults remain 300 seconds for generation, 60 seconds for verification, 4 GiB memory, and one thread. Exact root isolation of high-degree candidates can use the full verification budget; no coefficient or degree cap is added.

## Validation

Run:

```sh
.venv/bin/python -m pytest tasks/t089/test_task.py -q
.venv/bin/python -m json.tool tasks/t089/task.json > /dev/null
.venv/bin/python -m json.tool tasks/t089/sota.json > /dev/null
.venv/bin/python -m json.tool tasks/t089/records.json > /dev/null
```

Results on Python 3.13.12 in `.venv`: `17 passed in 1.72s`; all JSON checks passed. Tests cover Fourier coefficients, the human witness, a simple seed, baseline and evolution outputs, a polynomial with a later even-multiplicity contact, strict origin signs, eventual tail sign, malformed rational/boolean/non-finite data, fixed-configuration and strict configuration-type checks, forged score fields, and runner error/timeout handling.

The task-local test verifies a deliberate program error and timeout through `mathbench.evaluate._run`. It does not register T089 in the shared runner registry. The missing task ID in a separate process remains expected until Sol admission.
