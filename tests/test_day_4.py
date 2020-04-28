import pytest
from aoc.day_4 import is_valid_password

@pytest.mark.parametrize('password, expect', [
    (122345, True),
    (12234, False),
    (223450, False),
    (123789, False),
    (112233, True),
    (123444, False),
    (111122, True)

])
def test_is_valid_password(password, expect):
    assert is_valid_password(password) == expect
