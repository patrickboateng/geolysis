from src.soil_classifier.soil_classifier import USCS
from .conftest import soil_infos


def test_USCS():
    for soil_parameters, classification in soil_infos():
        assert USCS(soil_parameters) == classification
