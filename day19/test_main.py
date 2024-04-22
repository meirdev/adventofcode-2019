from .main import part1, part2


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 220
    assert part2(input) == 10010825
