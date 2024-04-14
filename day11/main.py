import collections
import enum
import itertools
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


class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Color(enum.IntEnum):
    BLACK = 0
    WHITE = 1


class Turn(enum.IntEnum):
    LEFT = 0
    RIGHT = 1


Panel: TypeAlias = dict[tuple[int, int], Color]


FORWARD = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}


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
    opcodes: list[int], input: queue.Queue[int], relative_base: int = 0
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
            memory[parameters[0]] = input.get()

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


def solution(input: str, start: Color) -> Panel:
    opcodes = parse_input(input)

    panel: Panel = {}

    directions = collections.deque(Direction)

    y, x = 0, 0

    q: queue.Queue[int] = queue.Queue()
    q.put(start)

    steps = intcode_computer(opcodes, q)

    for color, turn in itertools.batched(steps, 2):
        panel[y, x] = Color(color)

        directions.rotate(1 if Turn(turn) == Turn.LEFT else -1)

        forward_y, forward_x = FORWARD[directions[0]]

        y += forward_y
        x += forward_x

        q.put(panel.get((y, x), Color.BLACK))

    return panel


def part1(input: str) -> int:
    return len(solution(input, Color.BLACK))


def part2(input: str) -> str:
    panel = solution(input, Color.WHITE)

    min_y, _ = min(panel, key=lambda i: i[0])
    _, min_x = min(panel, key=lambda i: i[1])
    max_y, _ = max(panel, key=lambda i: i[0])
    _, max_x = max(panel, key=lambda i: i[1])

    return "\n" + "\n".join(
        "".join(
            "#" if panel.get((y, x), Color.BLACK) == Color.WHITE else " "
            for x in range(min_x, max_x + 1)
        )
        for y in range(min_y, max_y + 1)
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
