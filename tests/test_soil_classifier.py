import pytest

from geolysis.exceptions import PSDValueError
from geolysis.soil_classifier import AASHTO, PSD, USCS, AtterbergLimits


def test_PSDValueError():
    with pytest.raises(PSDValueError):
        PSD(30, 30, 30)


@pytest.mark.parametrize(
    "soil_params,classification",
    [
        ((17.9, 3.4, 24.01), "A-2-4(0)"),
        ((37.7, 13.9, 47.44), "A-6(4)"),
        ((30.1, 13.7, 18.38), "A-2-6(0)"),
        ((61.7, 29.4, 52.09), "A-7-5(12)"),
        ((52.6, 25.0, 45.8), "A-7-6(7)"),
        ((30.2, 6.3, 11.18), "A-2-4(0)"),
        ((70.0, 32.0, 86), "A-7-5(20)"),
        ((45, 29, 60), "A-7-6(13)"),
    ],
)
def test_aashto(soil_params, classification):
    assert AASHTO(*soil_params).classify() == classification


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
    psd = PSD(*psd, **particle_sizes)
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
    ],
)
def test_dual_classification_no_psd_coeff(
    al,
    psd,
    classification: str,
):
    atterberg_limits = AtterbergLimits(*al)
    psd = PSD(*psd)
    uscs = USCS(atterberg_limits=atterberg_limits, psd=psd)

    assert uscs.classify() == classification


@pytest.mark.parametrize(
    "al,psd,classification",
    [
        ((34.1, 21.1), (47.88, 37.84, 14.28), "SC"),
        ((27.5, 13.8), (54.23, 45.69, 0.08), "CL"),
        ((27.7, 22.7), (18.95, 77.21, 3.84), "SM"),
        ((64.1, 29), (57.17, 42.58, 0.25), "CH"),
        ((56, 32.4), (51.11, 46.87, 2.02), "MH"),
        ((70, 38), (86, 7, 7), "MH"),
        ((26.4, 19.4), (54.76, 45.24, 0), "ML-CL"),
        ((33, 21), (30, 30, 40), "GC"),
        ((34.46, 23.85), (18.09, 18.7, 63.21), "GM-GC"),
    ],
)
def test_single_classification(al, psd, classification: str):
    atterberg_limits = AtterbergLimits(*al)
    psd = PSD(*psd)
    uscs = USCS(atterberg_limits=atterberg_limits, psd=psd)

    assert uscs.classify() == classification
