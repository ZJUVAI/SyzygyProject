"""Example only: a fixed-length list of distinct positive integers."""


def validate(solution, config, strict=False):
    values = solution["values"]
    if not isinstance(values, list) or len(values) != config["parameters"]["size"]:
        raise ValueError("Wrong list size")
    if any(type(value) is not int or value <= 0 for value in values):
        raise ValueError("Positive integers required")
    if len(set(values)) != len(values):
        raise ValueError("Repeated elements")
    return {"objective": sum(values), "verification_status": "exact"}
