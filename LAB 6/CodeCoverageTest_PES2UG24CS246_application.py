import pytest

from bike_share_rental import ride_cost, dock_status, can_unlock


def test_ride_cost_valid_cases():
    assert ride_cost("standard", 30, False, False) == 20
    assert ride_cost("electric", 60, False, False) == 70
    assert ride_cost("cargo", 30, False, True) == 50
    assert ride_cost("standard", 30, True, False) == 0
    assert ride_cost("standard", 60, True, True) == 35
    assert ride_cost("standard", 31, True, False) == 20
    assert ride_cost("standard", 181, False, False) == 240


def test_ride_cost_invalid_cases():
    with pytest.raises(ValueError, match="unknown bike type"):
        ride_cost("mountain", 30, False, False)

    with pytest.raises(ValueError, match="invalid duration"):
        ride_cost("standard", 0, False, False)


def test_dock_status_valid_cases():
    assert dock_status(0, 10) == "empty"
    assert dock_status(10, 10) == "full"
    assert dock_status(1, 10) == "few bikes"
    assert dock_status(2, 10) == "few bikes"
    assert dock_status(8, 10) == "few slots"
    assert dock_status(9, 10) == "few slots"
    assert dock_status(5, 10) == "available"


def test_dock_status_invalid_cases():
    with pytest.raises(ValueError, match="invalid capacity"):
        dock_status(0, 0)

    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(-1, 10)

    with pytest.raises(ValueError, match="invalid bike count"):
        dock_status(11, 10)


def test_can_unlock_cases():
    assert can_unlock(500, True, 20) is False
    assert can_unlock(500, False, 15) is False
    assert can_unlock(99, False, 16) is False
    assert can_unlock(100, False, 17) is True
    assert can_unlock(49, False, 18) is False
    assert can_unlock(50, False, 18) is True
