import pytest

from geolysis.bearing_capacity.abc.cohl import \
    create_allowable_bearing_capacity


class TestMeyerhofABC:
    @pytest.mark.parametrize(
        ["corrected_spt_n_value", "tol_settlement", "depth",
         "width", "footing_shape", "foundation_type", "expected"],
        [(12.0, 20.0, 1.5, 1.2, "square", "pad", 150.8),
         (12.0, 20.0, 1.5, 1.3, "square", "pad", 153.22)])
    def test_meyerhof_abc_4_pad_foundation(self, corrected_spt_n_value,
                                           tol_settlement,
                                           depth,
                                           width,
                                           footing_shape,
                                           foundation_type,
                                           expected):
        meyerhof = create_allowable_bearing_capacity(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="MEYERHOF")
        assert meyerhof.bearing_capacity() == pytest.approx(expected=expected,
                                                            rel=0.01)

    @pytest.mark.parametrize(
        ["corrected_spt_n_value", "tol_settlement", "depth",
         "width", "footing_shape", "foundation_type", "expected"],
        [(12.0, 20.0, 1.5, 1.2, "square", "mat", 100.54)])
    def test_meyerhof_abc_4_mat_foundation(self, corrected_spt_n_value,
                                           tol_settlement,
                                           depth,
                                           width,
                                           footing_shape,
                                           foundation_type,
                                           expected):
        meyerhof = create_allowable_bearing_capacity(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="MEYERHOF")
        assert meyerhof.bearing_capacity() == pytest.approx(expected=100.54,
                                                            rel=0.01)
