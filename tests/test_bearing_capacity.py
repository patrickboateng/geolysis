import pytest

from geolab import FoundationTypeError
from geolab.bearing_capacity import Kp, T, terzaghi_qult


def test_Kp():
    assert Kp(30) == pytest.approx(3)


def test_Nq():
    assert T.Nq(0) == pytest.approx(1.00)
    assert T.Nq(1) == pytest.approx(1.10)
    assert T.Nq(15) == pytest.approx(4.45)
    assert T.Nq(25) == pytest.approx(12.72)
    assert T.Nq(27) == pytest.approx(15.9)


def test_Nc():
    assert T.Nc(0) == pytest.approx(5.70)
    assert T.Nc(1) == pytest.approx(6.00)
    assert T.Nc(15) == pytest.approx(12.86)
    assert T.Nc(25) == pytest.approx(25.13)
    assert T.Nc(27) == pytest.approx(29.24)


@pytest.mark.xfail
def test_Ngamma():
    assert T.Ngamma(0) == pytest.approx(0.00)
    assert T.Ngamma(1) == pytest.approx(0.01)
    assert T.Ngamma(15) == pytest.approx(1.52)
    assert T.Ngamma(25) == pytest.approx(8.34)
    assert T.Ngamma(27) == pytest.approx(11.6)


def test_terzaghi_qult():
    with pytest.raises(FoundationTypeError):
        terzaghi_qult(27, 28, 18, 1.2, 4, "rectangular")

    # assert terzaghi_qult(16, 27, 18.5, 1.2, 1.715) == pytest.approx(1200)


@pytest.mark.skip(reason="Not Implemented yet.")
def test_terzaghi_qult_4_strip_footing():
    ...
