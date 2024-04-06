from typing import NamedTuple


class Point(NamedTuple):
    direction: tuple[int, int]
    steps: int


DIRECTIONS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1),
}


def parse_input(input: str) -> list[list[Point]]:
    return [
        list(
            map(
                lambda point: Point(DIRECTIONS[point[0]], int(point[1:])),
                line.split(","),
            )
        )
        for line in input.strip().splitlines()
    ]


def solution(input: str) -> dict[tuple[int, int], tuple[int, int]]:
    wires = parse_input(input)

    paths = []

    for wire in wires:
        x, y, steps = 0, 0, 0

        points: dict[tuple[int, int], int] = {}

        for point in wire:
            for _ in range(point.steps):
                x += point.direction[0]
                y += point.direction[1]
                steps += 1

                points[x, y] = points.get((x, y), steps)

        paths.append(points)

    return {i: (paths[0][i], paths[1][i]) for i in set(paths[0]) & set(paths[1])}


def part1(input: str) -> int:
    paths = solution(input)

    return min(map(lambda i: abs(i[0]) + abs(i[1]), paths))


def part2(input: str) -> int:
    paths = solution(input)

    return min(map(lambda i: paths[i][0] + paths[i][1], paths))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
