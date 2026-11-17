"""Calculate scores from verified objectives and frozen references."""
import math
from fractions import Fraction


def score_result(checked, config, strict):
    objective = checked["objective"]
    numeric = checked.get("objective_value", objective)
    score_value = float(Fraction(numeric)) if isinstance(numeric, str) else float(numeric)
    if not math.isfinite(score_value) or score_value < 0:
        raise ValueError("Objective must be finite and nonnegative")
    reference = float(config["human_reference"])
    if not math.isfinite(reference) or reference <= 0:
        raise ValueError("Positive frozen human reference required")
    score = score_value / reference if config["direction"] == "maximize" else reference / score_value
    if not math.isfinite(score):
        raise ValueError("Non-finite score")
    certification = checked.get("verification_status", "numeric")
    if certification not in ("exact", "certified", "numeric"):
        raise ValueError("Unknown verification status")
    if strict and certification not in ("exact", "certified"):
        raise ValueError("Strict verification requires a certificate")
    return {
        "validity": 1.0,
        "combined_score": score,
        "objective": objective,
        "objective_value": numeric,
        "verification_status": certification,
        "details": checked.get("details", {}),
    }
