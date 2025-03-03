import pytest

from geolysis.bearing_capacity.ubc import create_ultimate_bearing_capacity


class TestVesicUBC:
    @pytest.mark.parametrize(
        ["friction_angle", "cohesion", "moist_unit_wgt", "depth",
         "width", "length", "eccentricity", "shape", "expected"],
        [(0.0, 100.0, 21.0, 1.0, 1.5, None, 0.2, "square", 765.2)])
    def test_bearing_capacity(self, friction_angle,
                              cohesion,
                              moist_unit_wgt,
                              depth,
                              width,
                              length,
                              eccentricity,
                              shape,
                              expected):
        ubc = create_ultimate_bearing_capacity(friction_angle=friction_angle,
                                               cohesion=cohesion,
                                               moist_unit_wgt=moist_unit_wgt,
                                               depth=depth,
                                               width=width,
                                               length=length,
                                               eccentricity=eccentricity,
                                               shape=shape,
                                               ubc_type="VESIC")
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(expected, 0.01)
