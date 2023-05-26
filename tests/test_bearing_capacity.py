import pytest

from geolab import ERROR_TOLERANCE, passive_earth_pressure_coef
from geolab.bearing_capacity import Terzaghi, Meyerhoff
from geolab.estimators import foundation_depth

T_nq = [(0, 1.00), (1, 1.10), (15, 4.45), (25, 12.72), (27, 15.9), (18.76, 6.54)]
T_nc = [(0, 5.70), (1, 6.00), (15, 12.86), (25, 25.13), (27, 29.24), (18.76, 16.21)]
T_ngamma = [(0, 0.00), (1, 0.01), (15, 1.52), (25, 8.34), (27, 11.6), (18.76, 2.95)]
M_ngamma = [(0, 0.0), (1, 0.07), (2, 0.15)]


def test_Kp():
    assert passive_earth_pressure_coef(friction_angle=30) == pytest.approx(3)


def test_foundation_depth():
    assert foundation_depth(350, 18, friction_angle=35) == pytest.approx(
        1.429, ERROR_TOLERANCE
    )


class TestTerzaghi:
    @pytest.mark.parametrize("phi,exp", T_nq)
    def test_nq(self, phi, exp):
        assert Terzaghi.nq(friction_angle=phi) == pytest.approx(exp)

    @pytest.mark.parametrize("phi,exp", T_nc)
    def test_nc(self, phi, exp):
        assert Terzaghi.nc(friction_angle=phi) == pytest.approx(exp, ERROR_TOLERANCE)

    @pytest.mark.xfail
    @pytest.mark.parametrize("phi,exp", T_ngamma)
    def test_ngamma(self, phi, exp):
        assert Terzaghi.ngamma(friction_angle=phi) == pytest.approx(exp)


class TestMeyerhoff:
    """Tests for Meyerhoff Bearing Capacity Theory."""

    @pytest.mark.skip(reason="Need to verify values")
    def test_nq(self):
        assert Meyerhoff.nq(0) == pytest.approx(1.00, 0.01)
        assert Meyerhoff.nq(1) == pytest.approx(1.00, 0.01)
        assert Meyerhoff.nq(2) == pytest.approx(1.20, 0.01)

    @pytest.mark.xfail
    def test_nc(self):
        assert Meyerhoff.nc(0) == pytest.approx(5.14, 0.01)
        assert Meyerhoff.nc(1) == pytest.approx(5.38, 0.01)
        assert Meyerhoff.nc(2) == pytest.approx(5.63, 0.01)

    @pytest.mark.parametrize("phi,exp", M_ngamma)
    def test_ngamma(self, phi, exp):
        assert Meyerhoff.ngamma(friction_angle=phi) == pytest.approx(
            exp, ERROR_TOLERANCE
        )
