import pytest

from geolab import ERROR_TOLERANCE
from geolab.estimators import rankine_foundation_depth


def test_foundation_depth():
    assert rankine_foundation_depth(
        350, 18, friction_angle=35
    ) == pytest.approx(  # type: ignore
        1.4, ERROR_TOLERANCE
    )
