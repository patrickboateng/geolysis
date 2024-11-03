import pytest

from geolysis.core import Quantity
from geolysis.core._config.config import UReg
from geolysis.core.bearing_capacity.ubc_4_soils import Soil
from geolysis.core.bearing_capacity.ubc_4_soils.vesic_ubc import (
    VesicUltimateBearingCapacity,
)
from geolysis.core.foundation import Shape, create_foundation

ERROR_TOL = 0.01


class TestVesicUBC:
    def test_bearing_capacity(self):
        fs = create_foundation(
            depth=1.0,
            width=1.5,
            eccentricity=0.2,
            footing_shape=Shape.SQUARE,
        )
        soil_prop = Soil(
            friction_angle=0.0,
            cohesion=100.0,
            moist_unit_wgt=21.0,
        )
        v_ubc = VesicUltimateBearingCapacity(
            soil_properties=soil_prop,
            foundation_size=fs,
        )
        actual = v_ubc.bearing_capacity().magnitude
        expected = Quantity(765.2, UReg.kPa).to_compact().magnitude
        assert actual == pytest.approx(expected, ERROR_TOL)
