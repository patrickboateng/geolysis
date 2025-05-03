import pytest

from geolysis.bearing_capacity.abc.cohl import \
    create_allowable_bearing_capacity


class TestBowlesABC:
    @pytest.mark.parametrize(
        ["corrected_spt_n_value", "tol_settlement", "depth",
         "width", "footing_shape", "foundation_type", "expected"],
        [(12.0, 20.0, 1.5, 1.2, "square", "pad", 240.78),
         (12.0, 20.0, 1.5, 1.3, "square", "pad", 229.45)])
    def test_bowles_abc_4_pad_foundation(self, corrected_spt_n_value,
                                         tol_settlement,
                                         depth,
                                         width,
                                         footing_shape,
                                         foundation_type,
                                         expected):
        bowles = create_allowable_bearing_capacity(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="BOWLES")
        assert bowles.bearing_capacity() == pytest.approx(expected=expected,
                                                          rel=0.01)

    @pytest.mark.parametrize(
        ["corrected_spt_n_value", "tol_settlement", "depth",
         "width", "footing_shape", "foundation_type", "expected"],
        [(12.0, 20.0, 1.5, 1.2, "square", "mat", 150.55)])
    def test_bowles_abc_4_mat_foundation(self, corrected_spt_n_value,
                                         tol_settlement,
                                         depth,
                                         width,
                                         footing_shape,
                                         foundation_type,
                                         expected):
        bowles = create_allowable_bearing_capacity(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="BOWLES")
        assert bowles.bearing_capacity() == pytest.approx(expected=expected,
                                                          rel=0.01)
