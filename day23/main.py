import collections
import enum
import operator
from typing import Iterator, Deque, TypeAlias

Packet: TypeAlias = tuple[int, int]


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


class VM:
    def __init__(self, opcodes: list[int]) -> None:
        self._input: Deque[int] = collections.deque()
        self._output: Deque[int] = collections.deque()

        memory = collections.defaultdict(int)

        for i, val in enumerate(opcodes):
            memory[i] = val

        self._memory = memory
        self._relative_base = 0
        self._iter = iter(self)

    def __next__(self) -> None:
        return next(self._iter)

    def __iter__(self) -> Iterator[None]:
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
                if len(self._input) == 0:
                    yield

                memory[parameters[0]] = self._input.popleft()

                i += 2
            elif instruction == Op.OUTPUT:
                self._output.append(memory[parameters[0]])

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

    @property
    def input(self) -> Deque[int]:
        return self._input

    @property
    def output(self) -> Deque[int]:
        return self._output


def solution(input: str) -> tuple[int, int]:
    opcodes = parse_input(input)

    vms: list[VM] = []

    for i in range(50):
        vm = VM(opcodes)
        vm.input.append(i)

        vms.append(vm)

    prev_nat: Packet | None = None
    nat: Packet | None = None

    first_packet: Packet | None = None

    while True:
        idle = True

        for vm in vms:
            if len(vm.input) == 0:
                vm.input.append(-1)
            else:
                idle = False

            next(vm)

            while vm.output:
                address = vm.output.popleft()
                x = vm.output.popleft()
                y = vm.output.popleft()

                if address == 255:
                    nat = (x, y)

                    if not first_packet:
                        first_packet = nat
                else:
                    vms[address].input.extend([x, y])

        if idle and nat:
            if nat and prev_nat and nat[1] == prev_nat[1] and first_packet:
                return first_packet[1], nat[1]

            vms[0].input.extend(nat)

            prev_nat = nat


def part1(input: str) -> int:
    return solution(input)[0]


def part2(input: str) -> int:
    return solution(input)[1]


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
