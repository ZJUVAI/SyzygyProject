# T096: Benguria–Loss ovals problem

## Definition

For a smooth simple closed plane curve of length (2\pi), let (\kappa) be its curvature and let (\lambda_0(\gamma)) be the least periodic eigenvalue of

\[
H_\gamma=-\frac{d^2}{ds^2}+\kappa(s)^2.
\]

The target is (C_{\rm oval}=\inf_\gamma\lambda_0(\gamma)). Minimize this scalar. The unit circle has value 1. Benguria and Loss conjectured that (C_{\rm oval}=1).

The current source checked, Suragan's 2026 preprint, proves
\[
C_{\rm oval}\geq \frac{\sqrt\pi}{2}\left(\frac{\Gamma(7/6)}{\Gamma(5/3)}\right)^3\approx0.9618316523
\]
and states that the sharp lower bound remains open. This is a lower bound, not a feasible construction or a matching result.

## Exact finite certificates

Write the curve by its tangent angle \(\theta\) and set \(\rho(\theta)=ds/d\theta=1/\kappa(\theta)>0\). The curve closes and has length \(2\pi\) when the mean of \(\rho\) is 1 and its first sine and cosine coefficients vanish. Then
\[
\gamma'(\theta)=\rho(\theta)(\cos\theta,\sin\theta).
\]
For a real periodic trial function (f(\theta)\), its Rayleigh quotient is
\[
Q(\rho,f)=\frac{\int_0^{2\pi}(f'^2+f^2)/\rho\,d\theta}
{\int_0^{2\pi}f^2\rho\,d\theta}.
\]
It satisfies \(\lambda_0(\gamma)\leq Q(\rho,f)\). The search minimizes certified upper bounds on this joint Rayleigh quotient. The reported score is the upper endpoint; it is not claimed to be the first eigenvalue for a non-circle candidate.

The program accepts rational trigonometric polynomials for \(\rho\) and \(f\). This family preserves the full infimum. Positive smooth \(\rho\) can be approximated uniformly by Fejér trigonometric polynomials; this preserves the constant and first Fourier coefficients and preserves positivity for a sufficiently close approximation. Rational coefficient perturbations are dense while retaining those linear constraints. Periodic \(H^1\) trial functions are approximated in \(H^1\) by trigonometric polynomials, then by rational coefficients. Both numerator and positive denominator are continuous under these approximations. Denzler's existence and classification result supplies the remaining domain step: the relaxed minimizer is either the digon, with value 1, or an analytic strictly convex curve with positive curvature. Since the circle gives value 1, the strict positive-curvature family captures the global infimum.

The checker verifies the claimed lower bound \(\rho\geq\delta>0\) on the full circle. It changes variables with \(t=\tan(\theta/2)\), clears the positive denominator, and uses exact rational Sturm counts to prove the resulting polynomial is nonnegative on all real \(t\), including the limiting point at infinity. It bounds \(\rho\) above by the Fourier coefficient norm and encloses \(1/\rho\) with a finite geometric series plus an exact tail bound. All Fourier products, integrals, and final interval endpoints are rational. No floating-point tolerance or sampled angles certify a result.

## Baselines and status

The frozen human baseline is the unit circle. Its curvature is 1 and its constant eigenfunction has eigenvalue 1; the operator spectrum is \(1+k^2\), so this value is exact. The fixed reference replays the same analytic construction. The local search programs start at the circle and explore generated rational Fourier perturbations. They do not load reference data.

Sources:

- [Benguria and Loss (2004)](https://arxiv.org/abs/math-ph/0402048)
- [Denzler (arXiv:1301.6322; published 2015)](https://arxiv.org/abs/1301.6322)
- [Suragan, arXiv:2609.10775v1 (2026)](https://arxiv.org/html/2609.10775v1)

Source dates and scope notes are in `data/source/source_notes.json`. The task remains `accepted_by_sol`.
