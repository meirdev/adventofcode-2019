import collections
import enum
import re


class Technique(enum.IntEnum):
    CUT = 0
    INC = 1
    NEW = 2


def parse_input(input: str) -> list[tuple[Technique, int | None]]:
    techniques: list[tuple[Technique, int | None]] = []

    for line in input.strip().splitlines():
        if match := re.match(r"cut (-?\d+)", line):
            techniques.append((Technique.CUT, int(match.group(1))))
        elif match := re.match(r"deal with increment (\d+)", line):
            techniques.append((Technique.INC, int(match.group(1))))
        elif line == "deal into new stack":
            techniques.append((Technique.NEW, None))
        else:
            raise ValueError(f"unknown: {line}")

    return techniques


def deck_shuffle(input: str, deck_size: int) -> list[int]:
    techniques = parse_input(input)

    cards = collections.deque(range(deck_size))

    for i in techniques:

        match i:
            case Technique.NEW, _:
                cards.reverse()
            case Technique.CUT, value:
                cards.rotate(value * -1)
            case Technique.INC, value:
                temp_cards = [None] * deck_size

                index = 0

                for _ in range(deck_size):
                    card = cards.popleft()

                    while temp_cards[index] is not None:
                        index = (index + value) % deck_size

                    temp_cards[index] = card

                cards = collections.deque(temp_cards)

    return list(cards)


def part1(input: str) -> int:
    cards = deck_shuffle(input, 10_007)

    return cards.index(2019)


def part2(input: str) -> int:
    techniques = parse_input(input)

    cards = 119315717514047
    repeats = 101741582076661

    inv = lambda n: pow(n, cards - 2, cards)
    get = lambda offset, increment, i: (offset + i * increment) % cards

    increment_mul = 1
    offset_diff = 0

    for i in techniques:
        match i:
            case Technique.NEW, _:
                increment_mul *= -1
                increment_mul %= cards
                offset_diff += increment_mul
                offset_diff %= cards
            case Technique.CUT, value:
                offset_diff += value * increment_mul
                offset_diff %= cards
            case Technique.INC, value:
                increment_mul *= inv(value)
                increment_mul %= cards

    def get_sequence(iterations: int) -> tuple[int, int]:
        increment = pow(increment_mul, iterations, cards)
        offset = offset_diff * (1 - increment) * inv((1 - increment_mul) % cards)
        offset %= cards
        return increment, offset

    increment, offset = get_sequence(repeats)
    return get(offset, increment, 2020)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
