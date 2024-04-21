from .main import part1, part2


INPUT_1 = """
#########
#b.A.@.a#
#########
"""

INPUT_2 = """
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""

INPUT_3 = """
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
"""

INPUT_4 = """
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""

INPUT_5 = """
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""

def test_part1():
    for input, expected in (
        (INPUT_1, 8),
        (INPUT_2, 86),
        (INPUT_3, 132),
        (INPUT_4, 136),
        (INPUT_5, 81),
    ):
        assert part1(input) == expected


def test_input():
    with open("input.txt") as file:
        input = file.read()

    assert part1(input) == 4954
    assert part2(input) == 2334