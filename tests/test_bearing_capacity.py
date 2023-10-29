import pytest

from geolysis import ERROR_TOLERANCE
from geolysis.bearing_capacity import FoundationSize
from geolysis.bearing_capacity.hansen import HansenFactors
from geolysis.bearing_capacity.terzaghi import (
    TerzaghiBearingCapacity,
    TerzaghiFactors,
)
from geolysis.bearing_capacity.vesic import VesicFactors


class TestTerzaghiBearingCapacity:
    @classmethod
    def setup_class(cls):
        cls.tbc_1 = TerzaghiBearingCapacity(
            cohesion=16,
            soil_friction_angle=27,
            soil_unit_weight=18.5,
            foundation_size=FoundationSize(1.068, 1.068, 1.2),
        )
        cls.tbc_2 = TerzaghiBearingCapacity(
            cohesion=30,
            soil_friction_angle=30,
            soil_unit_weight=18,
            foundation_size=FoundationSize(2, 2, 1.5),
        )
        # cls.tbc_3 = TerzaghiBearingCapacity(
        #     cohesion=16,
        #     soil_friction_angle=27,
        #     soil_unit_weight=18.5,
        #     foundation_size=FoundationSize(1.715, 1.715, 1.2),
        # )

    @classmethod
    def teardown_class(cls):
        ...

    def test_nc(self):
        assert self.tbc_1.nc == pytest.approx(29.24, ERROR_TOLERANCE)
        assert self.tbc_2.nc == pytest.approx(37.16, ERROR_TOLERANCE)
        # assert self.tbc_3.nc == pytest.approx(16.21, ERROR_TOLERANCE)

    def test_nq(self):
        assert self.tbc_1.nq == pytest.approx(15.9, ERROR_TOLERANCE)
        assert self.tbc_2.nq == pytest.approx(22.46, ERROR_TOLERANCE)
        # assert self.tbc_3.nq == pytest.approx(6.54, ERROR_TOLERANCE)

    def test_ngamma(self):
        assert self.tbc_1.ngamma == pytest.approx(11.6, ERROR_TOLERANCE)
        assert self.tbc_2.ngamma == pytest.approx(19.13, ERROR_TOLERANCE)
        # assert self.tbc_3.ngamma == pytest.approx(2.73, ERROR_TOLERANCE)

    def test_ultimate_4_square_footing(self):
        assert self.tbc_1.ultimate_4_square_footing() == pytest.approx(
            1052.85, ERROR_TOLERANCE
        )
        assert self.tbc_2.ultimate_4_square_footing() == pytest.approx(
            2331.13, ERROR_TOLERANCE
        )
        # assert self.tbc_3.ultimate_4_square_footing() == pytest.approx(
        #     408.11, ERROR_TOLERANCE
        # )


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
    tbcf = TerzaghiFactors(soil_friction_angle)
    assert tbcf.nc == pytest.approx(bcf["nc"], ERROR_TOLERANCE)
    assert tbcf.nq == pytest.approx(bcf["nq"], ERROR_TOLERANCE)
    assert tbcf.ngamma == pytest.approx(bcf["ngamma"], ERROR_TOLERANCE)


# @pytest.mark.parametrize(
#     "soil_friction_angle,bcf",
#     [
#         (5, {"nq": 1.57, "nc": 6.49, "ngamma": 0.09}),
#         (10, {"nq": 2.47, "nc": 8.35, "ngamma": 0.47}),
#         (15, {"nq": 3.94, "nc": 10.98, "ngamma": 1.42}),
#         (20, {"nq": 6.40, "nc": 14.83, "ngamma": 3.54}),
#     ],
# )
# def test_hansen_bcf(soil_friction_angle: float, bcf: dict):
#     hbcf = HansenFactors(soil_friction_angle)
#     assert hbcf.nc == pytest.approx(bcf["nc"], ERROR_TOLERANCE)
#     assert hbcf.nq == pytest.approx(bcf["nq"], ERROR_TOLERANCE)
#     assert hbcf.ngamma == pytest.approx(bcf["ngamma"], ERROR_TOLERANCE)


# @pytest.mark.parametrize(
#     "soil_friction_angle,bcf",
#     [
#         (5, {"nq": 1.57, "nc": 6.49, "ngamma": 0.45}),
#         (10, {"nq": 2.47, "nc": 8.35, "ngamma": 1.22}),
#         (15, {"nq": 3.94, "nc": 10.98, "ngamma": 2.65}),
#         (20, {"nq": 6.40, "nc": 14.83, "ngamma": 5.39}),
#     ],
# )
# def test_vesic_bcf(soil_friction_angle: float, bcf: dict):
#     vbcf = VesicBearingCapacityFactors(soil_friction_angle)
#     assert vbcf.nc == pytest.approx(bcf["nc"], ERROR_TOLERANCE)
#     assert vbcf.nq == pytest.approx(bcf["nq"], ERROR_TOLERANCE)
#     assert vbcf.ngamma == pytest.approx(bcf["ngamma"], ERROR_TOLERANCE)
