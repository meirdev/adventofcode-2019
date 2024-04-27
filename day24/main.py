import copy
import enum
import itertools


class Type(enum.StrEnum):
    BUG = "#"
    EMPTY_SPACE = "."


def parse_input(input: str) -> list[list[Type]]:
    return [list(map(Type, row)) for row in input.strip().splitlines()]


def hash_layout(layout: list[list[Type]]) -> int:
    return hash(tuple(tuple(i) for i in layout))


def get_biodiversity_rating(layout: list[list[Type]]) -> int:
    return sum(
        2**i
        for i, type_ in enumerate(itertools.chain.from_iterable(layout))
        if type_ == Type.BUG
    )


def count_adjacent_bugs(layout: list[list[Type]], y: int, x: int) -> int:
    return sum(
        1
        for yi, xi in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))
        if 0 <= yi < len(layout)
        and 0 <= xi < len(layout[yi])
        and layout[yi][xi] == Type.BUG
    )


def part1(input: str) -> int:
    layout = parse_input(input)

    layouts = {hash_layout(layout)}

    while True:
        next_layout = copy.deepcopy(layout)

        for y in range(len(layout)):
            for x in range(len(layout[y])):
                bugs = count_adjacent_bugs(layout, y, x)

                if layout[y][x] == Type.BUG and bugs != 1:
                    next_layout[y][x] = Type.EMPTY_SPACE
                elif layout[y][x] == Type.EMPTY_SPACE and bugs in (1, 2):
                    next_layout[y][x] = Type.BUG

        next_layout_hash = hash_layout(next_layout)

        if next_layout_hash in layouts:
            return get_biodiversity_rating(next_layout)

        layouts.add(next_layout_hash)

        layout = next_layout


def part2(input: str):
    pass


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
