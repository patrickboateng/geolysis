import pytest

from geolab import ERROR_TOLERANCE
from geolab.bearing_capacity.ultimate import (
    hansen_bearing_capacity_factors,
    terzaghi_bearing_capacity_factors,
    vesic_bearing_capacity_factors,
)


@pytest.mark.parametrize(
    "soil_friction_angle,bcf",
    [
        (1, {"nq": 1.10, "nc": 6.00}),
        (15, {"nq": 4.45, "nc": 12.86}),
        (25, {"nq": 12.72, "nc": 25.13}),
        (27, {"nq": 15.9, "nc": 29.24}),
        (18.76, {"nq": 6.54, "nc": 16.21}),
    ],
)
def test_terzaghi_bcf(soil_friction_angle: float, bcf: dict):
    tbcf = terzaghi_bearing_capacity_factors(soil_friction_angle)
    assert tbcf.nc == pytest.approx(bcf["nc"], ERROR_TOLERANCE)
    assert tbcf.nq == pytest.approx(bcf["nq"], ERROR_TOLERANCE)


@pytest.mark.parametrize(
    "soil_friction_angle,bcf",
    [
        (5, {"nq": 1.57, "nc": 6.49, "ngamma": 0.09}),
        (10, {"nq": 2.47, "nc": 8.35, "ngamma": 0.47}),
        (15, {"nq": 3.94, "nc": 10.98, "ngamma": 1.42}),
        (20, {"nq": 6.40, "nc": 14.83, "ngamma": 3.54}),
    ],
)
def test_hansen_bcf(soil_friction_angle: float, bcf: dict):
    hbcf = hansen_bearing_capacity_factors(soil_friction_angle)
    assert hbcf.nc == pytest.approx(bcf["nc"], ERROR_TOLERANCE)
    assert hbcf.nq == pytest.approx(bcf["nq"], ERROR_TOLERANCE)
    assert hbcf.ngamma == pytest.approx(bcf["ngamma"], ERROR_TOLERANCE)


@pytest.mark.parametrize(
    "soil_friction_angle,bcf",
    [
        (5, {"nq": 1.57, "nc": 6.49, "ngamma": 0.45}),
        (10, {"nq": 2.47, "nc": 8.35, "ngamma": 1.22}),
        (15, {"nq": 3.94, "nc": 10.98, "ngamma": 2.65}),
        (20, {"nq": 6.40, "nc": 14.83, "ngamma": 5.39}),
    ],
)
def test_vesic_bcf(soil_friction_angle: float, bcf: dict):
    vbcf = vesic_bearing_capacity_factors(soil_friction_angle)
    assert vbcf.nc == pytest.approx(bcf["nc"], ERROR_TOLERANCE)
    assert vbcf.nq == pytest.approx(bcf["nq"], ERROR_TOLERANCE)
    assert vbcf.ngamma == pytest.approx(bcf["ngamma"], ERROR_TOLERANCE)
