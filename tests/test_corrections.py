import pytest

from geolab import ERROR_TOLERANCE
from geolab.bearing_capacity.spt_corrections import (
    dilatancy_spt_correction,
    spt_n60,
)


@pytest.mark.parametrize(
    "n_value,exp", [(30, 22.5), (20, 17.5), (15, 15), (10, 10), (5, 5)]
)
def test_dilatancy_spt_correction(n_value, exp):
    assert dilatancy_spt_correction(n_value) == pytest.approx(
        exp, ERROR_TOLERANCE
    )


def test_spt_n60():
    assert spt_n60(15, 0.6, 1.0, 1.0, 0.85) == pytest.approx(
        12.75, ERROR_TOLERANCE
    )
