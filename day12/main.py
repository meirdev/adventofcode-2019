import dataclasses
import functools
import itertools
import math
import re
from typing import Iterator

import more_itertools


@dataclasses.dataclass
class Position:
    x: int
    y: int
    z: int


def parse_input(input: str) -> list[Position]:
    return [
        Position(*map(int, match))
        for match in re.findall(
            r"<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>", input
        )
    ]


def motion_dim(positions: list[int]) -> Iterator[tuple[list[int], list[int]]]:
    velocities = [0] * len(positions)

    first_state = tuple(velocities) + tuple(positions)

    while True:
        for a, b in itertools.combinations(range(len(positions)), 2):
            if positions[a] < positions[b]:
                velocities[a] += 1
                velocities[b] -= 1
            elif positions[a] > positions[b]:
                velocities[a] -= 1
                velocities[b] += 1

        for i in range(len(positions)):
            positions[i] += velocities[i]

        yield positions, velocities

        if first_state == tuple(velocities) + tuple(positions):
            break


def part1(input: str, steps: int = 1000) -> int:
    moons = parse_input(input)

    x = motion_dim([moon.x for moon in moons])
    y = motion_dim([moon.y for moon in moons])
    z = motion_dim([moon.z for moon in moons])

    _, *result = more_itertools.last(zip(range(steps), x, y, z))

    positions = list(zip(*(i[0] for i in result)))
    velocities = list(zip(*(i[1] for i in result)))

    return sum(
        sum(map(abs, positions[i])) * (sum(map(abs, velocities[i])))
        for i in range(len(positions))
    )


def part2(input: str) -> int:
    moons = parse_input(input)

    x = motion_dim([moon.x for moon in moons])
    y = motion_dim([moon.y for moon in moons])
    z = motion_dim([moon.z for moon in moons])

    return functools.reduce(
        lambda a, b: (a * b) // math.gcd(a, b),
        map(more_itertools.ilen, (x, y, z)),
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
