import pytest

from geolysis.bearing_capacity.abc.cohl import (
    BowlesABC4MatFoundation, BowlesABC4PadFoundation,
    MeyerhofABC4MatFoundation, TerzaghiABC4MatFoundation,
    create_allowable_bearing_capacity, create_foundation)
from geolysis.foundation import create_foundation


class SetUp:
    @classmethod
    def setup_class(cls):
        fs = create_foundation(depth=1.5, width=1.2, shape="square")
        cls.kwargs = {"corrected_spt_n_value": 12.0,
                      "tol_settlement": 20.0,
                      "foundation_size": fs}


class TestBowlesABC(SetUp):
    @pytest.mark.parametrize(
        "corrected_spt_n_value,tol_settlement,fs,expected",
        [(12.0, 20.0, dict(depth=1.5, width=1.2, shape="square"), 240.78),
         (12.0, 20.0, dict(depth=1.5, width=1.3, shape="square"), 229.45)])
    def test_bowles_abc_4_pad_foundation(self, corrected_spt_n_value,
                                         tol_settlement, fs, expected):
        bowles = create_allowable_bearing_capacity(corrected_spt_n_value,
                                                   tol_settlement, **fs,
                                                   abc_type="BOWLES")
        assert bowles.bearing_capacity() == pytest.approx(expected=expected,
                                                          rel=0.01)

    def test_bowles_abc_4_mat_foundation(self):
        bowles = BowlesABC4MatFoundation(**self.kwargs)
        assert bowles.bearing_capacity() == pytest.approx(expected=150.55,
                                                          rel=0.01)


class TestMeyerhofABC(SetUp):
    @pytest.mark.parametrize(
        "corrected_spt_n_value,tol_settlement,fs,expected",
        [(12.0, 20.0, dict(depth=1.5, width=1.2, shape="square"), 150.8),
         (12.0, 20.0, dict(depth=1.5, width=1.3, shape="square"), 153.22)])
    def test_meyerhof_abc_4_pad_foundation(self, corrected_spt_n_value,
                                           tol_settlement, fs, expected):
        meyerhof = create_allowable_bearing_capacity(corrected_spt_n_value,
                                                     tol_settlement, **fs,
                                                     abc_type="MEYERHOF")
        assert meyerhof.bearing_capacity() == pytest.approx(expected=expected,
                                                            rel=0.01)

    def test_meyerhof_abc_4_mat_foundation(self):
        meyerhof = MeyerhofABC4MatFoundation(**self.kwargs)
        assert meyerhof.bearing_capacity() == pytest.approx(expected=100.54,
                                                            rel=0.01)


class TestTerzaghiABC(SetUp):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.kwargs["ground_water_level"] = 1.2

    @pytest.mark.parametrize(
        "corrected_spt_n_value,tol_settlement,ground_water_level,fs,expected",
        ((12.0, 20.0, 1.2, dict(depth=1.5, width=1.2, shape="square"), 65.97),
         (12.0, 20.0, 1.8, dict(depth=1.5, width=1.3, shape="square"), 70.35)))
    def test_terzaghi_abc_4_pad_foundation(self, corrected_spt_n_value,
                                           tol_settlement,
                                           ground_water_level, fs, expected):
        terzaghi = create_allowable_bearing_capacity(
            corrected_spt_n_value,
            tol_settlement, **fs,
            ground_water_level=ground_water_level,
            abc_type="TERZAGHI")

        assert terzaghi.bearing_capacity() == pytest.approx(expected=expected,
                                                            rel=0.01)

    # def test_terzaghi_abc_4_mat_foundation(self):
    #     terzaghi = TerzaghiABC4MatFoundation(**self.kwargs)
    #     assert terzaghi.bearing_capacity() == pytest.approx(expected=43.98,
    #                                                         rel=0.01)
