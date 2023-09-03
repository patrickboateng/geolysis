import pytest

from geolab import ERROR_TOLERANCE
from geolab.estimators import misc


def test_foundation_depth():
    assert misc.foundation_depth(350, 18, friction_angle=35) == pytest.approx(
        1.429, ERROR_TOLERANCE
    )
