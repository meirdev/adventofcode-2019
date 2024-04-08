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
    HALT = 99


class Parameter(enum.IntEnum):
    A = 0
    B = 1
    C = 2


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


def intcode_computer(opcodes: list[int], input: str) -> Iterator[int]:
    opcodes = opcodes[:]

    i = 0

    is_immediate = lambda val: val == "1"

    while i < len(opcodes):
        opcode = str(opcodes[i]).zfill(5)

        """
        ABCDE

        DE - two-digit opcode,      02 == opcode 2
        C - mode of 1st parameter,  0 == position mode
        B - mode of 2nd parameter,  1 == immediate mode
        A - mode of 3rd parameter,  0 == position mode,
        """

        instruction = Op(int(opcode[3:]))

        if instruction in [Op.ADD, Op.MUL]:
            c = opcodes[i + 1] if is_immediate(opcode[Parameter.C]) else opcodes[opcodes[i + 1]]
            b = opcodes[i + 2] if is_immediate(opcode[Parameter.B]) else opcodes[opcodes[i + 2]]

            opcodes[opcodes[i + 3]] = OP_FN[instruction](c, b)

            i += 4
        elif instruction == Op.INPUT:
            opcodes[opcodes[i + 1]] = input

            i += 2
        elif instruction == Op.OUTPUT:
            c = opcodes[i + 1] if is_immediate(opcode[Parameter.C]) else opcodes[opcodes[i + 1]]

            yield c

            i += 2
        elif instruction in [Op.JUMP_IF_TRUE, Op.JUMP_IF_FALSE]:
            c = opcodes[i + 1] if is_immediate(opcode[Parameter.C]) else opcodes[opcodes[i + 1]]
            b = opcodes[i + 2] if is_immediate(opcode[Parameter.B]) else opcodes[opcodes[i + 2]]

            i = b if OP_FN[instruction](c, 0) else i + 3
        elif instruction in [Op.LESS_THEN, Op.EQUAL]:
            c = opcodes[i + 1] if is_immediate(opcode[Parameter.C]) else opcodes[opcodes[i + 1]]
            b = opcodes[i + 2] if is_immediate(opcode[Parameter.B]) else opcodes[opcodes[i + 2]]

            opcodes[opcodes[i + 3]] = OP_FN[instruction](c, b)

            i += 4
        elif instruction == Op.HALT:
            break


def solution(input: str, in_: int) -> int:
    opcodes = parse_input(input)

    return more_itertools.last(intcode_computer(opcodes, in_))


def part1(input: str) -> int:
    return solution(input, 1)


def part2(input: str) -> int:
    return solution(input, 5)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()