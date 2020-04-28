import pytest
from aoc.day_3 import find_closest_intersect, find_earliest_intersect

@pytest.mark.parametrize('w1, w2, expect_dist', [
    (
        ['R8', 'U5', 'L5', 'D3'],
        ['U7', 'R6', 'D4', 'L4'],
        6
    ),
    (
        ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
        ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'],
        159
    ),
    (
        ['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
        ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'],
        135
    )
])
def test_find_closest_intersect(w1, w2, expect_dist):
    dist = find_closest_intersect(w1, w2)
    assert dist == expect_dist


@pytest.mark.parametrize('w1, w2, expect_steps', [
    (
        ['R8', 'U5', 'L5', 'D3'],
        ['U7', 'R6', 'D4', 'L4'],
        30
    ),
    (
        ['R75', 'D30', 'R83', 'U83', 'L12', 'D49', 'R71', 'U7', 'L72'],
        ['U62', 'R66', 'U55', 'R34', 'D71', 'R55', 'D58', 'R83'],
        610
    ),
    (
        ['R98', 'U47', 'R26', 'D63', 'R33', 'U87', 'L62', 'D20', 'R33', 'U53', 'R51'],
        ['U98', 'R91', 'D20', 'R16', 'D67', 'R40', 'U7', 'R15', 'U6', 'R7'],
        410
    )
])
def test_find_earliest_intersect(w1, w2, expect_steps):
    dist = find_earliest_intersect(w1, w2)
    assert dist == expect_steps