import unittest

import pytest

from src._config.config import Quantity, UnitReg
from src.bearing_capacity.ubc_4_soils import SoilProperties
from src.bearing_capacity.ubc_4_soils.terzaghi_ubc import (
    TerzaghiBearingCapacityFactor,
    TerzaghiUBC4CircFooting,
    TerzaghiUBC4RectFooting,
    TerzaghiUBC4SquareFooting,
    TerzaghiUBC4StripFooting,
)
from src.foundation import Shape, create_foundation
from src.utils import INF

ERROR_TOL = 0.01


class TestTerzaghiBCF:
    @classmethod
    def setup_class(cls):
        cls.t_bcf = TerzaghiBearingCapacityFactor()

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 5.70), (10, 9.61), (20, 17.69), (35, 57.8))
    )
    def test_n_c(self, f_angle, r_value):
        assert self.t_bcf.n_c(f_angle) == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 1.00), (10, 2.69), (20, 7.44), (35, 41.44))
    )
    def test_n_q(self, f_angle, r_value):
        assert self.t_bcf.n_q(f_angle) == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 0.00), (10, 0.42), (20, 3.42), (35, 46.52))
    )
    def test_n_gamma(self, f_angle, r_value):
        assert self.t_bcf.n_gamma(f_angle) == pytest.approx(r_value, ERROR_TOL)


class TestTerzaghiUBC4StripFooting:
    @pytest.mark.parametrize(
        ("soil_prop", "fs", "water_level", "res"),
        [
            (
                SoilProperties(
                    friction_angle=35.0, cohesion=15.0, moist_unit_wgt=18.0
                ),
                dict(depth=1, width=1.2, footing_shape=Shape.STRIP),
                INF,
                2114.586,
            ),
            (
                SoilProperties(
                    friction_angle=35.0, cohesion=15.0, moist_unit_wgt=18.0
                ),
                dict(depth=1.5, width=2.0, footing_shape=Shape.STRIP),
                0.4,
                1993.59,
            ),
        ],
    )
    def test_bearing_capacity(self, soil_prop, fs, water_level, res):
        fs = create_foundation(**fs)
        t_ubc = TerzaghiUBC4StripFooting(
            soil_properties=soil_prop,
            foundation_size=fs,
            water_level=water_level,
        )
        print(t_ubc.bearing_capacity())
        actual = t_ubc.bearing_capacity().magnitude
        expected = Quantity(res, UnitReg.kPa).to_compact().magnitude
        assert actual == pytest.approx(expected, ERROR_TOL)


class TestTerzaghiUBC4SquareFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(
            depth=1.0,
            width=2.0,
            footing_shape=Shape.SQUARE,
        )
        self.soil_prop = SoilProperties(
            friction_angle=25.0,
            cohesion=15.0,
            moist_unit_wgt=18.0,
        )
        return super().setUp()

    def testBearingCapacity(self):
        t_ubc = TerzaghiUBC4SquareFooting(
            soil_properties=self.soil_prop,
            foundation_size=self.fs,
            apply_local_shear=True,
        )
        actual = t_ubc.bearing_capacity().magnitude
        expected = Quantity(323.008, UnitReg.kPa).to_compact().magnitude
        assert actual == pytest.approx(expected, ERROR_TOL)


class TestTerzaghiUBC4CircFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(
            depth=1.0,
            width=2.3,
            footing_shape=Shape.CIRCLE,
        )
        self.soil_prop: SoilProperties = SoilProperties(
            **{
                "friction_angle": 25.0,
                "cohesion": 15.0,
                "moist_unit_wgt": 18.0,
            }
        )
        return super().setUp()

    def test_bearing_capacity(self):
        t_ubc = TerzaghiUBC4CircFooting(
            soil_properties=self.soil_prop,
            foundation_size=self.fs,
            apply_local_shear=True,
        )
        actual = t_ubc.bearing_capacity().magnitude
        expected = Quantity(318.9094, UnitReg.kPa).to_compact().magnitude
        assert actual == pytest.approx(expected, ERROR_TOL)


class TestTerzaghiUBC4RectFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(
            depth=1.0,
            width=1.5,
            length=2.5,
            footing_shape=Shape.RECTANGLE,
        )
        self.soil_prop: SoilProperties = SoilProperties(
            friction_angle=25.0,
            cohesion=15.0,
            moist_unit_wgt=18.0,
        )
        return super().setUp()

    def test_bearing_capacity(self):
        t_ubc = TerzaghiUBC4RectFooting(
            soil_properties=self.soil_prop,
            foundation_size=self.fs,
            apply_local_shear=True,
        )
        actual = t_ubc.bearing_capacity().magnitude
        expected = Quantity(300.0316, UnitReg.kPa).to_compact().magnitude
        assert actual == pytest.approx(expected, ERROR_TOL)
