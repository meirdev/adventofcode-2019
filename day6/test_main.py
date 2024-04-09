from .main import part1, part2


INPUT_PART_1 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

INPUT_PART_2 = """
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""


def test_part1():
    assert part1(INPUT_PART_1) == 42


def test_part2():
    assert part2(INPUT_PART_2) == 4


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 154386
    assert part2(input) == 346
