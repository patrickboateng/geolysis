import pytest

from geolysis.bearing_capacity.ubc import create_ubc_4_all_soil_types


class TestVesicUBC:
    @pytest.mark.parametrize(
        [
            "friction_angle",
            "cohesion",
            "moist_unit_wgt",
            "depth",
            "width",
            "length",
            "eccentricity",
            "shape",
            "expected",
        ],
        [
            (0.0, 100.0, 21.0, 1.0, 1.5, None, 0.2, "square", 765.2),
            (20.0, 20.0, 18.0, 1.5, 2.0, None, 0.0, "strip", 697.13),
            (20.0, 20.0, 18.0, 1.5, 2.0, None, 0.0, "square", 901.37),
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
        eccentricity,
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
            eccentricity=eccentricity,
            shape=shape,
            ubc_type="vesic",
        )
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)
