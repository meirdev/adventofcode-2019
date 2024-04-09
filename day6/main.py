import collections
from typing import Iterator


def parse_input(input: str) -> list[list[str]]:
    return [line.split(")") for line in input.strip().splitlines()]


def get_orbits(input: str) -> Iterator[list[str]]:
    orbits = parse_input(input)

    graph = collections.defaultdict(list)

    for a, b in orbits:
        graph[a].append(b)

    def rec(key: str, path: list[str]) -> Iterator[list[str]]:
        for i in graph[key]:
            i_path = path + [i]
            yield i_path
            yield from rec(i, i_path)

    yield from rec("COM", ["COM"])


def part1(input: str) -> int:
    return sum(len(i) - 1 for i in get_orbits(input))


def part2(input: str) -> int:
    transfers = {i[-1]: i for i in get_orbits(input) if i[-1] in ["YOU", "SAN"]}

    return next(
        (
            sum(map(len, transfers.values())) - (i + 1) * 2
            for i, (a, b) in enumerate(zip(transfers["YOU"], transfers["SAN"]))
            if a != b
        ),
        -1,
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
