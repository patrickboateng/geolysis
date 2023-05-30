import pytest

from geolab import ERROR_TOLERANCE
from geolab.bearing_capacity.terzaghi import TerzaghiBCF

# from geolab.bearing_capacity.meyerhof import MBC

T_bearing_cap_factors = [
    (0, {"nq": 1.00, "nc": 5.7}),
    (1, {"nq": 1.10, "nc": 6.00}),
    (15, {"nq": 4.45, "nc": 12.86}),
    (25, {"nq": 12.72, "nc": 25.13}),
    (27, {"nq": 15.9, "nc": 29.24}),
    (18.76, {"nq": 6.54, "nc": 16.21}),
]
# M_ngamma = [(0, 0.0), (1, 0.07), (2, 0.15)]


class TestTerzaghi:
    @pytest.mark.parametrize("phi,exp", T_bearing_cap_factors)
    def test_bearing_capacity_factors(self, phi, exp):
        T = TerzaghiBCF(friction_angle=phi)
        assert T.nc() == pytest.approx(exp["nc"], ERROR_TOLERANCE)
        assert T.nq() == pytest.approx(exp["nq"], ERROR_TOLERANCE)


# class TestMeyerhoff:
#     """Tests for Meyerhoff Bearing Capacity Theory."""

#     @pytest.mark.skip(reason="Need to verify values")
#     def test_nq(self):
#         assert Meyerhoff.nq(0) == pytest.approx(1.00, 0.01)
#         assert Meyerhoff.nq(1) == pytest.approx(1.00, 0.01)
#         assert Meyerhoff.nq(2) == pytest.approx(1.20, 0.01)

#     @pytest.mark.xfail
#     def test_nc(self):
#         assert Meyerhoff.nc(0) == pytest.approx(5.14, 0.01)
#         assert Meyerhoff.nc(1) == pytest.approx(5.38, 0.01)
#         assert Meyerhoff.nc(2) == pytest.approx(5.63, 0.01)

#     @pytest.mark.parametrize("phi,exp", M_ngamma)
#     def test_ngamma(self, phi, exp):
#         assert Meyerhoff.ngamma(friction_angle=phi) == pytest.approx(
#             exp, ERROR_TOLERANCE
#         )
