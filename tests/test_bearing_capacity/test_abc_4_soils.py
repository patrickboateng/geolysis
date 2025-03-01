import pytest

from geolysis.bearing_capacity.abc.cohl import \
    create_allowable_bearing_capacity
from geolysis.utils import inf


def test_create_allowable_bearing_capacity_errors():
    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2,
                                          abc_type="HANSEN")

    with pytest.raises(ValueError):
        create_allowable_bearing_capacity(corrected_spt_n_value=12,
                                          tol_settlement=20,
                                          depth=1.5,
                                          width=1.2,
                                          foundation_type="COMBINED")


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
        assert bowles.bearing_capacity() == pytest.approx(expected=150.55,
                                                          rel=0.01)


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


class TestTerzaghiABC:

    @pytest.mark.parametrize(
        ["corrected_spt_n_value", "tol_settlement", "depth", "width",
         "ground_water_level", "footing_shape", "foundation_type", "expected"],
        [(12.0, 20.0, 1.5, 1.2, 1.2, "square", "pad", 65.97),
         (12.0, 20.0, 1.5, 1.2, inf, "square", "pad", 45.35),
         (12.0, 20.0, 1.5, 1.3, 1.8, "square", "pad", 70.35)])
    def test_terzaghi_abc_4_pad_foundation(self, corrected_spt_n_value,
                                           tol_settlement,
                                           depth,
                                           width,
                                           ground_water_level,
                                           footing_shape,
                                           foundation_type,
                                           expected):
        terzaghi = create_allowable_bearing_capacity(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            ground_water_level=ground_water_level,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="TERZAGHI")

        assert terzaghi.bearing_capacity() == pytest.approx(expected=expected,
                                                            rel=0.01)

    @pytest.mark.parametrize(
        ["corrected_spt_n_value", "tol_settlement", "depth", "width",
         "ground_water_level", "footing_shape", "foundation_type", "expected"],
        [(12.0, 20.0, 1.5, 1.2, 1.2, "square", "mat", 43.98)])
    def test_terzaghi_abc_4_mat_foundation(self, corrected_spt_n_value,
                                           tol_settlement,
                                           depth,
                                           width,
                                           ground_water_level,
                                           footing_shape,
                                           foundation_type,
                                           expected):
        terzaghi = create_allowable_bearing_capacity(
            corrected_spt_n_value=corrected_spt_n_value,
            tol_settlement=tol_settlement,
            depth=depth,
            width=width,
            ground_water_level=ground_water_level,
            shape=footing_shape,
            foundation_type=foundation_type,
            abc_type="TERZAGHI")

        assert terzaghi.bearing_capacity() == pytest.approx(expected=expected,
                                                            rel=0.01)
