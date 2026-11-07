"""Rational Fourier candidates for the Ovals Rayleigh quotient."""
from __future__ import annotations

from fractions import Fraction


def circle():
    return {
        "rho": {"constant": "1", "cos": [], "sin": []},
        "trial": {"constant": "1", "cos": [], "sin": []},
        "rho_lower_bound": "1",
        "series_terms": 0,
    }


def oval(epsilon: Fraction, alpha: Fraction, beta: Fraction = Fraction(0), terms: int = 36):
    if not (0 < epsilon < 1):
        raise ValueError("epsilon must lie in (0,1)")
    ec, es = str(epsilon.numerator) + "/" + str(epsilon.denominator), str((1-epsilon).numerator) + "/" + str((1-epsilon).denominator)
    # rho=1+epsilon*cos(2 theta) has mean one, no first harmonic, and rho>=1-epsilon.
    return {
        "rho": {"constant": "1", "cos": ["0", ec], "sin": ["0", "0"]},
        "trial": {
            "constant": "1",
            "cos": [str(alpha.numerator)+"/"+str(alpha.denominator)],
            "sin": [str(beta.numerator)+"/"+str(beta.denominator)],
        },
        "rho_lower_bound": es,
        "series_terms": terms,
    }
