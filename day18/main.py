import enum
import string


class Type(enum.StrEnum):
    ENTRANCE = "@"
    OPEN_PASSAGE = "."
    STONE_WALL = "#"
    KEY = "x"
    DOOR = "X"


TYPE = {
    "@": Type.ENTRANCE,
    ".": Type.OPEN_PASSAGE,
    "#": Type.STONE_WALL,
    **{i: Type.KEY for i in string.ascii_lowercase},
    **{i: Type.DOOR for i in string.ascii_uppercase},
}


def parse_input(input: str) -> dict[tuple[int, int], str]:
    rows = input.strip().splitlines()

    return {(y, x): col for y, row in enumerate(rows) for x, col in enumerate(row)}


def part1(input: str) -> int:
    return -1


def part2(input: str) -> int:
    return -1


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
