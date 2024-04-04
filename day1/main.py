from typing import Callable, Iterator


def parse_input(input: str) -> list[int]:
    return list(map(int, input.strip().splitlines()))


def solution(input: str, fn: Callable[[Iterator[int]], int]):
    masses = parse_input(input)

    def calculate(val: int) -> Iterator[int]:
        while val > 0:
            yield max(0, val := val // 3 - 2)

    return sum(fn(calculate(mass)) for mass in masses)


def part1(input: str) -> int:
    return solution(input, next)


def part2(input: str) -> int:
    return solution(input, sum)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
