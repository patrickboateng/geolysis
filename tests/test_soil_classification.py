import pytest

from geolab import ERROR_TOLERANCE
from geolab.exceptions import PIValueError, PSDValueError
from geolab.soil_classifier import AASHTO, PSD, USCS, AtterbergLimits

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
    ((17.9, 3.4, 24.01), "A-2-4(0)"),
    ((37.7, 13.9, 47.44), "A-6(4)"),
    ((30.1, 13.7, 18.38), "A-2-6(0)"),
    ((61.7, 29.4, 52.09), "A-7-5(12)"),
    ((52.6, 25.0, 45.8), "A-7-6(7)"),
    ((30.2, 6.3, 11.18), "A-2-4(0)"),
    ((70.0, 32.0, 86), "A-7-5(20)"),
    ((45, 29, 60), "A-7-6(13)"),
]


def test_PSD():
    with pytest.raises(PSDValueError):
        PSD(30, 30, 30)


def test_PI():
    with pytest.raises(PIValueError):
        atterberg_limits = AtterbergLimits(30, 10, 10)
        psd = PSD(30, 30, 40)
        AASHTO(atterberg_limits, fines=30).classify()
        USCS(atterberg_limits, psd).classify()


@pytest.mark.parametrize("soil_params,classification", aashto_class_test_data)
def test_aashto(soil_params, classification):
    assert AASHTO(*soil_params).classify() == classification


@pytest.mark.parametrize(
    "soil_params,particle_sizes,classification", dual_class_test_data
)
def test_dual_classification(
    soil_params: tuple, particle_sizes: dict, classification: dict
):
    assert USCS(*soil_params, **particle_sizes).classify() == classification


@pytest.mark.parametrize("soil_params,classification", single_class_test_data)
def test_single_classification(soil_params: tuple, classification: str):
    assert USCS(*soil_params).classify() == classification
