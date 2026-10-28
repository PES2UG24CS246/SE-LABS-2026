import pytest

from bike_share_rental import ride_cost, dock_status, can_unlock


@pytest.mark.parametrize("bike,minutes,subscriber,peak,expected", [
    ("standard", 30, False, False, 20),
    ("electric", 30, False, True, 50),
    ("cargo", 30, False, True, 50),
    ("standard", 181, False, False, 240),
    ("standard", 30, True, False, 0),
    ("standard", 60, True, True, 35),
    ("standard", 31, True, False, 20),
])
def test_ride_cost_branches(bike, minutes, subscriber, peak, expected):
    assert ride_cost(bike, minutes, subscriber, peak) == expected


@pytest.mark.parametrize("bike,minutes", [
    ("unknown", 30),
    ("standard", 0),
])
def test_ride_cost_errors(bike, minutes):
    with pytest.raises(ValueError):
        ride_cost(bike, minutes, False, False)


@pytest.mark.parametrize("bikes,capacity,expected", [
    (0, 10, "empty"),
    (10, 10, "full"),
    (1, 10, "few bikes"),
    (2, 10, "few bikes"),
    (8, 10, "few slots"),
    (9, 10, "few slots"),
    (5, 10, "available"),
])
def test_dock_status_branches(bikes, capacity, expected):
    assert dock_status(bikes, capacity) == expected


@pytest.mark.parametrize("bikes,capacity", [
    (0, 0),
    (-1, 10),
    (11, 10),
])
def test_dock_status_errors(bikes, capacity):
    with pytest.raises(ValueError):
        dock_status(bikes, capacity)


@pytest.mark.parametrize("balance,active,age,expected", [
    (500, True, 20, False),
    (500, False, 15, False),
    (99, False, 16, False),
    (100, False, 17, True),
    (49, False, 18, False),
    (50, False, 18, True),
])
def test_can_unlock_branches(balance, active, age, expected):
    assert can_unlock(balance, active, age) is expected
