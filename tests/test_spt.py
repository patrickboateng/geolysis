import pytest

from geolysis import ERROR_TOLERANCE
from geolysis.bearing_capacity.spt import n_design


def test_n_design():
    assert n_design([7, 15, 18]) == pytest.approx(9.37, ERROR_TOLERANCE)
