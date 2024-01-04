import pytest

from geolysis.constants import ERROR_TOLERANCE
from geolysis.utils import (
    PI,
    cos,
    cot,
    deg2rad,
    log10,
    rad2deg,
    round_,
    sin,
    sqrt,
    tan,
)


def test_deg2rad():
    assert deg2rad(180) == pytest.approx(PI, ERROR_TOLERANCE)


def test_rad2deg():
    assert rad2deg(PI) == pytest.approx(180, ERROR_TOLERANCE)


def test_tan():
    assert tan(45) == pytest.approx(1, ERROR_TOLERANCE)


def test_cot():
    assert cot(60) == pytest.approx(0.577, ERROR_TOLERANCE)


def test_sin():
    assert sin(45) == pytest.approx(0.707, ERROR_TOLERANCE)


def test_cos():
    assert cos(45) == pytest.approx(0.707, ERROR_TOLERANCE)


def test_log():
    assert log10(10) == pytest.approx(1, ERROR_TOLERANCE)


def test_sqrt():
    assert sqrt(25) == pytest.approx(5, ERROR_TOLERANCE)


def test_round():
    with pytest.raises(TypeError):
        round_(ndigits=2.02)  # type: ignore
