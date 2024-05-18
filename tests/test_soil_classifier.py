import unittest
from typing import Sequence

import pytest

from geolysis.core.soil_classifier import AASHTO, PSD, USCS
from geolysis.core.soil_classifier import AtterbergLimits as AL
from geolysis.core.soil_classifier import PSDAggSumError


class TestAL(unittest.TestCase):

    def setUp(self) -> None:
        self.atterberg_limits = AL(liquid_limit=25, plastic_limit=15)

    def testPlasticityIndex(self):
        plasticity_index = self.atterberg_limits.plasticity_index
        self.assertAlmostEqual(plasticity_index, 10)

    def testLiquidityIndex(self):
        liquidity_index = self.atterberg_limits.liquidity_index(nmc=20)
        self.assertAlmostEqual(liquidity_index, 50)

    def testConsistencyIndex(self):
        consistency_index = self.atterberg_limits.consistency_index(nmc=20)
        self.assertAlmostEqual(consistency_index, 50)


class TestPSD(unittest.TestCase):

    def setUp(self) -> None:
        self.psd = PSD(
            fines=0, sand=0, gravel=100, d_10=0.115, d_30=0.53, d_60=1.55
        )

    def testCoeffOfUniformity(self):
        self.assertAlmostEqual(self.psd.coeff_of_uniformity, 13.4783)

    def testCoeffOfCurvature(self):
        self.assertAlmostEqual(self.psd.coeff_of_curvature, 1.5759)

    def testPSDError(self):
        with self.assertRaises(PSDAggSumError):
            PSD(fines=30, sand=30, gravel=30)


class TestAASHTO:
    @pytest.mark.parametrize(
        "soil_params,clf",
        [
            ((30, 5, 10), "A-1-a(0)"),
            ((17.9, 3.4, 24.01), "A-1-b(0)"),
            ((0, 0, 9.5), "A-3(0)"),
            ((30.2, 6.3, 11.18), "A-2-4(0)"),
            ((30.1, 13.7, 18.38), "A-2-6(0)"),
            ((35, 7, 40), "A-4(1)"),
            ((48, 9, 40), "A-5(1)"),
            ((37.7, 13.9, 47.44), "A-6(4)"),
            ((61.7, 29.4, 52.09), "A-7-5(12)"),
            ((70.0, 32.0, 86), "A-7-5(20)"),
            ((52.6, 25.0, 45.8), "A-7-6(7)"),
            ((45, 29, 60), "A-7-6(13)"),
        ],
    )
    def test_aashto_with_grp_idx(self, soil_params: Sequence, clf: str):
        asshto_classifier = AASHTO(*soil_params)
        assert asshto_classifier.soil_class == clf

    @pytest.mark.parametrize(
        "soil_params,clf",
        [
            ((0, 0, 9.5), "A-3"),
            ((43, 8, 30), "A-2-5"),
            ((43, 18, 30), "A-2-7"),
            ((35, 7, 40), "A-4"),
        ],
    )
    def test_aashto_without_grp_idx(self, soil_params: Sequence, clf: str):
        asshto_classifier = AASHTO(*soil_params)
        asshto_classifier.add_group_idx = False
        assert asshto_classifier.soil_class == clf


class TestUSCS:
    @pytest.mark.parametrize(
        "al,psd,size_dist,clf",
        [
            ((30.8, 20.7), (10.29, 81.89, 7.83), (0.07, 0.3, 0.8), "SW-SC"),
            ((24.4, 14.7), (9.77, 44.82, 45.41), (0.06, 0.6, 7), "GP-GC"),
            ((49.5, 33.6), (6.93, 91.79, 1.28), (0.153, 0.4, 1.2), "SP-SM"),
            ((30.33, 23.42), (8.93, 7.69, 83.38), (0.15, 18, 44), "GP-GM"),
            ((35.32, 25.57), (9.70, 5.63, 84.67), (0.06, 50, 55), "GP-GM"),
            ((26.17, 19.69), (12.00, 8.24, 79.76), (0.07, 15, 52), "GP-GC"),
            ((30.59, 24.41), (9.87, 19.03, 71.1), (0.07, 0.3, 0.8), "GW-GM"),
            ((32.78, 22.99), (3.87, 15.42, 80.71), (2.5, 6, 15), "GP"),
        ],
    )
    def test_dual_classification(
        self,
        al: Sequence,
        psd: Sequence,
        size_dist: Sequence,
        clf: str,
    ):
        uscs = USCS(
            *al, *psd, d_10=size_dist[0], d_30=size_dist[1], d_60=size_dist[2]
        )
        assert uscs.soil_class == clf

    @pytest.mark.parametrize(
        "al,psd,clf",
        [
            ((30.8, 20.7), (10.29, 81.89, 7.83), "SW-SC,SP-SC"),
            ((24.4, 14.7), (9.77, 44.82, 45.41), "GW-GC,GP-GC"),
            ((49.5, 33.6), (6.93, 91.79, 1.28), "SW-SM,SP-SM"),
            ((30.33, 23.42), (8.93, 7.69, 83.38), "GW-GM,GP-GM"),
            ((35.32, 25.57), (9.70, 5.63, 84.67), "GW-GM,GP-GM"),
            ((26.17, 19.69), (12.00, 8.24, 79.76), "GW-GC,GP-GC"),
            ((32.78, 22.99), (3.87, 15.42, 80.71), "GW,GP"),
        ],
    )
    def test_dual_classification_no_psd_coeff(
        self,
        al: Sequence,
        psd: Sequence,
        clf: str,
    ):
        uscs = USCS(*al, *psd)
        assert uscs.soil_class == clf

    @pytest.mark.parametrize(
        "al,psd,clf",
        [
            ((34.1, 21.1), (47.88, 37.84, 14.28), "SC"),
            ((27.5, 13.8), (54.23, 45.69, 0.08), "CL"),
            ((27.7, 22.7), (18.95, 77.21, 3.84), "SM-SC"),
            ((64.1, 29), (57.17, 42.58, 0.25), "CH"),
            ((56, 32.4), (51.11, 46.87, 2.02), "MH"),
            ((70, 38), (86, 7, 7), "MH"),
            ((26.4, 19.4), (54.76, 45.24, 0), "ML-CL"),
            ((33, 21), (30, 30, 40), "GC"),
            ((34.46, 23.85), (18.09, 18.7, 63.21), "GC"),
            ((45, 16), (59, 41, 0), "CL"),
            ((55, 40), (85, 15, 0), "MH"),
            ((49.93, 37.22), (49.4, 35.98, 14.62), "SM"),
            ((42.77, 29.98), (27.6, 27.93, 44.47), "GM"),
            ((35.83, 25.16), (68.94, 28.88, 2.18), "ML"),
        ],
    )
    def test_single_classification(
        self,
        al: Sequence,
        psd: Sequence,
        clf: str,
    ):
        uscs = USCS(*al, *psd)
        assert uscs.soil_class == clf

    def test_organic_soils_low_plasticity(self):
        uscs = USCS(
            liquid_limit=35.83,
            plastic_limit=25.16,
            fines=68.94,
            sand=28.88,
            gravel=2.18,
            organic=True,
        )
        assert uscs.soil_class == "OL"

    def test_organic_soils_high_plasticity(self):
        uscs = USCS(
            liquid_limit=55.0,
            plastic_limit=40.0,
            fines=85,
            sand=15,
            gravel=0,
            organic=True,
        )

        assert uscs.soil_class == "OH"
