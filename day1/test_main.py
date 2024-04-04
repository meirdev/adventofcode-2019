from .main import part1, part2


def test_part1():
    for input, expected in (
        ("12", 2),
        ("14", 2),
        ("1969", 654),
        ("100756", 33583),
    ):
        assert part1(input) == expected


def test_part2():
    for input, expected in (
        ("14", 2),
        ("1969", 966),
        ("100756", 50346),
    ):
        assert part2(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 3381405
    assert part2(input) == 5069241
