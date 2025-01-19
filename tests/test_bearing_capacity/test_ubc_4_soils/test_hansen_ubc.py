import pytest

from geolysis.bearing_capacity.ubc import (HansenBearingCapacityFactor,
                                                   HansenUltimateBearingCapacity)
from geolysis.foundation import create_foundation

ERROR_TOL = 0.01


class TestHansenBCF:
    @pytest.mark.parametrize("f_angle, r_value",
                             ((0, 5.14), 
                              (10, 8.34), 
                              (20, 14.84), 
                              (35, 46.13)))
    def test_n_c(self, f_angle, r_value):
        nc = HansenBearingCapacityFactor.n_c(f_angle)
        assert nc == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize("f_angle, r_value",
                             ((0, 1.00), 
                              (10, 2.47), 
                              (20, 6.4), 
                              (35, 33.29)))
    def test_n_q(self, f_angle, r_value):
        nq = HansenBearingCapacityFactor.n_q(f_angle)
        assert nq == pytest.approx(r_value, ERROR_TOL)

    @pytest.mark.parametrize("f_angle, r_value",
                             ((0, 0.00), (10, 0.47), (20, 3.54), (35, 40.69)))
    def test_n_gamma(self, f_angle, r_value):
        ngamma = HansenBearingCapacityFactor.n_gamma(f_angle)
        assert ngamma == pytest.approx(r_value, ERROR_TOL)


class TestHansenUBC:
    def test_bearing_capacity(self):
        fs = create_foundation(depth=1.5, width=2.0, shape="square")
        prop = dict(friction_angle=20.0, cohesion=20.0, moist_unit_wgt=18.0)
        ubc = HansenUltimateBearingCapacity(soil_properties=prop,
                                            foundation_size=fs)
        actual = ubc.bearing_capacity()
        assert actual == pytest.approx(798.41, ERROR_TOL)
