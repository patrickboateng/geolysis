import pytest

from geolab import Kp
from geolab.bearing_capacity import M, T
from geolab.exceptions import FoundationTypeError


def test_Kp():
    assert Kp(30) == pytest.approx(3)


class TestT:
    """Tests for Terzaghi Bearing Capacity Theory."""

    def test_Nq(self):
        assert T.Nq(0) == pytest.approx(1.00)
        assert T.Nq(1) == pytest.approx(1.10)
        assert T.Nq(15) == pytest.approx(4.45)
        assert T.Nq(25) == pytest.approx(12.72)
        assert T.Nq(27) == pytest.approx(15.9)
        assert T.Nq(18.76) == pytest.approx(6.54)

    def test_Nc(self):
        assert T.Nc(0) == pytest.approx(5.70)
        assert T.Nc(1) == pytest.approx(6.00)
        assert T.Nc(15) == pytest.approx(12.86)
        assert T.Nc(25) == pytest.approx(25.13)
        assert T.Nc(27) == pytest.approx(29.24)
        assert T.Nc(18.76) == pytest.approx(16.21, 0.01)

    @pytest.mark.xfail
    def test_Ngamma(self):
        assert T.Ngamma(0) == pytest.approx(0.00)
        assert T.Ngamma(1) == pytest.approx(0.01)
        assert T.Ngamma(15) == pytest.approx(1.52)
        assert T.Ngamma(25) == pytest.approx(8.34)
        assert T.Ngamma(27) == pytest.approx(11.6)
        assert T.Ngamma(18.76) == pytest.approx(2.95)

    def test_terzaghi_qult(self):
        with pytest.raises(FoundationTypeError):
            T.qult(27, 28, 18, 1.2, 4, "rectangular")

    @pytest.mark.skip(reason="Not Implemented yet.")
    def test_terzaghi_qult_4_strip_footing(self):
        ...


class TestM:
    """Tests for Meyerhoff Bearing Capacity Theory."""

    @pytest.mark.skip(reason="Need to verify values")
    def test_Nq(self):
        assert M.Nq(0) == pytest.approx(1.00, 0.01)
        assert M.Nq(1) == pytest.approx(1.00, 0.01)
        assert M.Nq(2) == pytest.approx(1.20, 0.01)

    @pytest.mark.xfail
    def test_Nc(self):
        # assert M.Nc(0) == pytest.approx(5.14, 0.01)
        assert M.Nc(1) == pytest.approx(5.38, 0.01)
        assert M.Nc(2) == pytest.approx(5.63, 0.01)

    def test_Nq(self):
        assert M.Ngamma(0) == pytest.approx(0.00, 0.01)
        assert M.Ngamma(1) == pytest.approx(0.07, 0.01)
        assert M.Ngamma(2) == pytest.approx(0.15, 0.01)
