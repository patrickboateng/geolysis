import pytest

from geolysis.bearing_capacity.ubc import create_ubc_4_all_soil_types
from geolysis.utils import inf


#
# class TestTerzaghiUBC4StripFooting:
#     @pytest.mark.parametrize(
#         [
#             "friction_angle",
#             "cohesion",
#             "moist_unit_wgt",
#             "depth",
#             "width",
#             "water_level",
#             "expected",
#         ],
#         [
#             (35.0, 15.0, 18.0, 1.0, 1.2, None, 2114.586),
#             (35.0, 15.0, 18.0, 1.5, 2.0, 0.4, 1993.59),
#             (0, 15.0, 18.0, 1.5, 1.2, None, 112.5),
#         ],
#     )
#     def test_bearing_capacity(
#         self,
#         friction_angle,
#         cohesion,
#         moist_unit_wgt,
#         depth,
#         width,
#         water_level,
#         expected,
#     ):
#         ubc = create_ubc_4_all_soil_types(
#             friction_angle=friction_angle,
#             cohesion=cohesion,
#             moist_unit_wgt=moist_unit_wgt,
#             depth=depth,
#             width=width,
#             ground_water_level=water_level,
#             shape="strip",
#             ubc_type="terzaghi",
#         )
#         actual = ubc.ultimate_bearing_capacity()
#         assert actual == pytest.approx(expected, 0.01)


class TestTerzaghiUBC4SquareFooting:
    @pytest.mark.parametrize(
        [
            "friction_angle",
            "cohesion",
            "moist_unit_wgt",
            "depth",
            "width",
            "water_level",
            "apply_loc_shear",
            "expected",
        ],
        [(25.0, 15.0, 18.0, 1.0, 2.0, inf, True, 323.01)],
    )
    def test_bearing_capacity(
        self,
        friction_angle,
        cohesion,
        moist_unit_wgt,
        depth,
        width,
        water_level,
        apply_loc_shear,
        expected,
    ):
        ubc = create_ubc_4_all_soil_types(
            friction_angle=friction_angle,
            cohesion=cohesion,
            moist_unit_wgt=moist_unit_wgt,
            depth=depth,
            width=width,
            ground_water_level=water_level,
            shape="square",
            apply_local_shear=apply_loc_shear,
            ubc_type="terzaghi",
        )
        actual = ubc.ultimate_bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)


class TestTerzaghiUBC4CircFooting:

    @pytest.mark.parametrize(
        [
            "friction_angle",
            "cohesion",
            "moist_unit_wgt",
            "depth",
            "width",
            "water_level",
            "apply_loc_shear",
            "expected",
        ],
        [(25.0, 15.0, 18.0, 1.0, 2.3, inf, True, 318.9)],
    )
    def test_bearing_capacity(
        self,
        friction_angle,
        cohesion,
        moist_unit_wgt,
        depth,
        width,
        water_level,
        apply_loc_shear,
        expected,
    ):
        ubc = create_ubc_4_all_soil_types(
            friction_angle=friction_angle,
            cohesion=cohesion,
            moist_unit_wgt=moist_unit_wgt,
            depth=depth,
            width=width,
            ground_water_level=water_level,
            shape="circle",
            apply_local_shear=apply_loc_shear,
            ubc_type="terzaghi",
        )
        actual = ubc.ultimate_bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)


class TestTerzaghiUBC4RectFooting:

    @pytest.mark.parametrize(
        [
            "friction_angle",
            "cohesion",
            "moist_unit_wgt",
            "depth",
            "width",
            "length",
            "water_level",
            "apply_loc_shear",
            "expected",
        ],
        [(25.0, 15.0, 18.0, 1.0, 1.5, 2.5, inf, True, 300.03)],
    )
    def test_bearing_capacity(
        self,
        friction_angle,
        cohesion,
        moist_unit_wgt,
        depth,
        width,
        length,
        water_level,
        apply_loc_shear,
        expected,
    ):
        ubc = create_ubc_4_all_soil_types(
            friction_angle=friction_angle,
            cohesion=cohesion,
            moist_unit_wgt=moist_unit_wgt,
            depth=depth,
            width=width,
            length=length,
            ground_water_level=water_level,
            shape="rectangle",
            apply_local_shear=apply_loc_shear,
            ubc_type="terzaghi",
        )
        actual = ubc.ultimate_bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)
