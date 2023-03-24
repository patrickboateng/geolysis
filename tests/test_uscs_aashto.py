import pytest

from src.geolab.soil_classifier import USCS
from .conftest import single_classification, dual_classification


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
