import itertools

WIDTH = 25
HEIGHT = 6


def parse_input(input: str) -> str:
    return input.strip()


def part1(input: str, width: int = WIDTH, height: int = HEIGHT) -> int:
    image = parse_input(input)

    _, layer = min(
        map(
            lambda layer: (layer.count("0"), layer),
            itertools.batched(image, width * height),
        ),
        key=lambda i: i[0],
    )

    return layer.count("1") * layer.count("2")


def part2(input: str, width: int = WIDTH, height: int = HEIGHT) -> str:
    image = parse_input(input)

    layers = reversed(
        list(
            map(
                lambda i: list(map(list, i)),
                itertools.batched(itertools.batched(image, width), height),
            )
        )
    )

    result = next(layers)

    for layer in layers:
        for h, row in enumerate(layer):
            for w, _ in enumerate(row):
                if layer[h][w] != "2":
                    result[h][w] = layer[h][w]

    return "\n" + "\n".join(
        "".join(["*" if i == "1" else " " for i in row]) for row in result
    )


def main() -> None:
    with open("input.txt") as file:
        input = file.read()

    print("Part 1:", part1(input))
    print("Part 2:", part2(input))


if __name__ == "__main__":
    main()
