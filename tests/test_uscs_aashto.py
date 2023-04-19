import unittest

import pytest

from geolab import PIValueError, PSDValueError
from geolab.soil_classifier import Soil


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
        self.assertEqual(self.soil.aashto_classification, "A-7-5(33)")
        self.assertEqual(self.soil.unified_classification, "MH")


def test_PSD():
    with pytest.raises(PSDValueError):
        Soil(30, 10, 20, 30, 30, 30)


def test_PI():
    with pytest.raises(PIValueError):
        Soil(30, 10, 10, 30, 30, 40)


def test_dual_classification():
    soil = Soil(30.8, 20.7, 10.1, 10.29, 81.89, 7.83, 0.07, 0.3, 0.8)
    assert soil.unified_classification == "SW-SC"
    assert soil.cu == pytest.approx(11.43, 0.01)
    assert soil.cc == pytest.approx(1.61, 0.01)

    soil = Soil(24.4, 14.7, 9.7, 9.77, 44.82, 45.41, 0.06, 0.6, 7)
    assert soil.unified_classification == "GP-GC"
    assert soil.cu == pytest.approx(116.67, 0.01)
    assert soil.cc == pytest.approx(0.86, 0.01)

    soil = Soil(49.5, 33.6, 15.9, 6.93, 91.79, 1.28, 0.153, 0.4, 1.2)
    assert soil.unified_classification == "SP-SM"
    assert soil.cu == pytest.approx(7.84, 0.01)
    assert soil.cc == pytest.approx(0.87, 0.01)


def test_soil_in_hatched_zone():
    soil = Soil(26.4, 19.4, 7, 54.76, 45.24, 0)
    assert soil.unified_classification == "ML-CL"


def _get_params(soils):
    for soil_parameters in soils:
        classification = soil_parameters.pop().strip()
        soil_parameters = (float(soil_data) for soil_data in soil_parameters)
    return soil_parameters, classification


def test_soil_single_classification(soils_: tuple[list, list]):
    soil_single_classification, _ = soils_
    soil_params, classification = _get_params(soil_single_classification)
    assert Soil(*soil_params).unified_classification == classification


@pytest.mark.xfail
def test_soil_dual_classification(soils_):
    _, soil_dual_classification = soils_
    soil_params, classification = _get_params(soil_dual_classification)
    assert Soil(*soil_params).aashto_classification == classification
