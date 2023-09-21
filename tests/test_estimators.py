import pytest

from geolab import ERROR_TOLERANCE, GeotechEng
from geolab.estimators import (
    SoilFrictionAngle,
    SoilUnitWeight,
    UndrainedShearStrength,
    rankine_foundation_depth,
)
from geolab.exceptions import EngineerTypeError


def test_soil_friction_angle():
    sfa = SoilFrictionAngle(spt_n60=50)
    exp = 40.75
    assert sfa() == pytest.approx(exp, ERROR_TOLERANCE)
    assert sfa.wolff_1989() == pytest.approx(exp, ERROR_TOLERANCE)

    sfa.spt_n60 = 40
    exp = 38.236
    assert sfa() == pytest.approx(exp, ERROR_TOLERANCE)
    assert sfa.wolff_1989() == pytest.approx(exp, ERROR_TOLERANCE)

    sfa = SoilFrictionAngle(
        spt_n60=40,
        eop=103.8,
        atm_pressure=101.325,
        eng=GeotechEng.KULLHAWY,
    )
    exp = 46.874
    assert sfa() == pytest.approx(exp, ERROR_TOLERANCE)
    assert sfa.kullhawy_mayne_1990() == pytest.approx(exp, ERROR_TOLERANCE)

    with pytest.raises(EngineerTypeError):
        SoilFrictionAngle(spt_n60=35, eng=GeotechEng.BAZARAA)


def test_soil_unit_weight():
    suw = SoilUnitWeight(spt_n60=13)
    assert suw.moist == pytest.approx(17.3, ERROR_TOLERANCE)
    assert suw.saturated == pytest.approx(18.75, ERROR_TOLERANCE)
    assert suw.submerged == pytest.approx(8.93, ERROR_TOLERANCE)


def test_undrained_shear_strength():
    uss = UndrainedShearStrength(spt_n60=40)
    exp = 140
    assert uss() == pytest.approx(exp, ERROR_TOLERANCE)
    assert uss.stroud_1974() == pytest.approx(exp, ERROR_TOLERANCE)

    uss = UndrainedShearStrength(
        spt_n60=40,
        eop=108.3,
        plasticity_index=12,
        eng=GeotechEng.SKEMPTON,
    )
    exp = 16.722
    assert uss() == pytest.approx(exp, ERROR_TOLERANCE)
    assert uss.skempton_1957() == pytest.approx(exp, ERROR_TOLERANCE)

    with pytest.raises(EngineerTypeError):
        UndrainedShearStrength(spt_n60=30, eng=GeotechEng.LIAO)


def test_foundation_depth():
    assert rankine_foundation_depth(
        350, 18, soil_friction_angle=35
    ) == pytest.approx(1.4, ERROR_TOLERANCE)
