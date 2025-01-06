import pytest

from geolysis.utils import (
    PI,
    cos,
    cot,
    deg2rad,
    log10,
    rad2deg,
    sin,
    sqrt,
    tan,
)

ERROR_TOL = 0.01


def test_deg2rad():
    assert deg2rad(180) == pytest.approx(PI, ERROR_TOL)


def test_rad2deg():
    assert rad2deg(PI) == pytest.approx(180, ERROR_TOL)


def test_tan():
    assert tan(45) == pytest.approx(1, ERROR_TOL)


def test_cot():
    assert cot(60) == pytest.approx(0.577, ERROR_TOL)


def test_sin():
    assert sin(45) == pytest.approx(0.707, ERROR_TOL)


def test_cos():
    assert cos(45) == pytest.approx(0.707, ERROR_TOL)


def test_log():
    assert log10(10) == pytest.approx(1, ERROR_TOL)


def test_sqrt():
    assert sqrt(25) == pytest.approx(5, ERROR_TOL)
