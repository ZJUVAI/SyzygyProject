"""Decode the pinned public 537 certificate by Chen, Zhu, and Long."""

from pathlib import Path


def run_code():
    lines = (Path(__file__).parent / "data" / "chen_zhu_long_537_certificate.col").read_text().split()
    if len(lines) != 539:
        raise ValueError("certificate must contain a header and 537 color assignments")
    n, color_count = map(int, lines[:2])
    colors = [int(value) for value in lines[2:]]
    if n != 537 or color_count != 6 or len(colors) != n:
        raise ValueError("certificate header or assignment length does not match the pinned 537 witness")
    return {"n": n, "colors": colors}
