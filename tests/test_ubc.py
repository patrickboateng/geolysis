import pytest

from geolysis.core.constants import ERROR_TOL
from geolysis.core.foundation import Shape, create_foundation
from geolysis.core.ubc import TerzaghiBCF, TerzaghiUBC4StripFooting


class TestTerzaghiUBC4StripFooting:

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 5.70), (10, 9.61), (20, 17.69), (35, 57.8))
    )
    def test_n_c(self, f_angle, r_value):
        t_bcf = TerzaghiBCF(f_angle)
        assert t_bcf.n_c == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 1.00), (10, 2.69), (20, 7.44), (35, 41.44))
    )
    def test_n_q(self, f_angle, r_value):
        t_bcf = TerzaghiBCF(f_angle)
        assert t_bcf.n_q == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 0.00), (10, 0.42), (20, 3.42), (35, 46.52))
    )
    def test_n_gamma(self, f_angle, r_value):
        t_bcf = TerzaghiBCF(f_angle)
        assert t_bcf.n_gamma == pytest.approx(r_value, ERROR_TOL)

    def test_bearing_capacity(self):
        fs = create_foundation(
            depth=1,
            thickness=0.3,
            width=1.2,
            footing_shape=Shape.STRIP,
        )
        t = TerzaghiUBC4StripFooting(
            soil_friction_angle=35,
            cohesion=15,
            unit_wgt=18,
            foundation_size=fs,
        )
        assert t.bearing_capacity() == pytest.approx(2114.586, ERROR_TOL)
