import unittest

import pytest

from geolab import soil_classifier
from geolab import PSDValueError, PIValueError


class TestSoil(unittest.TestCase):
    def setUp(self) -> None:
        self.soil = soil_classifier.Soil(
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
        self.assertEqual(self.soil.get_aashto_classification(), "A-7-5(33)")
        self.assertEqual(self.soil.get_unified_classification(), "MH")


def test_PSD():
    with pytest.raises(PSDValueError):
        soil_classifier.Soil(30, 10, 20, 30, 30, 30)


def test_PI():
    with pytest.raises(PIValueError):
        soil_classifier.Soil(30, 10, 10, 30, 30, 40)


def _get_params(soils):
    for soil_parameters in soils:
        classification = soil_parameters.pop().strip()
        soil_parameters = (float(soil_data) for soil_data in soil_parameters)
    return soil_parameters, classification


def test_soil_single_classification(soils_: tuple[list, list]):
    soil_single_classification, _ = soils_
    soil_params, classification = _get_params(soil_single_classification)
    assert (
        soil_classifier.Soil(*soil_params).get_unified_classification()
        == classification
    )


@pytest.mark.xfail
def test_soil_dual_classification(soils_):
    _, soil_dual_classification = soils_
    soil_params, classification = _get_params(soil_dual_classification)
    assert (
        soil_classifier.Soil(*soil_params).get_aashto_classification() == classification
    )
