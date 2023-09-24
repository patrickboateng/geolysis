import pytest

from geolab import ERROR_TOLERANCE
from geolab.bearing_capacity import FoundationSize
from geolab.bearing_capacity.ultimate import (
    TerzaghiBearingCapacity,
    TerzaghiBearingCapacityFactors,
    hansen_bearing_capacity_factors,
    vesic_bearing_capacity_factors,
)


class TestTerzaghiBearingCapacity:
    @classmethod
    def setup_class(cls):
        fs_general_shear = FoundationSize(1.068, 1.068, 1.2)
        fs_local_shear = FoundationSize(1.715, 1.715, 1.2)
        cls.tbc_general_shear = TerzaghiBearingCapacity(
            16, 27, 18.5, fs_general_shear
        )
        cls.tbc_local_shear = TerzaghiBearingCapacity(
            16, 27, 18.5, fs_local_shear, local_shear=True
        )

    @classmethod
    def teardown_class(cls):
        ...

    def test_nc(self):
        assert self.tbc_general_shear.nc == pytest.approx(
            29.24, ERROR_TOLERANCE
        )
        assert self.tbc_local_shear.nc == pytest.approx(16.21, ERROR_TOLERANCE)

    def test_nq(self):
        assert self.tbc_general_shear.nq == pytest.approx(
            15.9, ERROR_TOLERANCE
        )
        assert self.tbc_local_shear.nq == pytest.approx(6.54, ERROR_TOLERANCE)

    def test_ngamma(self):
        assert self.tbc_general_shear.ngamma == pytest.approx(
            11.6, ERROR_TOLERANCE
        )
        assert self.tbc_local_shear.ngamma == pytest.approx(
            2.73, ERROR_TOLERANCE
        )

    def test_soil_friction_angle(self):
        assert self.tbc_local_shear.soil_friction_angle == pytest.approx(
            18.76, ERROR_TOLERANCE
        )

    def test_ultimate_4_square_footing(self):
        print(self.tbc_local_shear.ultimate_4_square_footing())
        assert (
            self.tbc_general_shear.ultimate_4_square_footing()
            == pytest.approx(1052.85, ERROR_TOLERANCE)
        )
        assert (
            self.tbc_local_shear.ultimate_4_square_footing()
            == pytest.approx(408.11, ERROR_TOLERANCE)
        )

    # def test_ultimate_4_circular_footing(self):
    #     ...

    # def test_ultimate_4_strip_footing(self):
    #     ...


@pytest.mark.parametrize(
    "soil_friction_angle,bcf",
    [
        (1, {"nq": 1.10, "nc": 5.73, "ngamma": 0.0}),
        (15, {"nq": 4.45, "nc": 12.86, "ngamma": 1.32}),
        (25, {"nq": 12.72, "nc": 25.13, "ngamma": 8.21}),
        (27, {"nq": 15.9, "nc": 29.24, "ngamma": 11.6}),
        (18.76, {"nq": 6.54, "nc": 16.21, "ngamma": 2.73}),
    ],
)
def test_terzaghi_bcf(soil_friction_angle: float, bcf: dict):
    tbcf = TerzaghiBearingCapacityFactors(soil_friction_angle)
    assert tbcf.nc == pytest.approx(bcf["nc"], ERROR_TOLERANCE)
    assert tbcf.nq == pytest.approx(bcf["nq"], ERROR_TOLERANCE)
    assert tbcf.ngamma == pytest.approx(bcf["ngamma"], ERROR_TOLERANCE)


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
