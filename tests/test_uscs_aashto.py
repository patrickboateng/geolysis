import pytest

from geolab.soil_classifier import USCS, Soil
from geolab import PSDValueError
from .conftest import single_classification, dual_classification


class TestSoil:
    @pytest.fixture(scope="class")
    def soil(self) -> Soil:
        yield Soil(
            liquid_limit=33,
            plastic_limit=21,
            plasticity_index=12,
            fines=30,
            sand=30,
            gravel=40,
        )

    @pytest.fixture(scope="class")
    def aashto_soil(self) -> Soil:
        yield Soil(
            liquid_limit=70,
            plastic_limit=38,
            plasticity_index=32,
            fines=86,
            sand=7,
            gravel=7,
        )

    def test_group_index(self, soil: Soil):
        expected = 0.0
        assert soil.group_index == pytest.approx(expected=expected)

    def test_aggregates(self):
        with pytest.raises(PSDValueError):
            Soil(33, 21, 12, 30, 30, 30)

    def test_Aline(self, soil: Soil):
        expected = 9.49
        assert soil._A_line == pytest.approx(expected=expected)

    def test_unified_classification(self, soil: Soil):
        assert soil.get_unified_classification() == "GC"

    def test_aashto_classification(self, aashto_soil: Soil):
        assert aashto_soil.get_aashto_classification() == "A-7-5(33)"


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
