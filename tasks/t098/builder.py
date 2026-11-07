"""Integer skyline reconstruction for the published Bouwkamp code format."""

import re


def parse_bouwkamp_line(line):
    main = line.split("*", 1)[0].strip()
    header = main.split(maxsplit=3)
    if len(header) != 4:
        raise ValueError("Bouwkamp code must contain order, width, height, and strip data")
    order, width, height = map(int, header[:3])
    strip_text = header[3]
    sizes = [int(value) for value in re.findall(r"\d+", strip_text)]
    if len(sizes) != order:
        raise ValueError("Bouwkamp code order does not match its square list")
    return order, width, height, sizes


def _normalize_segments(segments):
    out = []
    for x0, x1, height in segments:
        if x0 >= x1:
            continue
        if out and out[-1][1] == x0 and out[-1][2] == height:
            out[-1] = (out[-1][0], x1, height)
        else:
            out.append((x0, x1, height))
    return out


def _anchor(segments):
    lowest = min(height for _, _, height in segments)
    for x0, _, height in segments:
        if height == lowest:
            return x0, lowest
    raise ValueError("no empty skyline anchor remains")


def _flat_interval(segments, x, size, height):
    end = x + size
    position = x
    for x0, x1, filled in segments:
        if x1 <= position:
            continue
        if x0 > position or filled != height:
            return False
        position = min(x1, end)
        if position == end:
            return True
    return False


def _raise(segments, x, size, height):
    end = x + size
    out = []
    for x0, x1, old_height in segments:
        if x1 <= x or x0 >= end:
            out.append((x0, x1, old_height))
            continue
        if x0 < x:
            out.append((x0, x, old_height))
        out.append((max(x0, x), min(x1, end), height))
        if x1 > end:
            out.append((end, x1, old_height))
    return _normalize_segments(out)


def tile_bouwkamp_line(line):
    order, width, height, sizes = parse_bouwkamp_line(line)
    if order <= 0 or width <= 0 or height <= 0:
        raise ValueError("Bouwkamp code dimensions and order must be positive")
    skyline = [(0, width, 0)]
    squares = []
    at = 0
    while at < len(sizes):
        x0, y0 = _anchor(skyline)
        x = x0
        stop = at
        while stop < len(sizes):
            size = sizes[stop]
            if size <= 0 or x + size > width or y0 + size > height:
                break
            if not _flat_interval(skyline, x, size, y0):
                break
            x += size
            stop += 1
        if stop == at:
            raise ValueError("Bouwkamp strip cannot be placed on the current skyline")
        x = x0
        for size in sizes[at:stop]:
            squares.append([x, y0, size])
            skyline = _raise(skyline, x, size, y0 + size)
            x += size
        at = stop
    if skyline != [(0, width, height)] or len(squares) != order:
        raise ValueError("Bouwkamp code does not fill its outer rectangle")
    return {"side": width, "squares": squares}
