"""Exact certificate checker for the Ovals variational problem."""
from __future__ import annotations

from fractions import Fraction
from math import comb
from pathlib import Path

import sympy as sp

CONFIG_ID = "T096-C01"
_EXPECTED = {
    "dimension": 2,
    "curve_class": "smooth strictly convex simple closed plane curves",
    "length": "2*pi",
    "objective": "minimize joint Rayleigh quotient over curve and nonzero periodic trial function",
}


def _q(x, label):
    if isinstance(x, bool) or isinstance(x, float):
        raise ValueError(f"{label} must be an exact rational string or integer")
    if type(x) is int:
        return Fraction(x)
    if not isinstance(x, str):
        raise ValueError(f"{label} must be an exact rational string or integer")
    try:
        q = Fraction(x)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label} is not a rational number") from exc
    return q


def _fourier(spec, label, *, positive_mean=False):
    if not isinstance(spec, dict) or set(spec) != {"constant", "cos", "sin"}:
        raise ValueError(f"{label} must have constant, cos, and sin arrays")
    c0 = _q(spec["constant"], f"{label}.constant")
    if not isinstance(spec["cos"], list) or not isinstance(spec["sin"], list):
        raise ValueError(f"{label} cosine and sine coefficients must be lists")
    if len(spec["cos"]) != len(spec["sin"]):
        raise ValueError(f"{label} cosine and sine arrays must have equal length")
    out = {0: (c0, Fraction(0))}
    for k, (a_raw, b_raw) in enumerate(zip(spec["cos"], spec["sin"]), 1):
        a, b = _q(a_raw, f"{label}.cos[{k-1}]"), _q(b_raw, f"{label}.sin[{k-1}]")
        # e^(ik theta) coefficient is (a - i b)/2; conjugate at -k.
        out[k] = (a/2, -b/2)
        out[-k] = (a/2, b/2)
    return {k: v for k, v in out.items() if v != (0, 0)}


def _add(a, b):
    out = dict(a)
    for k, (x, y) in b.items():
        u, v = out.get(k, (Fraction(0), Fraction(0)))
        out[k] = (u+x, v+y)
    return {k: v for k, v in out.items() if v != (0, 0)}


def _scale(a, s):
    return {k: (x*s, y*s) for k, (x, y) in a.items() if (x*s, y*s) != (0, 0)}


def _mul(a, b):
    out = {}
    for i, (x, y) in a.items():
        for j, (u, v) in b.items():
            p, q = out.get(i+j, (Fraction(0), Fraction(0)))
            out[i+j] = (p+x*u-y*v, q+x*v+y*u)
    return {k: v for k, v in out.items() if v != (0, 0)}


def _derivative(a):
    # d/dtheta (x+iy)e^(ik theta) = ik(x+iy)e^(ik theta).
    return {k: (-k*y, k*x) for k, (x, y) in a.items() if k != 0 and (x or y)}


def _mean(a):
    x, y = a.get(0, (Fraction(0), Fraction(0)))
    if y:
        raise ValueError("A real trigonometric expression has a non-real mean")
    return x


def _real(a, label):
    if a.get(0, (Fraction(0), Fraction(0)))[1]:
        raise ValueError(f"{label} has a non-real constant term")
    for k, (x, y) in a.items():
        if a.get(-k) != (x, -y):
            raise ValueError(f"{label} does not have conjugate-symmetric Fourier coefficients")


def _sym(q):
    return sp.Rational(q.numerator, q.denominator)


