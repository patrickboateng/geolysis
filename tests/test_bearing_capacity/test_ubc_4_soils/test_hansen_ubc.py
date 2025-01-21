import pytest

from geolysis.bearing_capacity.ubc import (HansenBearingCapacityFactor,
                                           HansenUltimateBearingCapacity)
from geolysis.foundation import create_foundation


class TestHansenBCF:
    @pytest.mark.parametrize("f_angle, expected",
                             [(0.0, 5.14),
                              (10.0, 8.34),
                              (20.0, 14.84),
                              (35.0, 46.13)])
    def test_n_c(self, f_angle, expected):
        nc = HansenBearingCapacityFactor.n_c(f_angle)
        assert nc == pytest.approx(expected, 0.01)

    @pytest.mark.parametrize("f_angle, expected",
                             [(0.0, 1.00),
                              (10.0, 2.47),
                              (20.0, 6.4),
                              (35.0, 33.29)])
    def test_n_q(self, f_angle, expected):
        nq = HansenBearingCapacityFactor.n_q(f_angle)
        assert nq == pytest.approx(expected, 0.01)

    @pytest.mark.parametrize("f_angle, expected",
                             [(0.0, 0.00),
                              (10.0, 0.47),
                              (20.0, 3.54),
                              (35.0, 40.69)])
    def test_n_gamma(self, f_angle, expected):
        ngamma = HansenBearingCapacityFactor.n_gamma(f_angle)
        assert ngamma == pytest.approx(expected, 0.01)


class TestHansenUBC:
    def test_bearing_capacity(self):
        fs = create_foundation(depth=1.5, width=2.0, shape="square")
        ubc = HansenUltimateBearingCapacity(friction_angle=20.0,
                                            cohesion=20.0,
                                            moist_unit_wgt=18.0,
                                            foundation_size=fs)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(798.41, 0.01)
