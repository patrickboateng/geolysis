import pytest

from geolab import ERROR_TOLERANCE
from geolab.corrections import dilatancy_spt_correction


@pytest.mark.parametrize(
    "n_value,exp", [(30, 22.5), (20, 17.5), (15, 15), (10, 10), (5, 5)]
)
def test_dilatancy_spt_correction(n_value, exp):
    assert dilatancy_spt_correction(n_value) == pytest.approx(exp, ERROR_TOLERANCE)