def _rho_numerator(spec, degree):
    """Return P(t) with rho(theta)=P(t)/(1+t^2)^degree, t=tan(theta/2)."""
    t = sp.symbols("t")
    A, B = 1-t*t, 2*t
    num = _sym(_q(spec["constant"], "rho.constant")) * (1+t*t)**degree
    for k, (a0, b0) in enumerate(zip(spec["cos"], spec["sin"]), 1):
        a, b = _sym(_q(a0, f"rho.cos[{k-1}]")), _sym(_q(b0, f"rho.sin[{k-1}]"))
        real = sp.Integer(0)
        imag = sp.Integer(0)
        for j in range(k+1):
            base = sp.binomial(k, j)*A**(k-j)*B**j
            if j % 2 == 0:
                real += (-1)**(j//2)*base
            else:
                imag += (-1)**((j-1)//2)*base
        num += (a*real+b*imag)*(1+t*t)**(degree-k)
    return sp.Poly(sp.cancel(num), t)


def _nonnegative_poly(poly):
    if poly.is_zero:
        return True
    if poly.LC() <= 0:
        return False
    # Exact Sturm counts detect real roots of each square-free rational factor.
    # An odd-multiplicity factor with a real root changes sign; even factors do not.
    _, factors = poly.sqf_list()
    for factor, multiplicity in factors:
        if multiplicity % 2 and factor.count_roots(-sp.oo, sp.oo):
            return False
    return True


def _series_upper(rho, f, delta, terms):
    # M bounds rho above by the Fourier coefficient l1 norm. Since rho>=delta,
    # u=1-rho/M lies in [0,1-delta/M], and the geometric tail is bounded exactly.
    spec_constant = rho[0][0]
    M = abs(spec_constant)
    degree = max((abs(k) for k in rho), default=0)
    for k in range(1, degree+1):
        x, y = rho.get(k, (Fraction(0), Fraction(0)))
        M += 2*(abs(x)+abs(y))
    if M <= 0 or delta > M:
        raise ValueError("Invalid upper or lower curvature-radius bound")
    q = 1-delta/M
    if q < 0:
        raise ValueError("Curvature-radius lower bound exceeds its upper bound")
    one = {0: (Fraction(1), Fraction(0))}
    u = _add(one, _scale(rho, -1/M))
    partial = dict(one)
    power = dict(one)
    for _ in range(terms):
        power = _mul(power, u)
        partial = _add(partial, power)
    reciprocal_upper = _scale(partial, 1/M)
    fprime = _derivative(f)
    potential = _add(_mul(fprime, fprime), _mul(f, f))
    numerator_lower = _mean(_mul(potential, reciprocal_upper))
    numerator_upper = numerator_lower + q**(terms+1)*_mean(potential)/delta
    denominator = _mean(_mul(_mul(f, f), rho))
    if denominator <= 0 or numerator_lower <= 0:
        raise ValueError("The Rayleigh quotient denominator or numerator is not positive")
    return numerator_lower/denominator, numerator_upper/denominator, M, q


def validate(solution, config, strict=False):
    if not isinstance(config, dict) or config.get("id") != CONFIG_ID:
        raise ValueError("Unknown T096 configuration")
    params = config.get("parameters")
    if (not isinstance(params, dict) or params.keys() != _EXPECTED.keys()
            or any(type(params[k]) is not type(v) or params[k] != v for k, v in _EXPECTED.items())):
        raise ValueError("T096 parameters do not match the fixed variational problem")
    if config.get("direction") != "minimize":
        raise ValueError("T096 is a minimization configuration")
    if not isinstance(solution, dict) or set(solution) - {"rho", "trial", "rho_lower_bound", "series_terms", "objective", "score", "claimed_score"}:
        raise ValueError("Candidate must provide rho, trial, rho_lower_bound, and series_terms")
    if not all(k in solution for k in ("rho", "trial", "rho_lower_bound", "series_terms")):
        raise ValueError("Candidate is missing its variational certificate")
    rho_spec, f_spec = solution["rho"], solution["trial"]
    rho = _fourier(rho_spec, "rho")
    f = _fourier(f_spec, "trial")
    _real(rho, "rho")
    _real(f, "trial")
    if _mean(rho) != 1:
        raise ValueError("The mean curvature radius must be one (length 2*pi)")
    if rho.get(1, (0, 0)) != (0, 0) or rho.get(-1, (0, 0)) != (0, 0):
        raise ValueError("The first Fourier harmonics of rho must vanish for curve closure")
    if not f:
        raise ValueError("The trial function must be nonzero")
    delta = _q(solution["rho_lower_bound"], "rho_lower_bound")
    if delta <= 0:
        raise ValueError("rho_lower_bound must be strictly positive")
    if type(solution["series_terms"]) is not int or solution["series_terms"] < 0:
        raise ValueError("series_terms must be a nonnegative integer")
    degree = max((abs(k) for k in rho), default=0)
    p = _rho_numerator(rho_spec, degree)
    t = p.gens[0]
    lower_poly = p - sp.Poly(_sym(delta)*(1+t*t)**degree, t)
    if not _nonnegative_poly(lower_poly):
        raise ValueError("The claimed rho lower bound is not certified on the full circle")
    lower, upper, M, q = _series_upper(rho, f, delta, solution["series_terms"])
    lower_value = f"{lower.numerator}/{lower.denominator}"
    value = f"{upper.numerator}/{upper.denominator}"
    return {
        "objective": value,
        "objective_value": value,
        "verification_status": "certified",
        "details": {
            "objective_interval": [lower_value, value],
            "objective_interval_meaning": "Certified interval for this trial Rayleigh quotient only; the reported objective is its conservative upper endpoint, not a two-sided interval for the first eigenvalue.",
            "rayleigh_quotient_upper_bound": value,
            "curvature_radius_lower_bound": f"{delta.numerator}/{delta.denominator}",
            "curvature_radius_upper_bound": f"{M.numerator}/{M.denominator}",
            "geometric_series_tail_ratio": f"{q.numerator}/{q.denominator}",
            "series_terms": solution["series_terms"],
            "curve_closure": "mean rho is one and first harmonics vanish exactly",
            "score_claims_ignored": True,
        },
    }
