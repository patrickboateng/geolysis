import pytest

from geolysis import ERROR_TOLERANCE
from geolysis.exceptions import PSDValueError
from geolysis.soil_classifier import (
    AASHTOClassificationSystem,
    AtterbergLimits,
    ParticleSizeDistribution,
    UnifiedSoilClassificationSystem,
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
    def test_uniformity_coefficient(self):
        psd = ParticleSizeDistribution(
            0, 0, 100, d10=0.115, d30=0.53, d60=1.55
        )
        assert psd.uniformity_coefficient == pytest.approx(
            13.48,
            rel=ERROR_TOLERANCE,
        )
        assert psd.coefficient_of_uniformity == pytest.approx(
            13.48,
            rel=ERROR_TOLERANCE,
        )

    def test_curvature_coefficient(self):
        psd = ParticleSizeDistribution(
            0, 0, 100, d10=0.115, d30=0.53, d60=1.55
        )
        assert psd.curvature_coefficient == pytest.approx(
            1.58,
            rel=ERROR_TOLERANCE,
        )
        assert psd.coefficient_of_gradation == pytest.approx(
            1.58, ERROR_TOLERANCE
        )
        assert psd.coefficient_of_curvature == pytest.approx(
            1.58, ERROR_TOLERANCE
        )

    def test_PSDValueError(self):
        with pytest.raises(PSDValueError):
            ParticleSizeDistribution(30, 30, 30)


class TestAASHTOClassificationSystem:
    @pytest.mark.parametrize(
        "soil_params,classification",
        [
            ((17.9, 3.4, 24.01), "A-1-b(0)"),
            ((37.7, 13.9, 47.44), "A-6(4)"),
            ((30.1, 13.7, 18.38), "A-2-6(0)"),
            ((61.7, 29.4, 52.09), "A-7-5(12)"),
            ((52.6, 25.0, 45.8), "A-7-6(7)"),
            ((30.2, 6.3, 11.18), "A-2-4(0)"),
            ((70.0, 32.0, 86), "A-7-5(20)"),
            ((45, 29, 60), "A-7-6(13)"),
            ((30, 5, 10), "A-1-a(0)"),
        ],
    )
    def test_aashto(self, soil_params, classification):
        asshto_classifier = AASHTOClassificationSystem(*soil_params)
        assert asshto_classifier.classify() == classification


@pytest.mark.parametrize(
    "al,psd,particle_sizes,classification",
    [
        (
            (30.8, 20.7),
            (10.29, 81.89, 7.83),
            {"d10": 0.07, "d30": 0.3, "d60": 0.8},
            "SW-SC",
        ),
        (
            (24.4, 14.7),
            (9.77, 44.82, 45.41),
            {"d10": 0.06, "d30": 0.6, "d60": 7},
            "GP-GC",
        ),
        (
            (49.5, 33.6),
            (6.93, 91.79, 1.28),
            {"d10": 0.153, "d30": 0.4, "d60": 1.2},
            "SP-SM",
        ),
        (
            (30.33, 23.42),
            (8.93, 7.69, 83.38),
            {"d10": 0.15, "d30": 18, "d60": 44},
            "GP-GM",
        ),
        (
            (35.32, 25.57),
            (9.70, 5.63, 84.67),
            {"d10": 0.06, "d30": 50, "d60": 55},
            "GP-GM",
        ),
        (
            (26.17, 19.69),
            (12.00, 8.24, 79.76),
            {"d10": 0.07, "d30": 15, "d60": 52},
            "GP-GC",
        ),
    ],
)
def test_dual_classification(
    al,
    psd,
    particle_sizes: dict,
    classification: str,
):
    atterberg_limits = AtterbergLimits(*al)
    psd = ParticleSizeDistribution(*psd, **particle_sizes)
    uscs = UnifiedSoilClassificationSystem(
        atterberg_limits=atterberg_limits, psd=psd
    )

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
    ],
)
def test_dual_classification_no_psd_coeff(
    al,
    psd,
    classification: str,
):
    atterberg_limits = AtterbergLimits(*al)
    psd = ParticleSizeDistribution(*psd)
    uscs = UnifiedSoilClassificationSystem(
        atterberg_limits=atterberg_limits, psd=psd
    )

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
    ],
)
def test_single_classification(al, psd, classification: str):
    atterberg_limits = AtterbergLimits(*al)
    psd = ParticleSizeDistribution(*psd)
    uscs = UnifiedSoilClassificationSystem(
        atterberg_limits=atterberg_limits, psd=psd
    )

    assert uscs.classify() == classification
