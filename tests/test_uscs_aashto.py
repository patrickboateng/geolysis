import pytest

from geolab.soil_classifier import USCS, Soil
from geolab import PSDValueError
from .conftest import single_classification, dual_classification


class TestSoil:
    @pytest.fixture(scope="class")
    def soil(self) -> Soil:
        yield Soil(
            liquid_limit=70,
            plastic_limit=38,
            plasticity_index=32,
            fines=86,
            sand=8,
            gravel=6,
        )

    def test_group_index(self, soil: Soil):
        expected = 33.47
        assert soil.group_index() == pytest.approx(expected=expected)

    def test_aggregates(self):
        with pytest.raises(PSDValueError):
            Soil(33, 21, 12, 30, 30, 30)


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
