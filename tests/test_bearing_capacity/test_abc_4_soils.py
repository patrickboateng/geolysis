import pytest

from geolysis.bearing_capacity.abc_4_soils import (BowlesABC4PadFoundation,
                                                   BowlesABC4MatFoundation,
                                                   MeyerhofABC4PadFoundation,
                                                   MeyerhofABC4MatFoundation,
                                                   TerzaghiABC4PadFoundation,
                                                   TerzaghiABC4MatFoundation)
from geolysis.foundation import create_foundation


class SetUp:
    @classmethod
    def setup_class(cls):
        fs = create_foundation(depth=1.5, width=1.2, footing_shape="square")
        cls.kwargs = {"corrected_spt_number": 12.0, "tol_settlement": 20.0,
                      "foundation_size": fs}


class TestBowlesABC(SetUp):

    def test_bowles_abc_4_pad_foundation(self):
        bowles = BowlesABC4PadFoundation(**self.kwargs)
        assert bowles.bearing_capacity() == pytest.approx(expected=240.78,
                                                          rel=0.01)

    def test_bowles_abc_4_mat_foundation(self):
        bowles = BowlesABC4MatFoundation(**self.kwargs)
        assert bowles.bearing_capacity() == pytest.approx(expected=150.55,
                                                          rel=0.01)


class TestMeyerhofABC(SetUp):
    def test_meyerhof_abc_4_pad_foundation(self):
        meyerhof = MeyerhofABC4PadFoundation(**self.kwargs)
        assert meyerhof.bearing_capacity() == pytest.approx(expected=150.8,
                                                            rel=0.01)

    def test_meyerhof_abc_4_mat_foundation(self):
        meyerhof = MeyerhofABC4MatFoundation(**self.kwargs)
        assert meyerhof.bearing_capacity() == pytest.approx(expected=100.54,
                                                            rel=0.01)


class TestTerzaghiABC(SetUp):

    @classmethod
    def setup_class(cls):
        super().setup_class()
        cls.kwargs["water_depth"] = 1.2

    def test_terzaghi_abc_4_pad_foundation(self):
        terzaghi = TerzaghiABC4PadFoundation(**self.kwargs)
        assert terzaghi.bearing_capacity() == pytest.approx(expected=65.97,
                                                            rel=0.01)

    def test_terzaghi_abc_4_mat_foundation(self):
        terzaghi = TerzaghiABC4MatFoundation(**self.kwargs)
        assert terzaghi.bearing_capacity() == pytest.approx(expected=43.98,
                                                            rel=0.01)
