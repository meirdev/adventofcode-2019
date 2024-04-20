import collections
import enum
import operator
import queue
from typing import Iterator, TypeAlias


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


class Output(enum.IntEnum):
    SCAFFOLD = ord("#")
    OPEN_SPACE = ord(".")
    UP = ord("^")
    DOWN = ord("v")
    LEFT = ord("<")
    RIGHT = ord(">")
    NEW_LINE = ord("\n")


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


class VM:
    def __init__(self, opcodes: list[int]) -> None:
        self._queue: queue.Queue[int] = queue.Queue()

        memory = collections.defaultdict(int)

        for i, val in enumerate(opcodes):
            memory[i] = val

        self._memory = memory
        self._relative_base = 0
        self._iter = iter(self)

    def __next__(self) -> int:
        return next(self._iter)

    def __iter__(self) -> Iterator[int]:
        memory = self._memory
        relative_base = self._relative_base

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
                memory[parameters[0]] = self._queue.get()

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

    def send(self, value: int) -> None:
        self._queue.put(value)


def part1(input: str) -> int:
    opcodes = parse_input(input)

    points = {}

    vm = VM(opcodes)

    y, x = 0, 0

    for i in vm:
        out = Output(i)

        if out == Output.NEW_LINE:
            y += 1
            x = 0
        else:
            points[y, x] = out

            x += 1

    return sum(
        y * x
        for y, x in points
        if all(
            points.get(i) == Output.SCAFFOLD
            for i in ((y, x), (y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))
        )
    )


def part2(input: str) -> int:
    pass


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
