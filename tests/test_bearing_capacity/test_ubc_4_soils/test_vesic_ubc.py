import pytest

from geolysis.bearing_capacity.ubc import VesicUltimateBearingCapacity

from geolysis.foundation import create_foundation

ERROR_TOL = 0.01


class TestVesicUBC:
    def test_bearing_capacity(self):
        fs = create_foundation(depth=1.0, width=1.5, eccentricity=0.2,
                               shape="square")
        prop = dict(friction_angle=0.0, cohesion=100.0, moist_unit_wgt=21.0)
        ubc = VesicUltimateBearingCapacity(soil_properties=prop,
                                           foundation_size=fs)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(765.2, ERROR_TOL)
