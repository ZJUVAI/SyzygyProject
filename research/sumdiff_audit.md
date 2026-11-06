# Sum–difference benchmark audit (I / II / III)

## Finding

These are three genuinely different optimization tasks from §6.25 (“Sums and differences problems”) of Georgiev, Gómez-Serrano, Tao and Wagner, *Mathematical exploration and discovery at scale* (2025; problems 6.42–6.44). Each has a natural real-valued score computed exactly from a finite integer-set witness. They should be retained as three separate candidates, with the important caveat that the unbounded/global formulations need a benchmark resource configuration (for example, maximum support cardinality and maximum coordinate magnitude) so a run has a finite search domain. Such caps are configuration, not a redefinition of the score.

**Recommendation:** I and III are good first-wave construction tasks. II is a sound mathematical objective with a real human construction, but should be conditional until a compact, finite human witness and a reproducible configuration are attached. Do not collapse these into one task: they optimize different logarithmic ratios and III is a certificate for a two-set asymptotic theorem.

## I. Normalized sum–difference exponent (MSTD direction)

- **Original problem.** $C_I$ is the least $C$ such that, for every nonempty finite $A\subset\mathbb Z$,
  \[
  \frac{|A+A|}{|A|}\leq\left(\frac{|A-A|}{|A|}\right)^C.
  \]
- **Finite-witness task and scalar.** Return a finite integer set $A$, and maximize
  \[
  s_I(A)=\frac{\log(|A+A|/|A|)}{\log(|A-A|/|A|)}.
  \]
  The ratio is well-defined for $|A|\ge 2$, since $|A-A|/|A|>1$. The evaluator computes both sumset cardinalities exactly; no yes/no test is being substituted for the objective.
- **Human baseline.** Freiman–Pigarev’s 17-element construction, reproduced and credited to them by Martin–O’Bryant (2006), is
  $A=\{0,1,2,4,5,9,12,13,14,16,17,21,24,25,26,28,29\}$.
  Direct finite-set counting gives $|A+A|=59$, $|A-A|=55$, and score $\log(59/17)/\log(55/17)=1.0597930945\ldots$. AlphaEvolve’s paper gives the same human baseline and upper bound 2. Martin–O’Bryant’s paper is primarily about MSTD sets, so it is a source for the construction/provenance, not the source of the exponent definition.
- **Current status distinction.** The 2026 preprint by Lin and Li constructs a family with score tending to 2 and explicitly says the proof was developed with assistance from AI research agent Hyra. Thus 2 is now claimed as the sharp global supremum in that preprint; it is not a human baseline and should not be represented as one. The task can still measure finite-budget construction quality against score 2 or a frozen finite-size record. Report the finite witness and score, not merely the limiting theorem.
- **Configuration.** Cap $|A|$ and $\max A-\min A$ (or coordinate bit length); translate/reflect/scale normalization may fix $\min A=0$, $\gcd(A-A)=1$. These are search constraints only; score remains the expression above.
- **Verification cost / risk.** Exact enumeration of $A+A,A-A$ is $O(|A|^2)$ pair generation plus deduplication, practical for hundreds/thousands of elements. Main risk is unbounded-domain ambiguity and stale “best known” claims; keep a dated record and separate theorem-level limit from finite-size records.
- **Recommendation:** `accept` (with finite resource caps and dated leaderboard). A mathematical scalar objective and an explicit human construction are verified.

## II. Ordinary sum–difference exponent (unnormalized cardinalities)

- **Original problem.** $C_{II}$ is the least $C$ such that
  \[
  |A-A|\leq |A+A|^C
  \]
  for every nonempty finite integer set $A$.
- **Finite-witness task and scalar.** Return a finite integer set $A$ and maximize
  \[
  s_{II}(A)=\frac{\log|A-A|}{\log|A+A|}.
  \]
  This is not I: the factors $|A|$ are absent. The denominator is positive for every nonempty integer set because $A+A$ has at least one element, but singleton input gives $0/0$; specify $|A|\ge2$.
- **Human baseline.** Hennecart–Robert–Yudin’s 1999 simplex construction gives the asymptotic lower bound
  \(\log(1+\sqrt2)/\log2=1.271553\ldots\), as stated in the AlphaEvolve paper. Their construction is a family in a high-dimensional integer lattice; finite Freiman embedding/projection preserves the two relevant sumset cardinalities for a finite configuration and yields integer examples. The original Astérisque paper is the primary construction reference. The exact finite projected witness and its size were **not verified in this audit**; record the asymptotic human lower bound as literature baseline, not as an exact finite leaderboard entry.
- **Known bound context.** AlphaEvolve reports the classical upper bound $C_{II}\le4/3$, attributed there to Freiman–Pigarev (1973), and the simplex lower bound above. Hennecart–Robert–Yudin is the primary source for its construction; the 4/3 citation is to a Russian 1973 source and should not be presented as independently re-derived here.
- **Configuration.** A benchmark instance must specify maximum set cardinality and maximum coordinate magnitude/bit length, and should accept only integer sets. To capture the HRY baseline faithfully, permit a declared dimension and an explicit Freiman embedding or provide a finite projected witness as baseline artifact. Do not use a dimension parameter as a separate task.
- **Verification cost / risk.** Exact score calculation is quadratic in $|A|$. The risk is not verifier expense but a mismatch between an asymptotic lattice construction and a finite integer-set output; a baseline family without an explicit finite member is insufficient for a reproducible score comparison.
- **Recommendation:** `conditional`. Keep as a distinct numeric construction problem; before first-wave use, attach an explicit finite integer witness from the HRY family and freeze the finite search caps. Do not reject it as a Boolean existence question.

