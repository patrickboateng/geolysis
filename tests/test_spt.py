import unittest
import pytest

from geolysis.spt import (EnergyCorrection,
                          BazaraaPeckOPC,
                          DilatancyCorrection,
                          GibbsHoltzOPC,
                          LiaoWhitmanOPC,
                          SkemptonOPC,
                          PeckOPC,
                          SPTNDesign,
                          HammerType,
                          SamplerType)


class TestSPTDesign:

    def test_spt_n_design(self):
        spt_design = SPTNDesign([7.0, 15.0, 18])

        assert spt_design.minimum_spt_n_design() == pytest.approx(7.0)
        assert spt_design.average_spt_n_design() == pytest.approx(13.3)
        assert spt_design.weighted_spt_n_design() == pytest.approx(9.4)

    def test_errors(self):
        with pytest.raises(ValueError):
            SPTNDesign(corrected_spt_n_values=[])


class TestEnergyCorrection:

    @pytest.mark.parametrize(
        ["rec_spt_n_val", "energy_percentage", "borehole_diameter",
         "rod_len", "hammer_type", "sampler_type", "expected"],
        [(30, 0.6, 65.0, 3, HammerType.DONUT_1, SamplerType.STANDARD, 22.5),
         (30, 0.6, 120.0, 5, HammerType.AUTOMATIC, SamplerType.NON_STANDARD,
          37.5),
         (30, 0.6, 170.0, 7, HammerType.DONUT_2, SamplerType.STANDARD, 27.3),
         (30, 0.6, 65.0, 12, HammerType.SAFETY, SamplerType.STANDARD, 27.5)])
    def test_energy_correction(self, rec_spt_n_val,
                               energy_percentage,
                               borehole_diameter,
                               rod_len,
                               hammer_type,
                               sampler_type,
                               expected):
        energy_corr = EnergyCorrection(recorded_spt_n_value=rec_spt_n_val,
                                       energy_percentage=energy_percentage,
                                       borehole_diameter=borehole_diameter,
                                       rod_length=rod_len,
                                       hammer_type=hammer_type,
                                       sampler_type=sampler_type)

        assert energy_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestGibbsHoltzOPC:

    @pytest.mark.parametrize(["std_spt_n_value", "eop", "expected"],
                             [(22.5, 100.0, 23.2)])
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = GibbsHoltzOPC(std_spt_n_value=std_spt_n_value, eop=eop)
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestBazaraaPeckOPC:

    @pytest.mark.parametrize(["std_spt_n_value", "eop", "expected"],
                             [(11.4, 54.8, 13.9),
                              (22.5, 100.0, 21.0),
                              (22.5, 71.8, 22.5)])
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = BazaraaPeckOPC(std_spt_n_value=std_spt_n_value, eop=eop)
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestPeckOPC:

    @pytest.mark.parametrize(["std_spt_n_value", "eop", "expected"],
                             [(22.5, 100.0, 22.5)])
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = PeckOPC(std_spt_n_value=std_spt_n_value, eop=eop)
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestLiaoWhitmanOPC:

    @pytest.mark.parametrize(["std_spt_n_value", "eop", "expected"],
                             [(22.5, 100.0, 22.5)])
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = LiaoWhitmanOPC(std_spt_n_value=std_spt_n_value, eop=eop)
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestSkemptonOPC:
    @pytest.mark.parametrize(["std_spt_n_value", "eop", "expected"],
                             [(22.5, 100.0, 22.0)])
    def test_correction(self, std_spt_n_value, eop, expected):
        opc_corr = SkemptonOPC(std_spt_n_value=std_spt_n_value, eop=eop)
        assert opc_corr.corrected_spt_n_value() == pytest.approx(expected)


class TestDilatancyCorrection:

    @pytest.mark.parametrize(["std_spt_n_value", "expected"],
                             [(22.5, 18.8), (12.6, 12.6)])
    def test_correction(self, std_spt_n_value, expected):
        corr = DilatancyCorrection(std_spt_n_value=std_spt_n_value)
        assert corr.corrected_spt_n_value() == pytest.approx(expected)
