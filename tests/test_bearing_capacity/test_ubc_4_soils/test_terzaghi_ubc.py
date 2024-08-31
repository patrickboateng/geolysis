import unittest

import pytest

from geolysis.core.bearing_capacity.ubc_4_soils.terzaghi_ubc import (
    TerzaghiBearingCapacityFactor,
    TerzaghiUBC4StripFooting,
)

# from geolysis.core.constants import SoilData
from geolysis.core.foundation import Shape, create_foundation

ERROR_TOL = 0.01


class TestTerzaghiBCF:
    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 5.70), (10, 9.61), (20, 17.69), (35, 57.8))
    )
    def test_n_c(self, f_angle, r_value):
        t_bcf = TerzaghiBearingCapacityFactor()
        assert t_bcf.n_c(f_angle) == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 1.00), (10, 2.69), (20, 7.44), (35, 41.44))
    )
    def test_n_q(self, f_angle, r_value):
        t_bcf = TerzaghiBearingCapacityFactor()
        assert t_bcf.n_q(f_angle) == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize(
        ("f_angle, r_value"), ((0, 0.00), (10, 0.42), (20, 3.42), (35, 46.52))
    )
    def test_n_gamma(self, f_angle, r_value):
        t_bcf = TerzaghiBearingCapacityFactor()
        assert t_bcf.n_gamma(f_angle) == pytest.approx(r_value, ERROR_TOL)


class TestTerzaghiUBC4StripFooting(unittest.TestCase):
    # @classmethod
    # def setup_class(cls):
    #     cls.soil_prop = {
    #         "friction_angle": 35.0,
    #         "cohesion": 15.0,
    #         "moist_unit_wgt": 18.0,
    #     }

    def setUp(self) -> None:
        self.soil_prop = {
            "friction_angle": 35.0,
            "cohesion": 15.0,
            "moist_unit_wgt": 18.0,
        }
        return super().setUp()

    #: footing not embedded in water
    def testBearingCapacity(self):
        fs = create_foundation(
            depth=1,
            width=1.2,
            footing_shape=Shape.STRIP,
        )

        t = TerzaghiUBC4StripFooting(
            soil_properties=self.soil_prop, foundation_size=fs
        )
        # self.assertAlmostEqual(t.bearing_capacity(), 2114.586)
        assert t.bearing_capacity() == pytest.approx(2114.586, ERROR_TOL)

    #: footing embedded in water
    def testEmbBearingCapacity(self):
        fs = create_foundation(
            depth=1.5,
            width=2.0,
            footing_shape=Shape.STRIP,
        )
        t = TerzaghiUBC4StripFooting(
            soil_properties=self.soil_prop,
            foundation_size=fs,
            water_level=0.4,
        )
        assert t.bearing_capacity() == pytest.approx(1993.59, ERROR_TOL)


# class TestTerzaghiUBC4SquareFooting:
#     def test_bearing_capacity(self):
#         fs = create_foundation(
#             depth=1.0,
#             width=2.0,
#             footing_shape=Shape.SQUARE,
#         )
#         soil_prop = {
#             "soil_friction_angle": 25.0,
#             "cohesion": 15.0,
#             "moist_unit_wgt": 18.0,
#         }

#         t = TerzaghiUBC4SquareFooting(
#             soil_properties=soil_prop,
#             foundation_size=fs,
#             local_shear_failure=True,
#         )
#         assert t.bearing_capacity() == pytest.approx(323.008, ERROR_TOL)


# class TestTerzaghiUBC4CircFooting:
#     def test_bearing_capacity(self):
#         fs = create_foundation(
#             depth=1.0,
#             width=2.3,
#             footing_shape=Shape.CIRCLE,
#         )
#         soil_prop = {
#             "soil_friction_angle": 25.0,
#             "cohesion": 15.0,
#             "moist_unit_wgt": 18.0,
#         }
#         t = TerzaghiUBC4CircFooting(
#             soil_properties=soil_prop,
#             foundation_size=fs,
#             local_shear_failure=True,
#         )
#         assert t.bearing_capacity() == pytest.approx(318.9094, ERROR_TOL)


# class TestTerzaghiUBC4RectFooting:
#     def test_bearing_capacity(self):
#         fs = create_foundation(
#             depth=1.0,
#             width=1.5,
#             length=2.5,
#             footing_shape=Shape.RECTANGLE,
#         )
#         soil_prop = {
#             "soil_friction_angle": 25.0,
#             "cohesion": 15.0,
#             "moist_unit_wgt": 18.0,
#         }
#         t = TerzaghiUBC4RectFooting(
#             soil_properties=soil_prop,
#             foundation_size=fs,
#             local_shear_failure=True,
#         )
#         assert t.bearing_capacity() == pytest.approx(300.0316, ERROR_TOL)


# # class TestHansenUBC:
# #     @pytest.mark.parametrize(
# #         ("f_angle, r_value"), ((0, 5.14), (10, 8.34), (20, 14.83), (35, 46.13))
# #     )
# #     def test_n_c(self, f_angle, r_value):
# #         t_bcf = HansenBearingCapacityFactor()
# #         assert t_bcf.n_c(f_angle) == pytest.approx(r_value, ERROR_TOL)

# #     @pytest.mark.parametrize(
# #         ("f_angle, r_value"), ((0, 1.00), (10, 2.47), (20, 6.4), (35, 33.29))
# #     )
# #     def test_n_q(self, f_angle, r_value):
# #         t_bcf = HansenBearingCapacityFactor()
# #         assert t_bcf.n_q(f_angle) == pytest.approx(r_value, ERROR_TOL)

# #     @pytest.mark.parametrize(
# #         ("f_angle, r_value"), ((0, 0.00), (10, 0.47), (20, 3.54), (35, 40.69))
# #     )
# #     def test_n_gamma(self, f_angle, r_value):
# #         t_bcf = HansenBearingCapacityFactor()
# #         assert t_bcf.n_gamma(f_angle) == pytest.approx(r_value, ERROR_TOL)

# #     def test_bearing_capacity(self):
# #         fs = create_foundation(
# #             depth=1.5,
# #             width=2.0,
# #             footing_shape=Shape.SQUARE,
# #         )
# #         soil_prop = {
# #             "soil_friction_angle": 20.0,
# #             "cohesion": 20.0,
# #             "moist_unit_wgt": 18.0,
# #         }
# #         t = HansenUBC(soil_properties=soil_prop, foundation_size=fs)
# #         assert t.bearing_capacity() == pytest.approx(809.36, ERROR_TOL)


# # class TestVesicUBC:
# #     def test_bearing_capacity(self):
# #         fs = create_foundation(
# #             depth=1.0,
# #             width=1.5,
# #             footing_shape=Shape.SQUARE,
# #         )
# #         soil_prop = {
# #             "soil_friction_angle": 0.0,
# #             "cohesion": 100.0,
# #             "moist_unit_wgt": 21.0,
# #         }
# #         t = VesicUBC(soil_properties=soil_prop, foundation_size=fs, e=0.2)
# #         assert t.bearing_capacity() == pytest.approx(765.2, ERROR_TOL)
