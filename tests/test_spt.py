from statistics import StatisticsError

import pytest

from geolysis.bearing_capacity.spt import (
    SPTCorrections,
    spt_n_design,
    spt_n_val,
)
from geolysis.constants import GeotechEng
from geolysis.exceptions import EngineerTypeError


def test_spt_n_design():
    assert spt_n_design([7.0, 15.0, 18.0]) == 9.0
    assert spt_n_design([7.0, 15.0, 18.0], t=True) == 7.0

    with pytest.raises(StatisticsError):
        spt_n_design([])


def test_spt_n_val():
    assert spt_n_val([8.0, 10.0, 14.0]) == 10.67

    with pytest.raises(StatisticsError):
        spt_n_val([])


class TestSPTCorrections:
    @classmethod
    def setup_class(cls):
        cls.spt_correction = SPTCorrections(
            eop=103.8,
            hammer_efficiency=0.6,
            borehole_diameter_correction=1,
            sampler_correction=1,
            rod_length_correction=0.85,
        )
        cls.recorded_spt_n_vals = {1.5: 10, 3.0: 20, 4.5: 25}

    def test_skempton_opc(self):
        corrected_spt_n_vals = self.spt_correction(
            self.recorded_spt_n_vals, eng=GeotechEng.SKEMPTON
        )
        assert corrected_spt_n_vals == [7.2, 14.4, 20.4]

    def test_gibbs_holtz_opc(self):
        corrected_spt_n_vals = self.spt_correction(
            self.recorded_spt_n_vals, eng=GeotechEng.GIBBS
        )
        assert corrected_spt_n_vals == [7.55, 15.1, 21.4]

    def test_peck_et_al(self):
        corrected_spt_n_vals = self.spt_correction(
            self.recorded_spt_n_vals, eng=GeotechEng.PECK
        )
        assert corrected_spt_n_vals == [7.42, 14.84, 21.02]

    def test_liao_whitman_opc(self):
        corrected_spt_n_vals = self.spt_correction(
            self.recorded_spt_n_vals, eng=GeotechEng.LIAO
        )
        assert corrected_spt_n_vals == [7.36, 14.72, 20.86]

    def test_bazaraa_peck_opc(self):
        corrected_spt_n_vals = self.spt_correction(
            self.recorded_spt_n_vals, eng=GeotechEng.BAZARAA
        )
        assert corrected_spt_n_vals == [6.93, 13.86, 19.63]

    def test_exception(self):
        with pytest.raises(EngineerTypeError):
            self.spt_correction(self.recorded_spt_n_vals, eng=GeotechEng.HOUGH)

    @pytest.mark.parametrize(
        ("recorded_spt_nval", "n60"),
        ((15, 12.75), (8, 6.8), (7, 5.95), (26, 22.1)),
    )
    def test_spt_n60(self, recorded_spt_nval, n60):
        assert self.spt_correction.spt_n_60(recorded_spt_nval) == n60

    @pytest.mark.parametrize(("corr_spt_n_val", "exp"), ((15, 15), (30, 22.5)))
    def test_dilatancy_correction(self, corr_spt_n_val, exp):
        assert self.spt_correction.dilatancy_correction(corr_spt_n_val) == exp

    # def test_overburden_pressure(self):
    #     # Gibbs and Holtz (1957)
    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=103.8, eng=GeotechEng.GIBBS
    #     ) == pytest.approx(12.84, ERROR_TOLERANCE)

    #     with pytest.raises(ValueError):
    #         self.spt_correction.overburden_pressure_correction(
    #             spt_n_60=15, eop=300, eng=GeotechEng.GIBBS
    #         )

    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=200, eng=GeotechEng.GIBBS
    #     ) == pytest.approx(16.53, ERROR_TOLERANCE)

    #     # Peck et al (1974)
    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=103.8, eng=GeotechEng.PECK
    #     ) == pytest.approx(12.61, ERROR_TOLERANCE)

    #     with pytest.raises(ValueError):
    #         self.spt_correction.overburden_pressure_correction(
    #             spt_n_60=15, eop=20, eng=GeotechEng.PECK
    #         )

    #     # Liao and Whitman (1986)
    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=103.8, eng=GeotechEng.LIAO
    #     ) == pytest.approx(12.51, ERROR_TOLERANCE)

    #     # Skempton (1986)
    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=103.8, eng=GeotechEng.SKEMPTON
    #     ) == pytest.approx(12.24, ERROR_TOLERANCE)

    #     # Bazaraa and Peck (1969)
    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=71.8, eng=GeotechEng.BAZARAA
    #     ) == pytest.approx(12.75, ERROR_TOLERANCE)

    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=60.8, eng=GeotechEng.BAZARAA
    #     ) == pytest.approx(14.4, ERROR_TOLERANCE)

    #     assert self.spt_correction.overburden_pressure_correction(
    #         spt_n_60=15, eop=103.8, eng=GeotechEng.BAZARAA
    #     ) == pytest.approx(11.78, ERROR_TOLERANCE)

    #     with pytest.raises(EngineerTypeError):
    #         self.spt_correction.overburden_pressure_correction(
    #             spt_n_60=15, eop=103.8, eng=GeotechEng.KULLHAWY
    #         )
