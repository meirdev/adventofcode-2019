from .main import is_valid_password, part1, part2


def test_part1():
    for input, expected in (
        ("111111", True),
        ("223450", False),
        ("123789", False),
    ):
        assert is_valid_password(input, True) == expected


def test_part2():
    for input, expected in (
        ("112233", True),
        ("123444", False),
        ("111122", True),
    ):
        assert is_valid_password(input, False) == expected


def test_input():
    input = "145852-616942"

    assert part1(input) == 1767
    assert part2(input) == 1192
