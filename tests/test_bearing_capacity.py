import pytest

from geolab import Kp
from geolab.bearing_capacity import M, T, foundation_depth
from geolab.exceptions import FoundationTypeError

T_nq = [(0, 1.00), (1, 1.10), (15, 4.45), (25, 12.72), (27, 15.9), (18.76, 6.54)]
T_nc = [(0, 5.70), (1, 6.00), (15, 12.86), (25, 25.13), (27, 29.24), (18.76, 16.21)]
T_ngamma = [(0, 0.00), (1, 0.01), (15, 1.52), (25, 8.34), (27, 11.6), (18.76, 2.95)]


def test_Kp():
    assert Kp(phi=30) == pytest.approx(3)


def test_foundation():
    assert foundation_depth(350, 18, phi=35) == pytest.approx(1.429, 0.01)


class TestT:
    """Tests for Terzaghi Bearing Capacity Theory."""

    @pytest.mark.parametrize("phi,exp", T_nq)
    def test_Nq(self, phi, exp):
        assert T.Nq(phi=phi) == pytest.approx(exp)

    @pytest.mark.parametrize("phi,exp", T_nc)
    def test_Nc(self, phi, exp):
        assert T.Nc(phi=phi) == pytest.approx(exp, 0.01)

    @pytest.mark.xfail
    @pytest.mark.parametrize("phi,exp", T_ngamma)
    def test_Ngamma(self, phi, exp):
        assert T.Ngamma(phi=phi) == pytest.approx(exp)


#     def test_terzaghi_qult(self):
#         with pytest.raises(FoundationTypeError):
#             T.qult(27, 28, 18, 1.2, 4, "rectangular")

#     @pytest.mark.skip(reason="Not Implemented yet.")
#     def test_terzaghi_qult_4_strip_footing(self):
#         ...


# class TestM:
#     """Tests for Meyerhoff Bearing Capacity Theory."""

#     @pytest.mark.skip(reason="Need to verify values")
#     def test_Nq(self):
#         assert M.Nq(0) == pytest.approx(1.00, 0.01)
#         assert M.Nq(1) == pytest.approx(1.00, 0.01)
#         assert M.Nq(2) == pytest.approx(1.20, 0.01)

#     @pytest.mark.xfail
#     def test_Nc(self):
#         # assert M.Nc(0) == pytest.approx(5.14, 0.01)
#         assert M.Nc(1) == pytest.approx(5.38, 0.01)
#         assert M.Nc(2) == pytest.approx(5.63, 0.01)

#     def test_Nq(self):
#         assert M.Ngamma(0) == pytest.approx(0.00, 0.01)
#         assert M.Ngamma(1) == pytest.approx(0.07, 0.01)
#         assert M.Ngamma(2) == pytest.approx(0.15, 0.01)
