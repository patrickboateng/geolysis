import pytest

from geolysis import ERROR_TOLERANCE
from geolysis.exceptions import PSDValueError
from geolysis.soil_classifier import (
    AASHTO,
    PSD,
    USCS,
    AASHTOClassification,
    AtterbergLimits,
    ParticleSizeDistribution,
    ParticleSizes,
    UnifiedSoilClassification,
)


class TestAtterbergLimits:
    @classmethod
    def setup_class(cls):
        cls.atterberg_limits = AtterbergLimits(
            liquid_limit=25,
            plastic_limit=15,
        )

    def test_plasticity_index(self):
        plasticity_index = self.atterberg_limits.plasticity_index
        assert plasticity_index == pytest.approx(10, rel=ERROR_TOLERANCE)

    def test_liquidity_index(self):
        liquidity_index = self.atterberg_limits.liquidity_index(nmc=20)
        assert liquidity_index == pytest.approx(50, rel=ERROR_TOLERANCE)

    def test_consistency_index(self):
        consistency_index = self.atterberg_limits.consistency_index(nmc=20)
        assert consistency_index == pytest.approx(50, rel=ERROR_TOLERANCE)


class TestParticleSizeDistribution:
    def test_particle_coeff(self):
        psd = PSD(
            fines=0,
            sand=0,
            gravel=100,
            particle_sizes=ParticleSizes(d_10=0.115, d_30=0.53, d_60=1.55),
        )
        assert psd.coeff_of_uniformity == pytest.approx(
            13.48,
            rel=ERROR_TOLERANCE,
        )
        assert psd.coeff_of_curvature == pytest.approx(
            1.58,
            rel=ERROR_TOLERANCE,
        )

    def test_PSDValueError(self):
        with pytest.raises(PSDValueError):
            PSD(fines=30, sand=30, gravel=30)


class TestAASHTOClassificationSystem:
    @pytest.mark.parametrize(
        "soil_params,classification",
        [
            ((30, 5, 10), "A-1-a(0)"),
            ((17.9, 3.4, 24.01), "A-1-b(0)"),
            ((0, 0, 9.5), "A-3(0)"),
            ((0, 0, 9.5, False), "A-3"),
            ((30.2, 6.3, 11.18), "A-2-4(0)"),
            ((43, 8, 30, False), "A-2-5"),
            ((30.1, 13.7, 18.38), "A-2-6(0)"),
            ((43, 18, 30, False), "A-2-7"),
            ((35, 7, 40), "A-4(1)"),
            ((35, 7, 40, False), "A-4"),
            ((48, 9, 40), "A-5(1)"),
            ((37.7, 13.9, 47.44), "A-6(4)"),
            ((61.7, 29.4, 52.09), "A-7-5(12)"),
            ((70.0, 32.0, 86), "A-7-5(20)"),
            ((52.6, 25.0, 45.8), "A-7-6(7)"),
            ((45, 29, 60), "A-7-6(13)"),
        ],
    )
    def test_aashto(self, soil_params, classification):
        asshto_classifier = AASHTOClassification(*soil_params)
        assert asshto_classifier.classify() == classification


class TestUnifiedSoilClassificationSystem:
    @pytest.mark.parametrize(
        "al,psd,particle_sizes,classification",
        [
            (
                (30.8, 20.7),
                (10.29, 81.89, 7.83),
                (0.07, 0.3, 0.8),
                "SW-SC",
            ),
            (
                (24.4, 14.7),
                (9.77, 44.82, 45.41),
                (0.06, 0.6, 7),
                "GP-GC",
            ),
            (
                (49.5, 33.6),
                (6.93, 91.79, 1.28),
                (0.153, 0.4, 1.2),
                "SP-SM",
            ),
            (
                (30.33, 23.42),
                (8.93, 7.69, 83.38),
                (0.15, 18, 44),
                "GP-GM",
            ),
            (
                (35.32, 25.57),
                (9.70, 5.63, 84.67),
                (0.06, 50, 55),
                "GP-GM",
            ),
            (
                (26.17, 19.69),
                (12.00, 8.24, 79.76),
                (0.07, 15, 52),
                "GP-GC",
            ),
            (
                (30.59, 24.41),
                (9.87, 19.03, 71.1),
                (0.07, 0.3, 0.8),
                "GW-GM",
            ),
            (
                (32.78, 22.99),
                (3.87, 15.42, 80.71),
                (2.5, 6, 15),
                "GP",
            ),
        ],
    )
    def test_dual_classification(
        self,
        al,
        psd,
        particle_sizes: tuple,
        classification: str,
    ):
        atterberg_limits = AtterbergLimits(*al)
        psd = ParticleSizeDistribution(
            *psd, particle_sizes=ParticleSizes(*particle_sizes)
        )
        uscs = USCS(atterberg_limits=atterberg_limits, psd=psd)

        assert uscs.classify() == classification

    @pytest.mark.parametrize(
        "al,psd,classification",
        [
            (
                (30.8, 20.7),
                (10.29, 81.89, 7.83),
                "SW-SC,SP-SC",
            ),
            (
                (24.4, 14.7),
                (9.77, 44.82, 45.41),
                "GW-GC,GP-GC",
            ),
            (
                (49.5, 33.6),
                (6.93, 91.79, 1.28),
                "SW-SM,SP-SM",
            ),
            (
                (30.33, 23.42),
                (8.93, 7.69, 83.38),
                "GW-GM,GP-GM",
            ),
            (
                (35.32, 25.57),
                (9.70, 5.63, 84.67),
                "GW-GM,GP-GM",
            ),
            (
                (26.17, 19.69),
                (12.00, 8.24, 79.76),
                "GW-GC,GP-GC",
            ),
            ((32.78, 22.99), (3.87, 15.42, 80.71), "GW or GP"),
        ],
    )
    def test_dual_classification_no_psd_coeff(
        self,
        al,
        psd,
        classification: str,
    ):
        atterberg_limits = AtterbergLimits(*al)
        psd = ParticleSizeDistribution(*psd)
        uscs = USCS(atterberg_limits=atterberg_limits, psd=psd)

        assert uscs.classify() == classification

    @pytest.mark.parametrize(
        "al,psd,classification",
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
    def test_single_classification(self, al, psd, classification: str):
        atterberg_limits = AtterbergLimits(*al)
        psd = ParticleSizeDistribution(*psd)
        uscs = USCS(atterberg_limits=atterberg_limits, psd=psd)

        assert uscs.classify() == classification

    def test_single_classification_2(self):
        atterberg_limits = AtterbergLimits(35.83, 25.16)
        psd = PSD(fines=68.94, sand=28.88, gravel=2.18)
        uscs = UnifiedSoilClassification(atterberg_limits, psd, organic=True)

        assert uscs.classify() == "OL"

        atterberg_limits.liquid_limit = 55
        atterberg_limits.plastic_limit = 40

        psd.fines = 85
        psd.sand = 15
        psd.gravel = 0

        assert uscs.classify() == "OH"

    def test_soil_description(self):
        assert USCS.soil_description("SC") == "Clayey sands"
        assert USCS.soil_description(" SC ") == "Clayey sands"

        with pytest.raises(KeyError):
            USCS.soil_description("A-2-4")
