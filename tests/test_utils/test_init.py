import pytest

from geolysis.utils import (
    cosdeg,
    cotdeg,
    deg2rad,
    log10,
    pi,
    rad2deg,
    round_,
    sindeg,
    sqrt,
    tandeg,
)


def test_deg2rad():
    assert deg2rad(180.0) == pytest.approx(pi, 0.01)


def test_rad2deg():
    assert rad2deg(pi) == pytest.approx(180.0, 0.01)


def test_tan():
    assert tandeg(45.0) == pytest.approx(1.0, 0.01)


def test_cot():
    assert cotdeg(60.0) == pytest.approx(0.577, 0.01)


def test_sin():
    assert sindeg(45.0) == pytest.approx(0.707, 0.01)


def test_cos():
    assert cosdeg(45.0) == pytest.approx(0.707, 0.01)


def test_log():
    assert log10(10.0) == pytest.approx(1.0, 0.01)


def test_sqrt():
    assert sqrt(25.0) == pytest.approx(5.0, 0.01)


def test_round_():
    with pytest.raises(TypeError):
        round_(ndigits=2.0)
