from .main import part1, part2


def test_part1():
    for input, expected in (
        ("1,9,10,3,2,3,11,0,99,30,40,50", 3500),
        ("1,0,0,0,99", 2),
        ("2,3,0,3,99", 2),
        ("2,4,4,5,99,0", 2),
        ("1,1,1,4,99,5,6,0,99", 30),
    ):
        assert part1(input, None) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 9581917
    assert part2(input) == 2505
