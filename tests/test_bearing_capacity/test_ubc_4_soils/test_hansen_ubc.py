import pytest

from geolysis.bearing_capacity.ubc import create_ubc_4_all_soil_types


class TestHansenUBC:
    @pytest.mark.parametrize(
        [
            "friction_angle",
            "cohesion",
            "moist_unit_wgt",
            "depth",
            "width",
            "length",
            "shape",
            "expected",
        ],
        [
            (20.0, 20.0, 18.0, 1.5, 2.0, None, "square", 798.41),
            (20.0, 20.0, 18.0, 1.5, 2.0, None, "strip", 655.42),
            (20.0, 20.0, 18.0, 1.5, 2.0, 3.0, "rectangle", 715.13),
            (20.0, 20.0, 18.0, 1.5, 2.0, None, "circle", 785.66),
        ],
    )
    def test_bearing_capacity(
        self,
        friction_angle,
        cohesion,
        moist_unit_wgt,
        depth,
        width,
        length,
        shape,
        expected,
    ):
        ubc = create_ubc_4_all_soil_types(
            friction_angle=friction_angle,
            cohesion=cohesion,
            moist_unit_wgt=moist_unit_wgt,
            depth=depth,
            width=width,
            length=length,
            shape=shape,
            ubc_type="hansen",
        )
        actual = ubc.ultimate_bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)
