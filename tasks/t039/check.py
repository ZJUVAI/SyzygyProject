"""Exact checker for a seven-row difference triangle set."""


def validate(solution, config, strict=False):
    parameters = config.get("parameters", {}) if isinstance(config, dict) else {}
    row_count = parameters.get("rows")
    marks_per_row = parameters.get("marks_per_row")
    if type(row_count) is not int or row_count < 1:
        raise ValueError("configuration rows must be a positive integer")
    if type(marks_per_row) is not int or marks_per_row < 2:
        raise ValueError("configuration marks_per_row must be an integer >= 2")
    rows = solution.get("rows") if isinstance(solution, dict) else solution
    if not isinstance(rows, (list, tuple)) or len(rows) != row_count:
        raise ValueError(f"solution must contain exactly {row_count} rows")

    differences = set()
    spans = []
    checked = 0
    for row_index, row in enumerate(rows):
        if not isinstance(row, (list, tuple)) or len(row) != marks_per_row:
            raise ValueError(f"row {row_index} must contain exactly {marks_per_row} marks")
        if any(type(mark) is not int for mark in row):
            raise ValueError("marks must be integers; booleans are not accepted")
        if any(mark < 0 for mark in row):
            raise ValueError("marks must be nonnegative integers")
        ordered = sorted(row)
        if len(set(ordered)) != marks_per_row:
            raise ValueError(f"marks in row {row_index} must be distinct")
        span = ordered[-1] - ordered[0]
        spans.append(span)
        for i, left in enumerate(ordered):
            for right in ordered[i + 1:]:
                difference = right - left
                if difference in differences:
                    raise ValueError("positive within-row differences must be globally distinct")
                differences.add(difference)
                checked += 1

    return {
        "objective": max(spans),
        "verification_status": "exact",
        "details": {
            "rows": row_count,
            "marks_per_row": marks_per_row,
            "within_row_differences_checked": checked,
            "distinct_differences": len(differences),
            "row_spans": spans,
        },
    }
