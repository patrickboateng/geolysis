import unittest

import pytest

from geolysis.soil_classifier import (PSD, AtterbergLimits, _SizeDistribution,
                                      create_soil_classifier)


def test_create_soil_classifier():
    with pytest.raises(ValueError):
        create_soil_classifier(liquid_limit=30.4,
                               plastic_limit=15.9,
                               fines=40.20)

    with pytest.raises(ValueError):
        create_soil_classifier(liquid_limit=30.4,
                               plastic_limit=15.9,
                               fines=40.20,
                               clf_type="IS")

    with pytest.raises(ValueError):
        create_soil_classifier(liquid_limit=30.4,
                               plastic_limit=15.9,
                               fines=40.20,
                               clf_type="USCS")


class TestAtterbergLimits:
    @pytest.mark.parametrize(["liquid_lmt", "plastic_lmt", "expected"],
                             [(25.0, 15.0, 10.0)])
    def test_plasticity_idx(self, liquid_lmt: float,
                            plastic_lmt: float,
                            expected: float):
        al = AtterbergLimits(liquid_limit=liquid_lmt,
                             plastic_limit=plastic_lmt)
        assert al.plasticity_index == pytest.approx(expected)

    @pytest.mark.parametrize(["liquid_lmt", "plastic_lmt", "nmc", "expected"],
                             [(25.0, 15.0, 20.0, 50.0)])
    def test_liquidity_idx(self, liquid_lmt: float,
                           plastic_lmt: float,
                           nmc: float,
                           expected: float):
        al = AtterbergLimits(liquid_limit=liquid_lmt,
                             plastic_limit=plastic_lmt)
        assert al.liquidity_index(nmc=nmc) == pytest.approx(expected)

    @pytest.mark.parametrize(["liquid_lmt", "plastic_lmt", "nmc", "expected"],
                             [(25.0, 15.0, 20.0, 50.0)])
    def test_consistency_idx(self, liquid_lmt: float,
                             plastic_lmt: float,
                             nmc: float,
                             expected: float):
        al = AtterbergLimits(liquid_limit=liquid_lmt,
                             plastic_limit=plastic_lmt)
        assert al.consistency_index(nmc=nmc) == pytest.approx(expected)

    def test_errors(self):
        with pytest.raises(ValueError):
            AtterbergLimits(liquid_limit=15.0, plastic_limit=25.0)

    # def test_plasticity_index(self):
    #     self.assertAlmostEqual(self.al.plasticity_index, 10.0)
    #
    # def test_liquidity_index(self):
    #     self.assertAlmostEqual(self.al.liquidity_index(nmc=20), 50.0)
    #
    # def test_consistency_index(self):
    #     self.assertAlmostEqual(self.al.consistency_index(nmc=20), 50.0)
    #


class TestPSD:
    # def setUp(self) -> None:
    #     size_dist = _SizeDistribution(0.115, 0.53, 1.55)
    #     self.psd = PSD(fines=0.0, sand=0.0, size_dist=size_dist)

    @pytest.mark.parametrize(
        ["fines", "sand", "d_10", "d_30", "d_60", "expected"],
        [(0.0, 0.0, 0.115, 0.53, 1.55, 13.48)])
    def test_coeff_of_uniformity(self, fines,
                                 sand,
                                 d_10, d_30, d_60,
                                 expected):
        psd = PSD(fines=fines, sand=sand, d_10=d_10, d_30=d_30, d_60=d_60)
        assert psd.coeff_of_uniformity == pytest.approx(expected)

    @pytest.mark.parametrize(
        ["fines", "sand", "d_10", "d_30", "d_60", "expected"],
        [(0.0, 0.0, 0.115, 0.53, 1.55, 1.58)])
    def test_coeff_of_curvature(self, fines,
                                sand,
                                d_10, d_30, d_60,
                                expected):
        psd = PSD(fines=fines, sand=sand, d_10=d_10, d_30=d_30, d_60=d_60)
        assert psd.coeff_of_curvature == pytest.approx(expected)


