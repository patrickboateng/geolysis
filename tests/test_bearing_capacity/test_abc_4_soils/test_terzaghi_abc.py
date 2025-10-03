import pytest

from geolysis.bearing_capacity.abc import create_abc_4_cohesionless_soils
from geolysis.utils import inf


class TestTerzaghiABC:

    @pytest.mark.parametrize(
        [
            "corrected_spt_n_value",
            "tol_settlement",
            "depth",
            "width",
            "ground_water_level",
            "footing_shape",
            "foundation_type",
            "expected",
        ],
        [
            (12.0, 20.0, 1.5, 1.2, 1.2, "square", "pad", 65.97),
            (12.0, 20.0, 1.5, 1.2, inf, "square", "pad", 45.35),
            (12.0, 20.0, 1.5, 1.3, 1.8, "square", "pad", 70.35),
        ],
    )
    def test_terzaghi_abc_4_pad_foundation(
            self,
            corrected_spt_n_value,
            tol_settlement,
            depth,
            width,
            ground_water_level,
            footing_shape,
            foundation_type,
            expected,
    ):
        terzaghi = create_abc_4_cohesionless_soils(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            ground_water_level=ground_water_level,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="terzaghi",
        )

        assert terzaghi.allowable_bearing_capacity() == pytest.approx(
            expected=expected, rel=0.01
        )

    @pytest.mark.parametrize(
        [
            "corrected_spt_n_value",
            "tol_settlement",
            "depth",
            "width",
            "ground_water_level",
            "footing_shape",
            "foundation_type",
            "expected",
        ],
        [(12.0, 20.0, 1.5, 1.2, 1.2, "square", "mat", 43.98)],
    )
    def test_terzaghi_abc_4_mat_foundation(
            self,
            corrected_spt_n_value,
            tol_settlement,
            depth,
            width,
            ground_water_level,
            footing_shape,
            foundation_type,
            expected,
    ):
        terzaghi = create_abc_4_cohesionless_soils(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            ground_water_level=ground_water_level,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="terzaghi",
        )

        assert terzaghi.allowable_bearing_capacity() == pytest.approx(
            expected=expected, rel=0.01
        )
