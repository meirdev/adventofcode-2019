import itertools
import operator


def parse_input(input: str) -> list[int]:
    return list(map(int, input.strip().split(",")))


def intcode_computer(opcodes: list[int], values: tuple[int, int] | None) -> int:
    zero = opcodes[0]

    opcodes = opcodes[:]

    if values:
        opcodes[1:3] = values

    i = 0

    while i < len(opcodes):
        match opcodes[i]:
            case 1:
                op = operator.add
            case 2:
                op = operator.mul
            case 99:
                break

        try:
            opcodes[opcodes[i + 3]] = op(
                opcodes[opcodes[i + 1]], opcodes[opcodes[i + 2]]
            )
        except IndexError:
            break

        i += 4

        zero = opcodes[0]

    return zero


def part1(input: str, values: tuple[int, int] | None = (12, 2)) -> int:
    opcodes = parse_input(input)

    return intcode_computer(opcodes, values)


def part2(input: str) -> int:
    opcodes = parse_input(input)

    return next(
        100 * noun + verb
        for noun, verb in itertools.product(range(100), range(100))
        if intcode_computer(opcodes, (noun, verb)) == 19690720
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
