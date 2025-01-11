import pytest

from geolysis.utils import (pi, cos, cot, deg2rad, log10, rad2deg, sin, sqrt,
                            tan)

ERROR_TOL = 0.01


def test_deg2rad():
    assert deg2rad(180.0) == pytest.approx(pi, ERROR_TOL)


def test_rad2deg():
    assert rad2deg(pi) == pytest.approx(180.0, ERROR_TOL)


def test_tan():
    assert tan(45.0) == pytest.approx(1.0, ERROR_TOL)


def test_cot():
    assert cot(60.0) == pytest.approx(0.577, ERROR_TOL)


def test_sin():
    assert sin(45.0) == pytest.approx(0.707, ERROR_TOL)


def test_cos():
    assert cos(45.0) == pytest.approx(0.707, ERROR_TOL)


def test_log():
    assert log10(10.0) == pytest.approx(1.0, ERROR_TOL)


def test_sqrt():
    assert sqrt(25.0) == pytest.approx(5.0, ERROR_TOL)
