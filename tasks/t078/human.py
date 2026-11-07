"""Rebuild the published Lambda_10 Gram matrix from Nebe's catalogue page."""

import os
from pathlib import Path
import re


def build_lambda10():
    path = Path(__file__).parent / "data/source/lambda10.html"
    page = path.read_text(encoding="latin-1")
    match = re.search(
        r'<a\s+NAME="GRAM"[^>]*>.*?</a><br>\s*10\s+10<br>(.*?)(?=<p><li>)',
        page,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match is None:
        raise ValueError("source page has no 10x10 GRAM section")
    text = re.sub(r"<[^>]*>", " ", match.group(1))
    numbers = [int(token) for token in re.findall(r"(?<![\w.])-?\d+(?![\w.])", text)]
    if len(numbers) < 100:
        raise ValueError("source GRAM section has fewer than 100 integer entries")
    flat = numbers[:100]
    return {"gram": [flat[i * 10 : (i + 1) * 10] for i in range(10)]}


def run_code():
    chosen = os.environ.get("MATHBENCH_CONFIG_ID", "T078-C01")
    if chosen != "T078-C01":
        raise ValueError(f"unsupported configuration: {chosen}")
    return build_lambda10()
