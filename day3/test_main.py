from .main import part1, part2


INPUT = (
    (
        "R8,U5,L5,D3\nU7,R6,D4,L4",
        6,
        30,
    ),
    (
        "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83",
        159,
        610,
    ),
    (
        "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
        135,
        410,
    ),
)


def test_part1():
    for input, expected, _ in INPUT:
        assert part1(input) == expected


def test_part2():
    for input, _, expected in INPUT:
        assert part2(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 3229
    assert part2(input) == 32132
