import itertools


BASE_PATTERN = [0, 1, 0, -1]


def parse_input(input: str) -> str:
    return input.strip()


def generate_pattern(position: int):
    it = itertools.cycle(
        itertools.chain.from_iterable([i] * position for i in BASE_PATTERN)
    )

    next(it)

    return it


def part1(input: str, phases: int = 100) -> str:
    input_number = parse_input(input)

    for _ in range(phases):
        input_number = "".join(
            str(
                abs(
                    sum(
                        map(
                            lambda k: int(k[0]) * k[1],
                            zip(input_number, generate_pattern(i + 1)),
                        )
                    )
                )
                % 10
            )
            for i in range(len(input_number))
        )

    return input_number[:8]


def part2(input: str) -> str:
    input_number = parse_input(input)

    input_number_list = list(
        map(int, (input_number * 10_000)[int(input_number[:7]) :][::-1])
    )

    for _ in range(100):
        input_number_list = list(
            itertools.accumulate(input_number_list, lambda a, b: (a + b) % 10)
        )

    return "".join(map(str, input_number_list[::-1][:8]))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
