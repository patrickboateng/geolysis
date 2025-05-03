import pytest

from geolysis.bearing_capacity.abc.cohl import \
    create_allowable_bearing_capacity


def test_create_allowable_bearing_capacity_errors():
    # abc_type was not provided
    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2)

    # Invalid abc_type provided
    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2,
                                          abc_type="HANSEN")

    # Invalid foundation_type provided
    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2,
                                          abc_type="BOWLES",
                                          foundation_type="COMBINED")
