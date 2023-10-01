import pytest

from geolab import ERROR_TOLERANCE
from geolab.bearing_capacity.spt import n_design


def test_n_design():
    assert n_design([7, 15, 18]) == pytest.approx(9.37, ERROR_TOLERANCE)
