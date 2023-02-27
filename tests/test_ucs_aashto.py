from src.soil_classier.soil_classier import unified_classification
from .conftest import soil_infos


def test_unified_classification():
    for soil_parameters, classification in soil_infos():
        assert unified_classification(soil_parameters) == classification
