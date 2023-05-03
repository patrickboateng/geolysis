import unittest
from types import SimpleNamespace

import pytest

from geolab import PIValueError, PSDValueError
from geolab.soil_classifier import Soil


dual_class_test_data = [
    (
        (30.8, 20.7, 10.1, 10.29, 81.89, 7.83),
        {"d10": 0.07, "d30": 0.3, "d60": 0.8},
        SimpleNamespace(classification="SW-SC", cu=11.43, cc=1.61),
    ),
    (
        (24.4, 14.7, 9.7, 9.77, 44.82, 45.41),
        {"d10": 0.06, "d30": 0.6, "d60": 7},
        SimpleNamespace(classification="GP-GC", cu=116.67, cc=0.86),
    ),
    (
        (49.5, 33.6, 15.9, 6.93, 91.79, 1.28),
        {"d10": 0.153, "d30": 0.4, "d60": 1.2},
        SimpleNamespace(classification="SP-SM", cu=7.84, cc=0.87),
    ),
]
single_class_test_data = [
    ((34.1, 21.1, 13, 47.88, 37.84, 14.28), "SC"),
    ((27.5, 13.8, 13.7, 54.23, 45.69, 0.08), "CL"),
    ((27.7, 22.7, 5, 18.95, 77.21, 3.84), "SM"),
    ((64.1, 29, 35.1, 57.17, 42.58, 0.25), "CH"),
    ((56, 32.4, 23.6, 51.11, 46.87, 2.02), "MH"),
    ((33, 21, 12, 30, 30, 40), "GC"),
]


class TestSoil(unittest.TestCase):
    def setUp(self) -> None:
        self.soil = Soil(
            liquid_limit=70,
            plastic_limit=38,
            plasticity_index=32,
            fines=86,
            sand=7,
            gravels=7,
        )

    def test_A_line(self):
        self.assertEqual(self.soil.is_above_A_line, False)

    def test_group_index(self):
        self.assertAlmostEqual(self.soil.group_index, 33.47)

    def test_classification(self):
        self.assertEqual(self.soil.aashto, "A-7-5(33)")
        self.assertEqual(self.soil.uscs, "MH")


def test_PSD():
    with pytest.raises(PSDValueError):
        Soil(30, 10, 20, 30, 30, 30)


def test_PI():
    with pytest.raises(PIValueError):
        Soil(30, 10, 10, 30, 30, 40)


def test_soil_in_hatched_zone():
    soil = Soil(26.4, 19.4, 7, 54.76, 45.24, 0)
    assert soil.uscs == "ML-CL"


@pytest.mark.parametrize("soil_params,size_coef,results", dual_class_test_data)
def test_dual_classification(soil_params: tuple, size_coef: dict, results: dict):
    soil = Soil(*soil_params, **size_coef)
    assert soil.uscs == results.classification
    assert soil.cu == pytest.approx(results.cu, 0.01)
    assert soil.cc == pytest.approx(results.cc, 0.01)


@pytest.mark.parametrize("soil_params,classification", single_class_test_data)
def test_single_classification(soil_params: tuple, classification: str):
    soil = Soil(*soil_params)
    assert soil.uscs == classification
