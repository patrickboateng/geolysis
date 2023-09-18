import pytest

from geolab import ERROR_TOLERANCE, GeotechEng
from geolab.estimators import (
    rankine_foundation_depth,
    soil_friction_angle,
    soil_unit_weight,
)
from geolab.exceptions import EngineerTypeError


def test_foundation_depth():
    assert rankine_foundation_depth(
        350, 18, friction_angle=35
    ) == pytest.approx(1.4, ERROR_TOLERANCE)


def test_soil_friction_angle():
    sfa = soil_friction_angle(spt_n60=50)
    exp = 40.75
    assert sfa() == pytest.approx(exp, ERROR_TOLERANCE)
    assert sfa.wolff_1989() == pytest.approx(exp, ERROR_TOLERANCE)

    sfa.spt_n60 = 40
    exp = 38.236
    assert sfa() == pytest.approx(exp, ERROR_TOLERANCE)
    assert sfa.wolff_1989() == pytest.approx(exp, ERROR_TOLERANCE)

    sfa = soil_friction_angle(
        spt_n60=40,
        eop=103.8,
        atm_pressure=101.325,
        eng=GeotechEng.KULLHAWY,
    )
    exp = 46.874
    assert sfa() == pytest.approx(exp, ERROR_TOLERANCE)
    assert sfa.kullhawy_mayne_1990() == pytest.approx(exp, ERROR_TOLERANCE)

    with pytest.raises(EngineerTypeError):
        sfa = soil_friction_angle(spt_n60=35, eng=GeotechEng.BAZARAA)
        sfa()


def test_soil_unit_weight():
    suw = soil_unit_weight(spt_n60=13)
    assert suw.moist == pytest.approx(17.3, ERROR_TOLERANCE)
    assert suw.saturated == pytest.approx(18.75, ERROR_TOLERANCE)
    assert suw.submerged == pytest.approx(8.93, ERROR_TOLERANCE)
