"""Exact checker for the 208-step nonnegative convolution objective."""
from fractions import Fraction
import math

def validate(solution, config, strict=False):
    del strict
    if not isinstance(solution, dict) or not isinstance(config, dict):
        raise ValueError("solution and config must be objects")
    params = config.get("parameters", config)
    if not isinstance(params, dict) or params.get("steps") != 208 or params.get("support") != ["-1/4", "1/4"] or params.get("nonnegative") is not True:
        raise ValueError("configuration must specify steps=208, support [-1/4,1/4], and nonnegative=true")
    coeff = solution.get("coefficients")
    if not isinstance(coeff, list) or len(coeff) != 208:
        raise ValueError("coefficients must contain exactly 208 rational values")
    values=[]
    for x in coeff:
        if isinstance(x, bool) or not isinstance(x, (int, float, str, Fraction)):
            raise ValueError("coefficients must be nonnegative rational integers or strings")
        if isinstance(x, float) and not math.isfinite(x):
            raise ValueError("coefficients must be finite")
        try: value=Fraction(str(x)) if isinstance(x, float) else Fraction(x)
        except (ValueError, ZeroDivisionError, TypeError): raise ValueError("coefficients must be finite rational values")
        if value < 0: raise ValueError("coefficients must be nonnegative")
        values.append(value)
    mass=sum(values, Fraction(0))
    if mass == 0: raise ValueError("coefficient mass must be positive")
    conv=[sum((values[i]*values[k-i] for i in range(max(0,k-207),min(207,k)+1)),Fraction(0)) for k in range(415)]
    peak=max(conv)
    objective=Fraction(416)*peak/(mass*mass)
    peak_idx=[i for i,x in enumerate(conv) if x==peak]
    return {"objective": str(objective), "verification_status":"exact", "details":{"steps":208,"coefficient_count":208,"max_convolution":"%s" % peak,"max_indices":peak_idx,"normalization":"normalized to integral 1 before scoring"}}
