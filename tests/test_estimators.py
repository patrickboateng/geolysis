import pytest

from geolysis.constants import ERROR_TOLERANCE
from geolysis.estimators import (
    CompressionIndexEst,
    SoilFrictionAngleEst,
    SoilUnitWeightEst,
    UndrainedShearStrengthEst,
)
from geolysis.exceptions import EstimatorError


class TestSoilUnitWeightEst:
    @classmethod
    def setup_class(cls):
        cls.suw = SoilUnitWeightEst(spt_n_60=13)

    def test_moist_wgt(self):
        assert self.suw.moist_wgt == 17.3

    def test_saturated_wgt(self):
        assert self.suw.saturated_wgt == 18.75

    def test_submerged_wgt(self):
        assert self.suw.submerged_wgt == 8.93


class TestCompressionIndexEst:
    @classmethod
    def setup_class(cls):
        cls.est_comp_idx = CompressionIndexEst()

    def test_terzaghi_et_al_ci(self):
        assert (
            self.est_comp_idx.terzaghi_et_al_ci_1967(liquid_limit=35) == 0.225
        )

    def test_skempton_ci(self):
        assert self.est_comp_idx.skempton_ci_1994(liquid_limit=35) == 0.175

    def test_hough_ci(self):
        assert self.est_comp_idx.hough_ci_1957(void_ratio=0.78) == 0.148


class TestSoilFrictionAngleEst:
    @classmethod
    def setup_class(cls):
        cls.est_sfa = SoilFrictionAngleEst()

    def test_wolff_sfa(self):
        assert self.est_sfa.wolff_sfa_1989(spt_n_60=50) == 40.75

    def test_kullhawy_mayne_sfa(self):
        assert (
            self.est_sfa.kullhawy_mayne_sfa_1990(
                spt_n_60=40,
                eop=103.8,
                atm_pressure=101.325,
            )
            == 46.874
        )

    def test_kullhawy_mayne_sfa_error(self):
        with pytest.raises(EstimatorError):
            self.est_sfa.kullhawy_mayne_sfa_1990(
                spt_n_60=40,
                eop=103.8,
                atm_pressure=0,
            )


class TestUndrainedShearStrengthEst:
    @classmethod
    def setup_class(cls):
        cls.est_uss = UndrainedShearStrengthEst()

    def test_stroud_uss(self):
        assert self.est_uss.stroud_uss_1974(spt_n_60=40) == 140

    def test_stroud_uss_error(self):
        with pytest.raises(EstimatorError):
            self.est_uss.stroud_uss_1974(spt_n_60=30, k=7)

    def test_skempton_uss(self):
        assert (
            self.est_uss.skempton_uss_1957(eop=108.3, plasticity_index=12)
            == 16.722
        )
