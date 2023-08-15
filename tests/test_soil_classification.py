import pytest

from geolab import ERROR_TOLERANCE
from geolab.exceptions import PIValueError, PSDValueError
from geolab.soil_classifier import (
    AASHTO,
    USCS,
    AtterbergLimits,
    ParticleSizeDistribution,
    ParticleSizes,
    PSDCoefficient,
    group_index,
    soil_grade,
)

dual_class_test_data = [
    (
        (30.8, 20.7, 10.1, 10.29, 81.89, 7.83),
        {"d10": 0.07, "d30": 0.3, "d60": 0.8},
        "SW-SC",
    ),
    (
        (24.4, 14.7, 9.7, 9.77, 44.82, 45.41),
        {"d10": 0.06, "d30": 0.6, "d60": 7},
        "GP-GC",
    ),
    (
        (49.5, 33.6, 15.9, 6.93, 91.79, 1.28),
        {"d10": 0.153, "d30": 0.4, "d60": 1.2},
        "SP-SM",
    ),
]

single_class_test_data = [
    ((34.1, 21.1, 13, 47.88, 37.84, 14.28), "SC"),
    ((27.5, 13.8, 13.7, 54.23, 45.69, 0.08), "CL"),
    ((27.7, 22.7, 5, 18.95, 77.21, 3.84), "SM"),
    ((64.1, 29, 35.1, 57.17, 42.58, 0.25), "CH"),
    ((56, 32.4, 23.6, 51.11, 46.87, 2.02), "MH"),
    ((70, 38, 32, 86, 7, 7), "MH"),
    ((26.4, 19.4, 7, 54.76, 45.24, 0), "ML-CL"),
    ((33, 21, 12, 30, 30, 40), "GC"),
]

aashto_class_test_data = [
    ((17.9, 14.5, 3.4, 24.01), "A-2-4(0)"),
    ((37.7, 23.8, 13.9, 47.44), "A-6(4)"),
    ((30.1, 16.4, 13.7, 18.38), "A-2-6(0)"),
    ((61.7, 32.3, 29.4, 52.09), "A-7-5(12)"),
    ((52.6, 27.6, 25, 45.8), "A-7-6(7)"),
    ((30.2, 23.9, 6.3, 11.18), "A-2-4(0)"),
    ((70, 38, 32, 86), "A-7-5(33)"),
]

psd_coefficient = [
    ((0.07, 0.3, 0.8), {"cc": 1.61, "cu": 11.43}),
    ((0.06, 0.6, 7.0), {"cc": 0.86, "cu": 116.67}),
    ((0.153, 0.4, 1.2), {"cc": 0.87, "cu": 7.84}),
    ((2, 3.9, 8), {"cc": 0.95, "cu": 4}),
]


def test_grading():
    psd_coefficient = PSDCoefficient(ParticleSizes(2, 3.9, 8))
    assert soil_grade(psd_coefficient, "G") == "P"


def test_group_index():
    assert group_index(86, 70, 32) == pytest.approx(33, ERROR_TOLERANCE)


def test_PSD():
    with pytest.raises(PSDValueError):
        atterberg_limits = AtterbergLimits(30, 10, 20)
        psd = ParticleSizeDistribution(30, 30, 30)
        USCS(atterberg_limits, psd)()


def test_PI():
    with pytest.raises(PIValueError):
        atterberg_limits = AtterbergLimits(30, 10, 10)
        psd = ParticleSizeDistribution(30, 30, 40)
        AASHTO(atterberg_limits, fines=30)()
        USCS(atterberg_limits, psd)()


@pytest.mark.parametrize("psd,exp", psd_coefficient)
def test_PSDCoeffiecient(psd, exp):
    particle_sizes = ParticleSizes(*psd)
    psd_coeff = PSDCoefficient(particle_sizes)
    assert psd_coeff.curvature_coefficient == pytest.approx(
        exp["cc"], ERROR_TOLERANCE
    )
    assert psd_coeff.uniformity_coefficient == pytest.approx(
        exp["cu"], ERROR_TOLERANCE
    )


@pytest.mark.parametrize("soil_params,classification", aashto_class_test_data)
def test_aashto(soil_params, classification):
    liquid_limit, plastic_limit, plasticity_index, fines = soil_params
    atterberg_limits = AtterbergLimits(
        liquid_limit, plastic_limit, plasticity_index
    )
    assert AASHTO(atterberg_limits, fines)() == classification


@pytest.mark.parametrize(
    "soil_params,particle_sizes,classification", dual_class_test_data
)
def test_dual_classification(
    soil_params: tuple, particle_sizes: dict, classification: dict
):
    (
        liquid_limit,
        plastic_limit,
        plasticity_index,
        fines,
        sands,
        gravels,
    ) = soil_params
    atterberg_limits = AtterbergLimits(
        liquid_limit, plastic_limit, plasticity_index
    )
    _particle_sizes = ParticleSizes(**particle_sizes)
    psd = ParticleSizeDistribution(fines, sands, gravels, _particle_sizes)
    assert USCS(atterberg_limits, psd)() == classification


@pytest.mark.parametrize("soil_params,classification", single_class_test_data)
def test_single_classification(soil_params: tuple, classification: str):
    (
        liquid_limit,
        plastic_limit,
        plasticity_index,
        fines,
        sands,
        gravels,
    ) = soil_params
    atterberg_limits = AtterbergLimits(
        liquid_limit,
        plastic_limit,
        plasticity_index,
    )
    psd = ParticleSizeDistribution(fines, sands, gravels)
    assert USCS(atterberg_limits, psd)() == classification
