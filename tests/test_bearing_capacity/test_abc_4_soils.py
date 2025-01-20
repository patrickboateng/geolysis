import pytest

from geolysis.bearing_capacity.abc.cohl import (BowlesABC4PadFoundation,
                                                BowlesABC4MatFoundation,
                                                MeyerhofABC4PadFoundation,
                                                MeyerhofABC4MatFoundation,
                                                TerzaghiABC4PadFoundation,
                                                TerzaghiABC4MatFoundation)
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
            "corrected_spt_n_value,tol_settlement,fs,r_val", 
            ((12.0, 20.0, dict(depth=1.5, width=1.2, shape="square"), 240.78),
             (12.0, 20.0, dict(depth=1.5, width=1.3, shape="square"), 229.45)))
    def test_bowles_abc_4_pad_foundation(self, corrected_spt_n_value, 
                                         tol_settlement, fs, r_val):
        fnd_size = create_foundation(**fs)
        bowles = BowlesABC4PadFoundation(corrected_spt_n_value, 
                                         tol_settlement, 
                                         foundation_size=fnd_size)
        assert bowles.bearing_capacity() == pytest.approx(expected=r_val,
                                                          rel=0.01)

    def test_bowles_abc_4_mat_foundation(self):
        bowles = BowlesABC4MatFoundation(**self.kwargs)
        assert bowles.bearing_capacity() == pytest.approx(expected=150.55,
                                                          rel=0.01)


class TestMeyerhofABC(SetUp):
    @pytest.mark.parametrize(
            "corrected_spt_n_value,tol_settlement,fs,r_val", 
            ((12.0, 20.0, dict(depth=1.5, width=1.2, shape="square"), 150.8),
             (12.0, 20.0, dict(depth=1.5, width=1.3, shape="square"), 153.22)))
    def test_meyerhof_abc_4_pad_foundation(self, corrected_spt_n_value, 
                                           tol_settlement, fs, r_val):
        fnd_size = create_foundation(**fs)
        meyerhof = MeyerhofABC4PadFoundation(corrected_spt_n_value, 
                                            tol_settlement, 
                                            foundation_size=fnd_size)
        assert meyerhof.bearing_capacity() == pytest.approx(expected=r_val,
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
            "corrected_spt_n_value,tol_settlement,ground_water_level,fs,r_val", 
            ((12.0, 20.0, 1.2, dict(depth=1.5, width=1.2, shape="square"), 65.97),
             (12.0, 20.0, 1.8, dict(depth=1.5, width=1.3, shape="square"), 70.35)))
    def test_terzaghi_abc_4_pad_foundation(self, corrected_spt_n_value,
                                           tol_settlement,
                                           ground_water_level,fs,r_val):
        fnd_size = create_foundation(**fs)
        terzaghi = TerzaghiABC4PadFoundation(corrected_spt_n_value,
                                             tol_settlement,
                                             ground_water_level,
                                             foundation_size=fnd_size)
        assert terzaghi.bearing_capacity() == pytest.approx(expected=r_val,
                                                            rel=0.01)

    def test_terzaghi_abc_4_mat_foundation(self):
        terzaghi = TerzaghiABC4MatFoundation(**self.kwargs)
        assert terzaghi.bearing_capacity() == pytest.approx(expected=43.98,
                                                            rel=0.01)
