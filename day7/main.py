import collections
import enum
import itertools
import operator
import queue
from typing import Iterator


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


class ParameterMode(enum.StrEnum):
    POSITION = "0"
    IMMEDIATE = "1"


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
        self._iter = iter(self)

    def __next__(self) -> int:
        return next(self._iter)

    def __iter__(self) -> Iterator[int]:
        memory = self._memory

        i = 0

        while i < len(memory):
            opcode = str(memory[i]).zfill(5)

            instruction = Op(int(opcode[3:]))

            parameters = []

            for param, rel in zip((Parameter.C, Parameter.B, Parameter.A), (1, 2, 3)):
                if opcode[param] == ParameterMode.IMMEDIATE:
                    parameters.append(i + rel)
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
            elif instruction == Op.HALT:
                break

    def send(self, value: int) -> None:
        self._queue.put(value)


def solution(input: str, part: int) -> int:
    opcodes = parse_input(input)

    if part == 1:
        settings = range(5)
    else:
        settings = range(5, 10)

    max_signal = 0

    for setting in itertools.permutations(settings):
        vms: list[VM] = []

        second_input = 0

        for i in setting:
            vm = VM(opcodes)
            vm.send(i)
            vm.send(second_input)
            vms.append(vm)

            second_input = next(vm)

        if part == 1:
            max_signal = max(max_signal, second_input)
        else:
            for vm in itertools.cycle(vms):
                try:
                    vm.send(second_input)
                    second_input = next(vm)
                except StopIteration:
                    if vm is vms[-1]:
                        max_signal = max(max_signal, second_input)
                        break

    return max_signal


def part1(input: str) -> int:
    return solution(input, 1)


def part2(input: str) -> int:
    return solution(input, 2)


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
