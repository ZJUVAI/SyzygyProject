"""Fixed 5905 public witness; not part of candidate initialization."""

from pathlib import Path


def run_code():
    path = Path(__file__).parent / "data" / "reference" / "public_5905_attachment.txt"
    return {"word": "".join(path.read_text(encoding="ascii").split())}
