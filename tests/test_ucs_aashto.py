import pytest
from src.soil_classier.soil_classier import unified_classification


@pytest.mark.parametrize(
    "soil_parameters,classification",
    [
        ((34.1, 21.1, 13, 47.88, 37.84, 14.28), "SC"),
        ((27.5, 13.8, 13.7, 54.23, 45.69, 0.08), "CL"),
        ((28.2, 14.6, 13.6, 56.43, 43.47, 0.1), "CL"),
        ((28.5, 15.3, 13.2, 54.1, 45.71, 0.19), "CL"),
        ((17.9, 15.9, 2, 20.99, 54.72, 24.29), "SC"),
        ((15.1, 14.8, 0.27, 27.33, 61.8, 10.88), "SC"),
        ((17.8, 15.5, 2.31, 45.35, 54.31, 0.35), "SC"),
        ((53.5, 20.6, 33, 42.35, 57.3, 0.36), "SC"),
        ((44.1, 27.3, 16.8, 43.21, 55.89, 0.89), "SM"),
        ((37.9, 26.5, 11.3, 35.91, 63.77, 0.32), "SM"),
        ((40.4, 23.3, 17, 37.97, 61.28, 0.75), "SC"),
    ],
)
def test_unified_classification(soil_parameters, classification):
    assert unified_classification(soil_parameters=soil_parameters) == classification
