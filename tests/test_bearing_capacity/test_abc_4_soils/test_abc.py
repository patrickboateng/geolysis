import pytest

from geolysis.bearing_capacity.abc.cohl import \
    create_allowable_bearing_capacity


def test_create_allowable_bearing_capacity_errors():
    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2)

    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2,
                                          abc_type="HANSEN")

    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2,
                                          abc_type="BOWLES",
                                          foundation_type="COMBINED")
