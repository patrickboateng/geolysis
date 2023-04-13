import pytest

from geolab.bearing_capacity import Nq, Ngamma, Nc, Kp


def test_Kp():
    assert Kp(30) == pytest.approx(3)


def test_Nq():
    assert Nq(0) == pytest.approx(1.00)
    assert Nq(1) == pytest.approx(1.10)
    assert Nq(15) == pytest.approx(4.45)
    assert Nq(25) == pytest.approx(12.72)


def test_Ngamma():
    assert Ngamma(0) == pytest.approx(0.00)
    # assert Ngamma(1) == pytest.approx(0.01)
    assert Ngamma(15) == pytest.approx(1.52)
    assert Ngamma(25) == pytest.approx(8.34)


def test_Nc():
    assert Nc(0) == pytest.approx(5.70)
    # assert Nc(1) == pytest.approx(6.00)
    # assert Nc(15) == pytest.approx(12.86)
    assert Nc(25) == pytest.approx(25.13)
