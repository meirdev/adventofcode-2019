from .main import part1, part2


def test_part1():
    assert part1("12345678", 4) == "01029498"

    for input, expected in (
        ("80871224585914546619083218645595", "24176176"),
        ("19617804207202209144916044189917", "73745418"),
        ("69317163492948606335995924319873", "52432133"),
    ):
        assert part1(input) == expected


def test_part2():
    for input, expected in (
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ):
        assert part2(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == "44098263"
    assert part2(input) == "12482168"