class TestAASHTO:
    @pytest.mark.parametrize(["al", "fines", "expected"],
                             [((30, 25), 10, "A-1-a(0)"),
                              ((17.9, 14.5), 24.01, "A-1-b(0)"),
                              ((0, 0), 9.5, "A-3(0)"),
                              ((30.2, 23.9), 11.18, "A-2-4(0)"),
                              ((30.1, 16.5), 18.38, "A-2-6(0)"),
                              ((35, 28), 40.0, "A-4(1)"),
                              ((48, 39), 40.0, "A-5(1)"),
                              ((37.7, 23.8), 47.44, "A-6(4)"),
                              ((61.7, 32.3), 52.09, "A-7-5(12)"),
                              ((70.0, 38.0), 86, "A-7-5(20)"),
                              ((52.6, 27.6), 45.8, "A-7-6(7)"),
                              ((45.0, 16.0), 60, "A-7-6(13)")])
    def test_aashto_with_grp_idx(self, al, fines, expected):
        asshto_clf = create_soil_classifier(*al, fines=fines,
                                            clf_type="AASHTO")
        assert asshto_clf.classify().symbol == expected

    @pytest.mark.parametrize(["al", "fines", "expected"],
                             [((0.0, 0.0), 9.5, "A-3"),
                              ((43.0, 35.0), 30.0, "A-2-5"),
                              ((43.0, 25.0), 30.0, "A-2-7"),
                              ((35.0, 28.0), 40.0, "A-4")])
    def test_aashto_without_grp_idx(self, al, fines, expected):
        asshto_clf = create_soil_classifier(*al, fines=fines,
                                            add_group_idx=False,
                                            clf_type="AASHTO")
        assert asshto_clf.classify().symbol == expected


class TestUSCS:
    @pytest.mark.parametrize(["al", "psd", "dist", "expected"],
                             [((30.8, 20.7), (10.29, 81.89), (0.07, 0.3, 0.8),
                               "SW-SC"),
                              ((24.4, 14.7), (9.77, 44.82), (0.06, 0.6, 7),
                               "GP-GC"),
                              ((49.5, 33.6), (6.93, 91.79), (0.153, 0.4, 1.2),
                               "SP-SM"),
                              ((30.33, 23.42), (8.93, 7.69), (0.15, 18, 44),
                               "GP-GM"),
                              ((35.32, 25.57), (9.70, 5.63), (0.06, 50, 55),
                               "GP-GM"),
                              ((26.17, 19.69), (12.00, 8.24), (0.07, 15, 52),
                               "GP-GC"),
                              ((30.59, 24.41), (9.87, 19.03), (0.07, 0.3, 0.8),
                               "GW-GM"),
                              ((32.78, 22.99), (3.87, 15.42), (2.5, 6, 15),
                               "GP"), ])
    def test_dual_classification(self, al, psd, dist, expected):
        uscs_clf = create_soil_classifier(*al, *psd, *dist, clf_type="uscs")
        assert uscs_clf.classify().symbol == expected

    @pytest.mark.parametrize(
        "al,psd,expected",
        [((30.8, 20.7), (10.29, 81.89), "SW-SC,SP-SC"),
         ((24.4, 14.7), (9.77, 44.82), "GW-GC,GP-GC"),
         ((49.5, 33.6), (6.93, 91.79), "SW-SM,SP-SM"),
         ((30.33, 23.42), (8.93, 7.69), "GW-GM,GP-GM"),
         ((35.32, 25.57), (9.70, 5.63), "GW-GM,GP-GM"),
         ((26.17, 19.69), (12.00, 8.24), "GW-GC,GP-GC"),
         ((32.78, 22.99), (3.87, 15.42), "GW,GP"), ])
    def test_dual_classification_no_psd_coeff(self, al, psd, expected):
        uscs_clf = create_soil_classifier(*al, *psd, clf_type="uscs")
        assert uscs_clf.classify().symbol == expected

    @pytest.mark.parametrize(["al", "psd", "organic", "expected"],
                             [((34.1, 21.1), (47.88, 37.84), False, "SC"),
                              ((27.5, 13.8), (54.23, 45.69), False, "CL"),
                              ((27.7, 22.7), (18.95, 77.21), False, "SM-SC"),
                              ((64.1, 29), (57.17, 42.58), False, "CH"),
                              ((56, 32.4), (51.11, 46.87), False, "MH"),
                              ((70, 38), (86, 7), False, "MH"),
                              ((26.4, 19.4), (54.76, 45.24), False, "ML-CL"),
                              ((33, 21), (30, 30), False, "GC"),
                              ((34.46, 23.85), (18.09, 18.7), False, "GC"),
                              ((45, 16), (59, 41), False, "CL"),
                              ((55, 40), (85, 15), False, "MH"),
                              ((49.93, 37.22), (49.4, 35.98), False, "SM"),
                              ((42.77, 29.98), (27.6, 27.93), False, "GM"),
                              ((35.83, 25.16), (68.94, 28.88), False, "ML"),
                              ((27.7, 22.7), (18.95, 20.48), False, "GM-GC"),
                              ((35.83, 25.16), (68.94, 28.88), True, "OL"),
                              ((55.0, 40.0), (85.0, 15.0), True, "OH")])
    def test_single_classification(self, al, psd, organic, expected):
        uscs_clf = create_soil_classifier(*al, *psd,
                                          organic=organic,
                                          clf_type="uscs")
        assert uscs_clf.classify().symbol == expected
