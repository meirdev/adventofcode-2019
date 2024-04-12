from .main import solution, part1, part2


def test_solution():
    assert next(solution("109,19,204,-34", -1, 2000)) == 0

    assert list(
        solution("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99", -1)
    ) == [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

    assert len(str(next(solution("1102, 34915192, 34915192, 7, 4, 7, 99, 0", -1)))) == 16

    assert list(solution("104,1125899906842624,99", -1)) == [1125899906842624]


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 3013554615
    assert part2(input) == 50158
