import pytest

from geolysis.core.constants import ERROR_TOL
from geolysis.core.foundation import Shape, create_foundation
from geolysis.core.ubc import (
    TerzaghiBCF,
    TerzaghiUBC4CircFooting,
    TerzaghiUBC4RectFooting,
    TerzaghiUBC4SquareFooting,
    TerzaghiUBC4StripFooting,
)


class TestTerzaghiBCF:
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


class TestTerzaghiUBC4StripFooting:

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


class TestTerzaghiUBC4SquareFooting:
    def test_bearing_capacity(self):
        fs = create_foundation(
            depth=1.0,
            thickness=0.3,
            width=2.0,
            footing_shape=Shape.SQUARE,
        )
        t = TerzaghiUBC4SquareFooting(
            soil_friction_angle=25,
            cohesion=15,
            unit_wgt=18,
            foundation_size=fs,
            local_shear_failure=True,
        )
        assert t.bearing_capacity() == pytest.approx(323.008, ERROR_TOL)


class TestTerzaghiUBC4CircFooting:
    def test_bearing_capacity(self):
        fs = create_foundation(
            depth=1.0,
            thickness=0.3,
            width=2.3,
            footing_shape=Shape.CIRCLE,
        )
        t = TerzaghiUBC4CircFooting(
            soil_friction_angle=25,
            cohesion=15,
            unit_wgt=18,
            foundation_size=fs,
            local_shear_failure=True,
        )
        assert t.bearing_capacity() == pytest.approx(318.9094, ERROR_TOL)


class TestTerzaghiUBC4RectFooting:
    def test_bearing_capacity(self):
        fs = create_foundation(
            depth=1.0,
            thickness=0.3,
            width=1.5,
            length=2.5,
            footing_shape=Shape.RECTANGLE,
        )
        t = TerzaghiUBC4RectFooting(
            soil_friction_angle=25,
            cohesion=15,
            unit_wgt=18,
            foundation_size=fs,
            local_shear_failure=True,
        )
        assert t.bearing_capacity() == pytest.approx(300.0316, ERROR_TOL)
