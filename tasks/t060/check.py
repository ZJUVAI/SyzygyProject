"""Exact checker for integer-complexity expression trees at M61."""

TARGET = 2**61 - 1
CONFIG_ID = "T060-C01"
MAX_EXPRESSION_LENGTH = 100_000


def _selfridge_max(k):
    """Largest integer representable with at most k ones (Selfridge)."""
    if k == 1:
        return 1
    q, r = divmod(k, 3)
    if r == 0:
        return 3**q
    if r == 1:
        return 4 * 3 ** (q - 1)
    return 2 * 3**q


def _parse(expression):
    if not isinstance(expression, str):
        raise ValueError("expression must be a string")
    if not expression or len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("expression is empty or too long")

    # Shunting-yard evaluation with explicit stacks avoids Python recursion limits.
    values = []
    operators = []
    expect_operand = True
    depth = 0
    count_ones = 0

    def apply():
        if len(values) < 2 or not operators or operators[-1] not in ("+", "*"):
            raise ValueError("malformed expression")
        op = operators.pop()
        right = values.pop()
        left = values.pop()
        values.append(left + right if op == "+" else left * right)

    precedence = {"+": 1, "*": 2}
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch == " ":
            i += 1
            continue
        if ch == "1":
            if not expect_operand:
                raise ValueError("missing operator")
            values.append(1)
            count_ones += 1
            expect_operand = False
        elif ch == "(":
            if not expect_operand:
                raise ValueError("missing operator before parenthesis")
            operators.append(ch)
            depth += 1
            expect_operand = True
        elif ch == ")":
            if expect_operand or depth == 0:
                raise ValueError("unmatched or empty parenthesis")
            while operators and operators[-1] != "(":
                apply()
            if not operators:
                raise ValueError("unmatched closing parenthesis")
            operators.pop()
            depth -= 1
            expect_operand = False
        elif ch in precedence:
            if expect_operand:
                raise ValueError("operator without a left operand")
            while (operators and operators[-1] in precedence
                   and precedence[operators[-1]] >= precedence[ch]):
                apply()
            operators.append(ch)
            expect_operand = True
        else:
            raise ValueError("only 1, +, *, parentheses, and ASCII spaces are allowed")
        i += 1

    if expect_operand or depth:
        raise ValueError("incomplete expression")
    while operators:
        if operators[-1] == "(":
            raise ValueError("unmatched opening parenthesis")
        apply()
    if len(values) != 1 or count_ones == 0:
        raise ValueError("malformed expression")
    return values[0], count_ones


def _check_config(config):
    if not isinstance(config, dict):
        raise ValueError("configuration must be an object")
    cid = config.get("id", CONFIG_ID)
    params = config.get("parameters", config)
    if cid != CONFIG_ID or not isinstance(params, dict):
        raise ValueError("unsupported T060 configuration")
    if params.get("target", "2^61-1") != "2^61-1":
        raise ValueError("configuration target must be M61")
    if params.get("target_value", str(TARGET)) != str(TARGET):
        raise ValueError("configuration target value must equal M61")


def validate(solution, config, strict=False):
    _check_config(config)
    if not isinstance(solution, dict):
        raise ValueError("solution must be an object")
    value, ones = _parse(solution.get("expression"))
    if value != TARGET:
        raise ValueError("expression does not evaluate to M61")
    return {
        "objective": ones,
        "verification_status": "exact",
        "details": {
            "target": str(TARGET),
            "expression_value": str(value),
            "ones_count": ones,
            "expression_tree": True,
            "certified_lower_bound": 116,
            "selfridge_max_at_115": str(_selfridge_max(115)),
            "claimed_objective_ignored": True,
        },
    }
