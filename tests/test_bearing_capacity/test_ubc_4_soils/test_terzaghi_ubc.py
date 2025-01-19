import unittest

import pytest

from geolysis.bearing_capacity.ubc import (
    TerzaghiUBC4RectangularFooting, TerzaghiUBC4CircularFooting,
    TerzaghiUBC4SquareFooting, TerzaghiUBC4StripFooting,
    TerzaghiBearingCapacityFactor)

from geolysis.foundation import create_foundation
from geolysis.utils import inf

ERROR_TOL = 0.01


class TestTerzaghiBCF:
    @pytest.mark.parametrize("f_angle, r_value",
                             ((0, 5.70), (10, 9.61), (20, 17.69), (35, 57.8)))
    def test_n_c(self, f_angle, r_value):
        nc = TerzaghiBearingCapacityFactor.n_c(f_angle)
        assert nc == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize("f_angle, r_value",
                             ((0, 1.00), (10, 2.69), (20, 7.44), (35, 41.44)))
    def test_n_q(self, f_angle, r_value):
        nq = TerzaghiBearingCapacityFactor.n_q(f_angle)
        assert nq == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize("f_angle, r_value",
                             ((0, 0.00), (10, 0.42), (20, 3.42), (35, 46.52)))
    def test_n_gamma(self, f_angle, r_value):
        ngamma = TerzaghiBearingCapacityFactor.n_gamma(f_angle)
        assert ngamma == pytest.approx(r_value, ERROR_TOL)


class TestTerzaghiUBC4StripFooting:
    @pytest.mark.parametrize(("soil_prop", "fs", "water_level", "expected"),
                             [(dict(friction_angle=35.0, cohesion=15.0,
                                    moist_unit_wgt=18.0),
                               dict(depth=1.0, width=1.2, shape="strip"), 
                               inf, 2114.586),
                              (dict(friction_angle=35.0, cohesion=15.0,
                                    moist_unit_wgt=18.0),
                               dict(depth=1.5, width=2.0, shape="strip"), 
                               0.4, 1993.59)])
    def test_bearing_capacity(self, soil_prop, fs, water_level, expected):
        fs = create_foundation(**fs)
        ubc = TerzaghiUBC4StripFooting(soil_properties=soil_prop,
                                       foundation_size=fs,
                                       ground_water_level=water_level)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(expected, ERROR_TOL)


class TestTerzaghiUBC4SquareFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(depth=1.0, width=2.0,
                                    shape="square")
        self.soil_prop = dict(friction_angle=25.0, cohesion=15.0,
                              moist_unit_wgt=18.0)

    def test_bearing_capacity(self):
        ubc = TerzaghiUBC4SquareFooting(soil_properties=self.soil_prop,
                                        foundation_size=self.fs,
                                        apply_local_shear=True)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(323.008, ERROR_TOL)


class TestTerzaghiUBC4CircFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(depth=1.0, width=2.3,
                                    shape="circle")
        self.soil_prop = dict({"friction_angle": 25.0, "cohesion": 15.0,
                               "moist_unit_wgt": 18.0})

    def test_bearing_capacity(self):
        ubc = TerzaghiUBC4CircularFooting(soil_properties=self.soil_prop,
                                      foundation_size=self.fs,
                                      apply_local_shear=True)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(318.9094, ERROR_TOL)


class TestTerzaghiUBC4RectFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(depth=1.0, width=1.5, length=2.5,
                                    shape="rectangle")
        self.soil_prop = dict(friction_angle=25.0, cohesion=15.0,
                              moist_unit_wgt=18.0)

    def test_bearing_capacity(self):
        ubc = TerzaghiUBC4RectangularFooting(soil_properties=self.soil_prop,
                                      foundation_size=self.fs,
                                      apply_local_shear=True)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(300.0316, ERROR_TOL)
