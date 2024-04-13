import collections
import itertools
import math


def parse_input(input: str) -> list[str]:
    return input.strip().splitlines()


def angle(start: tuple[int, int], end: tuple[int, int]) -> float:
    (x1, y1), (x2, y2) = start, end

    if (result := math.atan2(x2 - x1, y1 - y2) * 180 / math.pi) < 0:
        return 360 + result

    return result


def get_asteroids(input: str) -> set[tuple[int, int]]:
    asteroids_map = parse_input(input)

    return {
        (x, y)
        for y in range(len(asteroids_map))
        for x in range(len(asteroids_map[y]))
        if asteroids_map[y][x] == "#"
    }


def get_best_location(asteroids: set[tuple[int, int]]) -> tuple[tuple[int, int], int]:
    stations = collections.defaultdict(set)

    for a, b in itertools.permutations(asteroids, 2):
        stations[a].add(angle(a, b))

    result = max(stations, key=lambda i: len(stations[i]))

    return result, len(stations[result])


def part1(input: str) -> int:
    asteroids = get_asteroids(input)

    return get_best_location(asteroids)[1]


def part2(input: str) -> int:
    asteroids = get_asteroids(input)

    location, _ = get_best_location(asteroids)

    asteroids.remove(location)

    angles = sorted(
        ((angle(location, end), end) for end in asteroids),
        key=lambda x: (
            x[0],
            abs(location[0] - x[1][0]) + abs(location[1] - x[1][1]),
        ),
    )

    idx = 0
    last = angles.pop(idx)

    i = 1

    while i < 200:
        if last[0] == angles[idx][0]:
            idx += 1
            continue
        last = angles.pop(idx)
        i += 1

    return last[1][0] * 100 + last[1][1]


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