## III. Gyarmati–Hennecart–Ruzsa finite certificate for the two-set exponent

- **Original asymptotic problem.** $C_{III}$ is the supremum of exponents $C$ for which there are arbitrarily large finite integer sets $A,B$ satisfying $|A+B|\lesssim|A|$ and $|A-B|\gtrsim|A|^C$. This is a two-set asymptotic growth problem, not II’s single-set ratio.
- **Finite certificate and scalar.** Return a finite $U\subset\mathbb Z_{\ge0}$ with $0\in U$ and define $s=|U+U|, d=|U-U|, q=2\max U+1$. The GHR construction yields the certificate
  \[
  s_{III}(U)=1+\frac{\log(d/s)}{\log q},\qquad C_{III}\ge s_{III}(U),
  \]
  under the source’s condition $d<q$ (equivalently $d\le 2\max U+1$ for these sets; the paper’s lemma is stated strictly). Optimize this real scalar over valid $U$. This is an externally proved finite-to-asymptotic certificate, not the raw ratio from II.
- **Human baseline.** Gyarmati, Hennecart and Ruzsa (2007), in their theorem following the finite-set digit construction, report computational search over sets $U$ and the witness $U=\{0,1,3,6,13,17,21\}$, optimal among eligible sets of cardinality at most 11. Exact counting gives $|U+U|=26, |U-U|=39, q=43$, hence score $1+\log(39/26)/\log43=1.1078020567\ldots$. The same paper develops a stronger simplex-based human lower bound (the then best asymptotic value cited by AlphaEvolve is 1.14465); keep that as a separate theorem/family baseline, not as the finite-$U$ leaderboard score. The AlphaEvolve paper later records its own 1.1584 result and further 2025 bounds; these are AI/newer results and must be labeled separately from the 2007 human witness.
- **Configuration.** Specify an upper bound for (|U|) and (max U), with canonical normalization (0\in U\subseteq[0,M]). These constraints define the search budget; the score formula and certificate theorem remain fixed. If comparing against the published size-\(\le11\) result, use exactly that cardinality limit and make the magnitude cap explicit; do not imply the old exhaustive search covered unbounded coordinates without checking its search domain.
- **Verification cost / risk.** Count (U+U,U-U) exactly in (O(|U|^2)). The certificate check is also exact integer arithmetic except for final logarithms; compare scores using (s^q\) or high precision if needed. Primary risks are theorem transcription and certificate eligibility: require nonnegative integers, zero included, and (d<q); do not score an invalid (U).
- **Recommendation:** `accept`. This is an unusually good benchmark: published finite witness, scalar score, compact exact verifier, and a theorem translating a candidate into a meaningful asymptotic lower bound.

## Primary sources checked

1. Georgiev, Gómez-Serrano, Tao, Wagner, [*Mathematical exploration and discovery at scale* (2025), arXiv:2511.02864](https://arxiv.org/abs/2511.02864), §6.25, Problems 6.42–6.44. Local copy examined at `research/sources/alphaevolve_paper.html`; the GitHub repository is [google-deepmind/alphaevolve_repository_of_problems](https://github.com/google-deepmind/alphaevolve_repository_of_problems). The repository’s current problem HTML pages render as empty templates, so the paper is the authoritative accessible statement in this audit.
2. Greg Martin and Kevin O’Bryant, [“Many sets have more sums than differences” (2006)](https://arxiv.org/abs/math/0608131), journal version in *Additive Combinatorics* (2007). Its text identifies the 17-element MSTD example as a construction of Pigarev and Freiman.
3. François Hennecart, Gilles Robert, Alexander Yudin, [“On the number of sums and differences” (1999)](https://www.numdam.org/item/AST_1999__258__173_0/), *Astérisque* 258, 173–178. Primary source for the high-dimensional simplex construction underpinning II.
4. Katalin Gyarmati, François Hennecart, Imre Z. Ruzsa, [“Sums and differences of finite sets” (2007)](https://doi.org/10.7169/facm/1229618749), *Functiones et Approximatio* 37(1), 175–186; [author-hosted PDF](https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf). Primary source for III’s finite (U)-certificate and the seven-element example.
5. Haowei Lin and Shanda Li, [“Settling the Optimal Exponent Relating Sumsets and Difference Sets” (2026)](https://arxiv.org/abs/2607.27199). arXiv abstract states normalized ratio tends to 2 and explicitly acknowledges AI-agent assistance.

## Corrections / traps

- The AlphaEvolve source reference is **§6.25**, but the individual problems are **6.42, 6.43, 6.44**.
- I’s (|A+A|/|A|) and (|A-A|/|A|) ratio, II’s raw (|A-A|) versus (|A+A|) ratio, and III’s two-set exponent/certificate are not interchangeable.
- Hennecart–Robert–Yudin’s 1999 paper also discusses the raw logarithmic quotient (log|A+A|/\log|A-A|); do not mistake that inverse raw quotient for either I or II.
- The human 2007 seven-element (U) gives a finite certificate for III. It is not an optimality result over all (U); the paper’s computational claim is only optimality for (|U|\le11) within the searched range.
- Keep human historical baselines and AI-generated later records in separate fields. A theorem-level limit is not a finite witness score.
