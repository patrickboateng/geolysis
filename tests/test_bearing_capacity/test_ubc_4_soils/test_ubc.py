import pytest
from func_validator import ValidationError

from geolysis.bearing_capacity.ubc import create_ubc_4_all_soil_types


def test_create_ultimate_bearing_capacity_errors():
    # Invalid ubc_type
    with pytest.raises(ValidationError):
        create_ubc_4_all_soil_types(
            friction_angle=20.0,
            cohesion=20.0,
            moist_unit_wgt=18.0,
            depth=1.5,
            width=2.0,
            shape="square",
            ubc_type="BOWLES",
        )
