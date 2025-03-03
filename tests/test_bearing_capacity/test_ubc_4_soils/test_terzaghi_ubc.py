import unittest

import pytest

from geolysis.bearing_capacity.ubc import (TerzaghiUBC4CircularFooting,
                                           TerzaghiUBC4RectangularFooting,
                                           TerzaghiUBC4SquareFooting,
                                           TerzaghiUBC4StripFooting,
                                           create_ultimate_bearing_capacity)
from geolysis.foundation import create_foundation


# class TestTerzaghiBCF:
#     @pytest.mark.parametrize("f_angle, expected",
#                              [(0.0, 5.70),
#                               (10.0, 9.61),
#                               (20.0, 17.69),
#                               (35.0, 57.8)])
#     def test_n_c(self, f_angle, expected):
#         nc = TerzaghiBearingCapacityFactor.n_c(f_angle)
#         assert nc == pytest.approx(expected, 0.01)
#
#     @pytest.mark.parametrize("f_angle, expected",
#                              [(0.0, 1.00),
#                               (10.0, 2.69),
#                               (20.0, 7.44),
#                               (35.0, 41.44)])
#     def test_n_q(self, f_angle, expected):
#         nq = TerzaghiBearingCapacityFactor.n_q(f_angle)
#         assert nq == pytest.approx(expected, 0.01)
#
#     @pytest.mark.parametrize("f_angle, expected",
#                              [(0.0, 0.00),
#                               (10.0, 0.42),
#                               (20.0, 3.42),
#                               (35.0, 46.52)])
#     def test_n_gamma(self, f_angle, expected):
#         ngamma = TerzaghiBearingCapacityFactor.n_gamma(f_angle)
#         assert ngamma == pytest.approx(expected, 0.01)


class TestTerzaghiUBC4StripFooting:
    @pytest.mark.parametrize(
        ["friction_angle", "cohesion", "moist_unit_wgt",
         "depth", "width", "water_level", "expected"],
        [(35.0, 15.0, 18.0, 1.0, 1.2, None, 2114.586),
         (35.0, 15.0, 18.0, 1.5, 2.0, 0.4, 1993.59),
         (0, 15.0, 18.0, 1.5, 1.2, None, 112.5)])
    def test_bearing_capacity(self, friction_angle,
                              cohesion,
                              moist_unit_wgt,
                              depth,
                              width,
                              water_level,
                              expected):
        ubc = create_ultimate_bearing_capacity(friction_angle=friction_angle,
                                               cohesion=cohesion,
                                               moist_unit_wgt=moist_unit_wgt,
                                               depth=depth,
                                               width=width,
                                               ground_water_level=water_level,
                                               shape="strip",
                                               ubc_type="TERZAGHI")
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)


class TestTerzaghiUBC4SquareFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(depth=1.0, width=2.0, shape="square")
        self.soil_prop = dict(friction_angle=25.0, cohesion=15.0,
                              moist_unit_wgt=18.0)

    def test_bearing_capacity(self):
        ubc = TerzaghiUBC4SquareFooting(**self.soil_prop,
                                        foundation_size=self.fs,
                                        apply_local_shear=True)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(323.008, 0.01)


class TestTerzaghiUBC4CircFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(depth=1.0, width=2.3, shape="circle")
        self.soil_prop = dict({"friction_angle": 25.0, "cohesion": 15.0,
                               "moist_unit_wgt": 18.0})

    def test_bearing_capacity(self):
        ubc = TerzaghiUBC4CircularFooting(**self.soil_prop,
                                          foundation_size=self.fs,
                                          apply_local_shear=True)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(318.9094, 0.01)


class TestTerzaghiUBC4RectFooting(unittest.TestCase):
    def setUp(self):
        self.fs = create_foundation(depth=1.0, width=1.5, length=2.5,
                                    shape="rectangle")
        self.soil_prop = dict(friction_angle=25.0, cohesion=15.0,
                              moist_unit_wgt=18.0)

    def test_bearing_capacity(self):
        ubc = TerzaghiUBC4RectangularFooting(**self.soil_prop,
                                             foundation_size=self.fs,
                                             apply_local_shear=True)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(300.0316, 0.01)
