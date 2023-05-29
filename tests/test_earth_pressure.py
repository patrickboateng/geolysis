import pytest

from geolab.earth_pressure import passive_earth_pressure_coef as kp


def test_Kp():
    assert kp(friction_angle=30) == pytest.approx(3)
