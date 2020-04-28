import pytest
from aoc.day_1 import calc_fuel_req, calc_fuel_req_adjusted


@pytest.mark.parametrize('mass,expected_fuel_req', [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583)
])
def test_calc_fuel_req(mass, expected_fuel_req):
    assert calc_fuel_req(mass) == expected_fuel_req


@pytest.mark.parametrize('mass,expected_fuel_req', [
    (14, 2),
    (1969, 966),
    (100756, 50346)
])
def test_calc_fuel_req_adjusted(mass, expected_fuel_req):
    assert calc_fuel_req_adjusted(mass) == expected_fuel_req