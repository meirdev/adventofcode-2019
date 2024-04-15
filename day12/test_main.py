from .main import part1, part2


INPUT_1 = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

INPUT_2 = """
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""


def test_part1():
    assert part1(INPUT_1, 10) == 179
    assert part1(INPUT_2, 100) == 1940


def test_part2():
    assert part2(INPUT_1) == 2772
    assert part2(INPUT_2) == 4686774924


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 8287
    assert part2(input) == 528250271633772
