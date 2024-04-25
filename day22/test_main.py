from .main import deck_shuffle, part1, part2


INPUT_1 = """
deal with increment 7
deal into new stack
deal into new stack
"""

INPUT_2 = """
cut 6
deal with increment 7
deal into new stack
"""

INPUT_3 = """
deal with increment 7
deal with increment 9
cut -2
"""

INPUT_4 = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""


def cards_shuffle():
    for input, expected in (
        (INPUT_1, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]),
        (INPUT_2, [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]),
        (INPUT_3, [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]),
        (INPUT_4, [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]),
    ):
        assert deck_shuffle(input, 10) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 6696
    assert part2(input) == 93750418158025
