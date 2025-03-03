import pytest

from geolysis.bearing_capacity.ubc import create_ultimate_bearing_capacity


def test_create_ultimate_bearing_capacity_errors():
    with pytest.raises(ValueError):
        create_ultimate_bearing_capacity(friction_angle=20.0,
                                         cohesion=20.0,
                                         moist_unit_wgt=18.0,
                                         depth=1.5,
                                         width=2.0,
                                         shape="square",
                                         ubc_type="BOWLES")
    with pytest.raises(ValueError):
        create_ultimate_bearing_capacity(friction_angle=20.0,
                                         cohesion=20.0,
                                         moist_unit_wgt=18.0,
                                         depth=1.5,
                                         width=2.0,
                                         shape="square")
