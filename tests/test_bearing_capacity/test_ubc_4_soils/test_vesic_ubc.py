import pytest

from geolysis.bearing_capacity.ubc import VesicUltimateBearingCapacity
from geolysis.foundation import create_foundation


class TestVesicUBC:
    def test_bearing_capacity(self):
        fs = create_foundation(depth=1.0, width=1.5, eccentricity=0.2,
                               shape="square")
        ubc = VesicUltimateBearingCapacity(friction_angle=0.0,
                                           cohesion=100.0,
                                           moist_unit_wgt=21.0,
                                           foundation_size=fs)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(765.2, 0.01)
