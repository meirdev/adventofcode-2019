from .main import part1, part2


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 1876
    # CGPJCGCL
    assert part2(input) == "\n  ##   ##  ###    ##  ##   ##   ##  #      \n #  # #  # #  #    # #  # #  # #  # #      \n #    #    #  #    # #    #    #    #      \n #    # ## ###     # #    # ## #    #      \n #  # #  # #    #  # #  # #  # #  # #      \n  ##   ### #     ##   ##   ###  ##  ####   "
