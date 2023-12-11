import pytest

from geolysis import ERROR_TOLERANCE, GeotechEng
from geolysis.bearing_capacity.spt import SPTCorrections, n_design


def test_n_design():
    assert n_design([7, 15, 18]) == pytest.approx(9.37, ERROR_TOLERANCE)


class TestSPTCorrections:
    @classmethod
    def setup_class(cls):
        cls.spt_correction = SPTCorrections(
            hammer_efficiency=0.6,
            borehole_diameter_correction=1,
            sampler_correction=1,
            rod_length_correction=0.85,
        )

    def test_spt_n60(self):
        assert self.spt_correction.spt_n60(15) == pytest.approx(
            12.75, ERROR_TOLERANCE
        )

    def test_overburden_pressure(self):
        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.GIBBS
        ) == pytest.approx(12.84, ERROR_TOLERANCE)

        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.PECK
        ) == pytest.approx(12.61, ERROR_TOLERANCE)

        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.LIAO
        ) == pytest.approx(12.51, ERROR_TOLERANCE)

        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.SKEMPTON
        ) == pytest.approx(12.24, ERROR_TOLERANCE)

        assert self.spt_correction.overburden_pressure_correction(
            recorded_spt_nval=15, eop=103.8, eng=GeotechEng.BAZARAA
        ) == pytest.approx(11.78, ERROR_TOLERANCE)

    def test_dilatancy_correction(self):
        assert self.spt_correction.dilatancy_correction(
            recorded_spt_nval=15
        ) == pytest.approx(12.75, ERROR_TOLERANCE)
