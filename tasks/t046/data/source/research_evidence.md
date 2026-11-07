# T096 source and status evidence

Checked on 2026-11-06. This note records the finite-degree sources checked for
the fixed configuration `degree_at_most=146` on `[0,1]`.

## Meichsner (2009)

Alan Meichsner, *The Integer Chebyshev Problem: Computational Explorations*,
PhD thesis, Simon Fraser University, 2009. Public full text:
<https://www.collectionscanada.gc.ca/obj/thesescanada/vol2/002/NR59810.PDF>.

- The abstract says that nth integer Chebyshev polynomials on `[0,1]` are given
  for every degree `n <= 145`.
- Table 1.2 is headed “Integer Chebyshev polynomials for the interval `[0,1]`
  (`n = 77 to 154)”. The entries `n=145` and `n=148` include factor products
  and a numerical reciprocal nth-root value. The `n=146` row gives only
  `>= 2.346298` in that column and no factor product or polynomial. It is a
  one-sided reported bound, not an exact n=146 table entry.
- The thesis defines `h1(x)=x(1-x)` in Section 1.3.3. The saved comparison
  construction is our explicit degree-146 reconstruction `h1(x)^73`; it is
  not represented as the omitted n=146 polynomial from the thesis.
- The thesis states that every n-th integer Chebyshev polynomial on `[0,1]`
  has degree exactly `n` for `n >= 2`. The task still uses the source problem's
  full definition `degree <= 146`, with nonzero integer coefficients.

## Hare and Hodges (2018; journal publication 2022)

Kevin G. Hare and Philip W. Hodges, *Applications of Integer and
Semi-Infinite Programming to the Integer Chebyshev Problem*, arXiv:1804.05985v2
(2018-10-26), later published in *Experimental Mathematics* (2022):
<https://arxiv.org/abs/1804.05985v2>.

- Section 1 recounts Meichsner's complete results through degree 145 and notes
  that many further degrees through 230 were known.
- Section 2.4 says the complete computations through degree 145 were followed
  by “many” results through degree 230. Section 2.5 lists 16 additional
  proved integer Chebyshev polynomials, starting at degree 147. The conclusion
  says 20 cases below 244 were still unknown, but does not enumerate them.
- Thus the finite n=146 status is specific but limited: the thesis row is
  explicitly one-sided and has no polynomial, and the later paper reports
  unresolved cases without naming the remaining degrees. No later n=146
  completion was found in the checked sources. This note does not claim that
  the 2018 paper names 146 in its unresolved list.

## Latest finite/asymptotic status checked

David Niedbala Giraudin, *New bounds for the integer Chebyshev constant of
`[0,1]`*, arXiv:2610.00386v3 (2026-10-12):
<https://arxiv.org/abs/2610.00386v3>.

This latest version proves new bounds on the limiting constant
`t_Z([0,1])`, using a degree-`2*10^10` upper-bound polynomial and a lower-bound
certificate. Its definitions and claims concern the limit as degree tends to
infinity; it does not claim a solution for the finite n=146 problem.

The 2018 paper is the latest source found in this search that gives finite
degree completion results. The 2026 version concerns the asymptotic constant.
No later finite-degree solution for n=146 was located. The exact remaining
degree set is not stated by the checked 2018 paper, so no stronger claim is
made.

## Reported bound in the raw task objective

Table 1.2 reports the reciprocal 146th-root lower bound `>=2.346298`. In the
task's raw objective this corresponds, using the printed decimal literally,
to the reported upper bound

`||P*_146||_[0,1] <= (1/(2346298/1000000))^146`.

This transformed value is recorded as a reported bound. The source decimal
presentation and the omitted n=146 witness have not been certified locally.
It is separate from the weaker reconstructed human-method baseline `h1^73`,
whose exact norm is `2^-146`.
