import unittest

import pytest

from geolab.soil_classifier import USCS, Soil
from geolab import PSDValueError
from .conftest import single_classification, dual_classification


class TestSoil(unittest.TestCase):
    def setUp(self) -> None:
        self.soil = Soil(
            liquid_limit=70,
            plastic_limit=38,
            plasticity_index=32,
            fines=86,
            sand=7,
            gravel=7,
        )

    def test_A_line(self):
        self.assertEqual(self.soil.is_above_A_line, False)

    def test_group_index(self):
        self.assertAlmostEqual(self.soil.group_index, 33.47)

    def test_classification(self):
        self.assertEqual(self.soil.get_aashto_classification(), "A-7-5(33)")
        self.assertEqual(self.soil.get_unified_classification(), "MH")


def _get_params(soil):
    for soil_parameters in single_classification:
        classification = soil_parameters.pop().strip()
        soil_parameters = (float(soil_data) for soil_data in soil_parameters)
    return soil_parameters, classification


def test_single_classification(soil_infos):
    soil_params, classification = _get_params(single_classification)
    assert USCS(soil_parameters=soil_params) == classification


@pytest.mark.xfail
def test_dual_classification(soil_infos):
    soil_params, classification = _get_params(dual_classification)
    assert USCS(soil_parameters=soil_params) == classification
