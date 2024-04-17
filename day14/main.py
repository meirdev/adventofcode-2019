import collections
import math
from typing import DefaultDict, NamedTuple, TypeAlias


class Chemical(NamedTuple):
    name: str
    quantity: int

    @classmethod
    def parse(cls, s: str) -> "Chemical":
        quantity, name = s.split(" ")

        return cls(name, int(quantity))


Reactions: TypeAlias = DefaultDict[Chemical, list[Chemical]]


def parse_input(input: str) -> Reactions:
    reactions: Reactions = collections.defaultdict(list)

    for line in input.strip().splitlines():
        a, b = line.split(" => ")

        reactions[Chemical.parse(b)].extend(map(Chemical.parse, a.split(", ")))

    return reactions


def calc_ore(
    reactions, target: str, target_amount: int, surplus: DefaultDict[str, int]
):
    if target == "ORE":
        return target_amount
    elif target_amount <= surplus[target]:
        surplus[target] -= target_amount
        return 0

    target_amount -= surplus[target]
    surplus[target] = 0
    ore = 0
    output_amount, inputs = reactions[target]
    copies = math.ceil(target_amount / output_amount)
    for input, input_amount in inputs:
        input_amount *= copies
        ore += calc_ore(reactions, input, input_amount, surplus)
    surplus[target] += output_amount * copies - target_amount

    return ore


def part1(input: str) -> int:
    reactions = parse_input(input)

    reactions_name_dict = {i.name: (i.quantity, reactions[i]) for i in reactions}

    return calc_ore(reactions_name_dict, "FUEL", 1, collections.defaultdict(int))


def part2(input: str) -> int:
    reactions = parse_input(input)

    reactions_name_dict = {i.name: (i.quantity, reactions[i]) for i in reactions}

    ore = 1000000000000
    target_amount = ore // calc_ore(
        reactions_name_dict, "FUEL", 1, collections.defaultdict(int)
    )
    fuel = 0
    surplus: DefaultDict[str, int] = collections.defaultdict(int)
    while ore and target_amount:
        new_surplus = collections.defaultdict(int, surplus)
        ore_used = calc_ore(reactions_name_dict, "FUEL", target_amount, new_surplus)
        if ore_used > ore:
            target_amount //= 2
        else:
            fuel += target_amount
            ore -= ore_used
            surplus = new_surplus
    return fuel


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
