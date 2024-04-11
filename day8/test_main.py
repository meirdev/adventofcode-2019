import textwrap

from .main import part1, part2


def test_part1():
    assert part1("123456789012", 3, 2) == 1


def test_part2():
    assert part2("0222112222120000", 2, 2) == "\n *\n* "


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 2159
    # CJZHR
    assert part2(input) == "\n **    ** **** *  * ***  \n*  *    *    * *  * *  * \n*       *   *  **** *  * \n*       *  *   *  * ***  \n*  * *  * *    *  * * *  \n **   **  **** *  * *  * "
