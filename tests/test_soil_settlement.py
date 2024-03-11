import pytest

from geolysis.constants import ERROR_TOL
from geolysis.foundation import SquareFooting
from geolysis.soil_settlement import immediate_settlement_cohl


def test_imm_settlement_cohl():
    I = [0.26, 0.453, 0.333, 0.2, 0.067]
    E = [8000, 9000, 10000, 11000, 12300]

    sett = immediate_settlement_cohl(24, 200, 6, E, I, SquareFooting(2.5))

    assert sett == pytest.approx(31.07, ERROR_TOL)
