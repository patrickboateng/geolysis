import pytest

from geolysis.bearing_capacity.ubc import create_ubc_4_all_soils


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
            (0.0, 100.0, 21.0, 1.0, 1.5, None, 0.2, "square", 773.0),  # 765.2
            (20.0, 20.0, 18.0, 1.5, 2.0, None, 0.0, "strip", 697.13),
            (20.0, 20.0, 18.0, 1.5, 2.0, None, 0.0, "square", 901.37),
            (25, 20, 16.5, 1.5, 2.0, None, 0.0, "square", 1373.2),
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
        ubc = create_ubc_4_all_soils(
            friction_angle=friction_angle,
            cohesion=cohesion,
            moist_unit_wgt=moist_unit_wgt,
            depth=depth,
            width=width,
            length=length,
            eccentricity=eccentricity,
            shape=shape,
            ubc_method="vesic",
        )
        actual = ubc.ultimate_bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)


def test_water_depth():
    ubc = create_ubc_4_all_soils(
        friction_angle=32,
        cohesion=0,
        moist_unit_wgt=16,
        depth=1.0,
        width=1.2,
        saturated_unit_wgt=19.5,
        ground_water_level=0.5,
    )

    actual = ubc.ultimate_bearing_capacity()
    assert actual == pytest.approx(700.5)


def test_water_depth_2():
    ubc = create_ubc_4_all_soils(
        friction_angle=32,
        cohesion=0,
        moist_unit_wgt=16,
        depth=1.0,
        width=1.2,
        saturated_unit_wgt=19.5,
        ground_water_level=1.5,
    )

    actual = ubc.ultimate_bearing_capacity()
    assert actual == pytest.approx(875, 0.01)
