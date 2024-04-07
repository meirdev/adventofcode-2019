import itertools
import operator


def parse_input(input: str) -> tuple[int, int]:
    return tuple(map(int, input.split("-")))


def is_valid_password(password: str, same_ge_one: int) -> bool:
    if same_ge_one:
        op = operator.ge
    else:
        op = operator.eq

    c1 = all(a <= b for a, b in itertools.pairwise(password))
    c2 = False

    i = 0
    while i < len(password):
        same = sum(1 for j in range(i + 1, len(password)) if password[i] == password[j])
        if op(same, 1):
            c2 = True
        i += 1 + same

    return c1 and c2


def solution(input: str, same_ge_one: bool) -> int:
    min_, max_ = parse_input(input)

    return sum(
        map(
            lambda password: is_valid_password(password, same_ge_one),
            map(str, range(min_, max_ + 1)),
        )
    )


def part1(input: str) -> int:
    return solution(input, True)


def part2(input: str) -> int:
    return solution(input, False)


def main() -> None:
    input = "145852-616942"

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
