import pytest
from geolysis.exceptions import ValidationError

from geolysis.bearing_capacity.abc import create_abc_4_cohesionless_soils


def test_create_allowable_bearing_capacity_errors():
    # Invalid abc_type provided
    with pytest.raises(ValidationError):
        create_abc_4_cohesionless_soils(
            corrected_spt_n_value=12,
            tol_settlement=20,
            depth=1.5,
            width=1.2,
            abc_type="HANSEN",
        )

    # Invalid foundation_type provided
    with pytest.raises(ValidationError):
        create_abc_4_cohesionless_soils(
            corrected_spt_n_value=12,
            tol_settlement=20,
            depth=1.5,
            width=1.2,
            abc_type="BOWLES",
            foundation_type="COMBINED",
        )
