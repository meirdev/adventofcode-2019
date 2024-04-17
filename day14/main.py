import collections
import math
from typing import DefaultDict, NamedTuple


class Chemical(NamedTuple):
    name: str
    quantity: int

    @classmethod
    def parse(cls, s: str) -> "Chemical":
        quantity, name = s.split(" ")

        return cls(name, int(quantity))


def parse_input(input: str) -> DefaultDict[Chemical, list[Chemical]]:
    chemicals: DefaultDict[Chemical, list[Chemical]] = collections.defaultdict(list)

    for line in input.strip().splitlines():
        a, b = line.split(" => ")

        chemicals[Chemical.parse(b)].extend(map(Chemical.parse, a.split(", ")))

    return chemicals


def part1(input: str) -> int:
    chemicals = parse_input(input)

    return -1


def part2(input: str) -> int:
    chemicals = parse_input(input)

    return -1


def main() -> None:
    with open("ex.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
