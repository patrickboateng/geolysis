import pytest

from geolab import ERROR_TOLERANCE
from geolab.estimators import rankine_foundation_depth, soil_unit_weight


def test_soil_unit_weight():
    suw = soil_unit_weight(spt_n60=13)
    assert suw.moist == pytest.approx(17.3, ERROR_TOLERANCE)
    assert suw.saturated == pytest.approx(18.75, ERROR_TOLERANCE)
    assert suw.submerged == pytest.approx(8.93, ERROR_TOLERANCE)


def test_foundation_depth():
    assert rankine_foundation_depth(
        350, 18, friction_angle=35
    ) == pytest.approx(  # type: ignore
        1.4, ERROR_TOLERANCE
    )
