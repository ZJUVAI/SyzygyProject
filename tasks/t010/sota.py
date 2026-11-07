"""Generate the zero-extended Nordstrom–Robinson code from the octacode."""

OCTACODE_GENERATOR = (
    (1, 0, 0, 0, 3, 1, 2, 1),
    (0, 1, 0, 0, 1, 2, 3, 1),
    (0, 0, 1, 0, 3, 3, 3, 2),
    (0, 0, 0, 1, 2, 3, 1, 1),
)
GRAY_PAIR = (0b00, 0b01, 0b11, 0b10)


def nordstrom_robinson_words():
    """Return the 256 Gray images of the octacode words, as 16-bit masks."""
    words = []
    for message in range(4**4):
        coefficients = []
        value = message
        for _ in range(4):
            coefficients.append(value % 4)
            value //= 4
        quaternary = [
            sum(coefficients[row] * OCTACODE_GENERATOR[row][column]
                for row in range(4)) % 4
            for column in range(8)
        ]
        word = sum(GRAY_PAIR[symbol] << (2 * column)
                   for column, symbol in enumerate(quaternary))
        words.append(word)
    if len(set(words)) != 256:
        raise AssertionError("octacode enumeration did not produce 256 distinct words")
    return words


def run_code():
    import json, os
    from pathlib import Path
    config_id=os.environ.get('MATHBENCH_CONFIG_ID','T010-C01')
    if config_id in ('T010-C02','T010-C03'):
        filename={'T010-C02':'parity_extended_23_84_10.json','T010-C03':'parity_extended_25_196_10.json'}[config_id]
        data=json.loads((Path(__file__).parent/'data'/filename).read_text())
        return {'codewords':data['codewords']}
    if config_id != 'T010-C01': raise ValueError('unsupported configuration')
    # A zero coordinate preserves every distance, giving n=17, d=6.
    return {"codewords": [word << 1 for word in nordstrom_robinson_words()]}
