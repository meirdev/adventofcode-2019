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


class TileId(enum.IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4


class Joystick(enum.IntEnum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


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

    def __next__(self) -> int | None:
        return next(self._iter)

    def __iter__(self) -> Iterator[int | None]:
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
                yield None

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


def run_vm(input: str, free: bool = False) -> VM:
    opcodes = parse_input(input)

    if free:
        opcodes[0] = 2

    return VM(opcodes)


def part1(input: str) -> int:
    screen = {}

    for x, y, i in itertools.batched(run_vm(input), 3):
        if i is not None:
            screen[x, y] = TileId(i)

    return sum(1 for i in screen.values() if i == TileId.BLOCK)


def part2(input: str) -> int:
    vm = run_vm(input, True)

    ball_x = paddle_x = 0

    output = []

    result = -1

    for out in vm:
        if out is None:
            if ball_x > paddle_x:
                vm.send(1)
            elif ball_x < paddle_x:
                vm.send(-1)
            else:
                vm.send(0)
        else:
            output.append(out)

        if len(output) == 3:
            x, y, i = output

            if (x, y) == (-1, 0):
                result = i
            elif TileId(i) == TileId.HORIZONTAL_PADDLE:
                paddle_x = x
            elif TileId(i) == TileId.BALL:
                ball_x = x

            output = []

    return result


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
