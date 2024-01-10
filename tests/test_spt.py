from statistics import StatisticsError

import pytest

from geolysis import GeotechEng
from geolysis.spt import (
    OverburdenPressureError,
    SPTCorrections,
    avg_uncorrected_spt_n_val,
    spt_n_60,
    weighted_avg_spt_n_val,
)

from geolysis.constants import EngineerTypeError


def test_wgted_avg_spt_n_val():
    assert weighted_avg_spt_n_val([7.0, 15.0, 18.0]) == 9.0


def test_wgted_avg_spt_n_val_error():
    with pytest.raises(StatisticsError):
        weighted_avg_spt_n_val([])


def test_avg_uncorrected_spt_n_val():
    assert avg_uncorrected_spt_n_val([8.0, 10.0, 14.0]) == 11


def test_spt_n_val_error():
    with pytest.raises(StatisticsError):
        avg_uncorrected_spt_n_val([])


def test_spt_n_60():
    assert spt_n_60(15) == 11.25


class TestSPTCorrections:
    @classmethod
    def setup_class(cls):
        cls.std_spt_n_vals = [7.5, 15.0, 22.5, 30.0, 37.5]

    def test_opcs_gibbs(self):
        opcs = SPTCorrections().overburden_pressure_correction(
            std_spt_n_vals=self.std_spt_n_vals,
            eop=100,
            eng=GeotechEng.GIBBS,
        )
        assert opcs == [7.72, 15.44, 23.16, 30.88, 38.6]

    def test_opcs_peck(self):
        opcs = SPTCorrections().overburden_pressure_correction(
            std_spt_n_vals=self.std_spt_n_vals,
            eop=100,
            eng=GeotechEng.PECK,
        )
        assert opcs == [7.51, 15.03, 22.54, 30.05, 37.57]

    def test_opcs_liao(self):
        opcs = SPTCorrections().overburden_pressure_correction(
            std_spt_n_vals=self.std_spt_n_vals,
            eop=100,
            eng=GeotechEng.LIAO,
        )
        assert opcs == [7.5, 15, 22.5, 30, 37.5]

    def test_opcs_skempton(self):
        opcs = SPTCorrections().overburden_pressure_correction(
            std_spt_n_vals=self.std_spt_n_vals,
            eop=100,
            eng=GeotechEng.SKEMPTON,
        )
        assert opcs == [7.34, 14.68, 22.02, 29.35, 36.69]

    def test_opcs_bazaraa(self):
        opcs = SPTCorrections().overburden_pressure_correction(
            std_spt_n_vals=self.std_spt_n_vals,
            eop=100,
            eng=GeotechEng.BAZARAA,
        )
        assert opcs == [6.99, 13.99, 20.98, 27.97, 34.97]

    def test_opcs_error(self):
        with pytest.raises(EngineerTypeError):
            SPTCorrections().overburden_pressure_correction(
                std_spt_n_vals=self.std_spt_n_vals,
                eop=100,
                eng=GeotechEng.STROUD,
            )

    def test_dilatancy_correction(self):
        dcs = SPTCorrections().dilatancy_correction(
            corrected_spt_n_vals=[7.34, 14.68, 22.02, 29.35, 36.69]
        )
        assert dcs == [7.34, 14.68, 18.51, 22.18, 25.84]

    @pytest.mark.parametrize(
        ("spt_n_60", "eop", "corr"),
        ((20, 150, 31.82), (20, 80, 23.33)),
    )
    def test_gibbs_holtz_opc(self, spt_n_60, eop, corr):
        opc = SPTCorrections.gibbs_holtz_opc_1957(spt_n_60=spt_n_60, eop=eop)
        assert opc == corr

    @pytest.mark.parametrize(
        ("spt_n_60", "eop"),
        ((20, 0), (20, 300)),
    )
    def test_gibbs_holtz_opc_error(self, spt_n_60, eop):
        with pytest.raises(OverburdenPressureError):
            SPTCorrections.gibbs_holtz_opc_1957(spt_n_60=spt_n_60, eop=eop)

    def test_peck_et_al_opc(self):
        opc = SPTCorrections.peck_et_al_opc_1974(spt_n_60=20, eop=50)
        assert opc == 24.67

    @pytest.mark.parametrize(
        ("spt_n_60", "eop"),
        ((20, 0), (20, 20)),
    )
    def test_peck_et_al_opc_error(self, spt_n_60, eop):
        with pytest.raises(OverburdenPressureError):
            SPTCorrections.peck_et_al_opc_1974(spt_n_60=spt_n_60, eop=eop)

    def test_liao_whitman_opc(self):
        opc = SPTCorrections.liao_whitman_opc_1986(spt_n_60=20, eop=50)
        assert opc == 28.28

    def test_liao_whitman_opc_error(self):
        with pytest.raises(OverburdenPressureError):
            SPTCorrections.liao_whitman_opc_1986(spt_n_60=20, eop=0)

    def test_skempton_opc(self):
        opc = SPTCorrections.skempton_opc_1986(spt_n_60=20, eop=50)
        assert opc == 26.28

    @pytest.mark.parametrize(
        ("spt_n_60", "eop", "corr"),
        ((20, 71.8, 20), (20, 60, 22.81), (20, 80, 19.6)),
    )
    def test_bazaraa_peck_opc(self, spt_n_60, eop, corr):
        opc = SPTCorrections.bazaraa_peck_opc_1969(spt_n_60=spt_n_60, eop=eop)
        assert opc == corr
