import pytest

from geolysis.utils import (cos, cot, deg2rad, log10, pi, rad2deg,
                            sin, sqrt, tan, round_)


def test_deg2rad():
    assert deg2rad(180.0) == pytest.approx(pi, 0.01)


def test_rad2deg():
    assert rad2deg(pi) == pytest.approx(180.0, 0.01)


def test_tan():
    assert tan(45.0) == pytest.approx(1.0, 0.01)


def test_cot():
    assert cot(60.0) == pytest.approx(0.577, 0.01)


def test_sin():
    assert sin(45.0) == pytest.approx(0.707, 0.01)


def test_cos():
    assert cos(45.0) == pytest.approx(0.707, 0.01)


def test_log():
    assert log10(10.0) == pytest.approx(1.0, 0.01)


def test_sqrt():
    assert sqrt(25.0) == pytest.approx(5.0, 0.01)


def test_round():
    with pytest.raises(TypeError):
        round_(ndigits=2.0)
