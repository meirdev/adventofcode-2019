import collections
import enum
import operator
from typing import Iterator

import more_itertools


class Op(enum.IntEnum):
    ADD = 1
    MUL = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THEN = 7
    EQUAL = 8
    ADJUST = 9
    HALT = 99


class Parameter(enum.IntEnum):
    A = 0
    B = 1
    C = 2


class ParameterMode(enum.StrEnum):
    POSITION = "0"
    IMMEDIATE = "1"
    RELATIVE = "2"


OP_FN = {
    Op.ADD: operator.add,
    Op.MUL: operator.mul,
    Op.JUMP_IF_TRUE: operator.ne,
    Op.JUMP_IF_FALSE: operator.eq,
    Op.LESS_THEN: operator.lt,
    Op.EQUAL: operator.eq,
}


def parse_input(input: str) -> list[int]:
    return list(map(int, input.strip().split(",")))


def intcode_computer(
    opcodes: list[int], input: int, relative_base: int = 0
) -> Iterator[int]:
    memory = collections.defaultdict(int)

    for i, val in enumerate(opcodes):
        memory[i] = val

    i = 0

    while i < len(memory):
        opcode = str(memory[i]).zfill(5)

        instruction = Op(int(opcode[3:]))

        parameters = []

        for param, rel in zip((Parameter.C, Parameter.B, Parameter.A), (1, 2, 3)):
            if opcode[param] == ParameterMode.IMMEDIATE:
                parameters.append(i + rel)
            elif opcode[param] == ParameterMode.RELATIVE:
                parameters.append(relative_base + memory[i + rel])
            elif opcode[param] == ParameterMode.POSITION:
                parameters.append(memory[i + rel])

        if instruction in [Op.ADD, Op.MUL]:
            memory[parameters[2]] = OP_FN[instruction](
                memory[parameters[0]], memory[parameters[1]]
            )

            i += 4
        elif instruction == Op.INPUT:
            memory[parameters[0]] = input

            i += 2
        elif instruction == Op.OUTPUT:
            yield memory[parameters[0]]

            i += 2
        elif instruction in [Op.JUMP_IF_TRUE, Op.JUMP_IF_FALSE]:
            i = (
                memory[parameters[1]]
                if OP_FN[instruction](memory[parameters[0]], 0)
                else i + 3
            )
        elif instruction in [Op.LESS_THEN, Op.EQUAL]:
            memory[parameters[2]] = int(
                OP_FN[instruction](memory[parameters[0]], memory[parameters[1]])
            )

            i += 4
        elif instruction == Op.ADJUST:
            relative_base += memory[parameters[0]]

            i += 2
        elif instruction == Op.HALT:
            break


def solution(input: str, in_: int, relative_base: int = 0) -> Iterator[int]:
    opcodes = parse_input(input)

    return intcode_computer(opcodes, in_, relative_base)


def part1(input: str) -> int:
    return more_itertools.last(solution(input, 1))


def part2(input: str) -> int:
    return more_itertools.last(solution(input, 2))


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
