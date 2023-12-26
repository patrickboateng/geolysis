import pytest

from geolysis import ERROR_TOLERANCE
from geolysis.estimators import (
    CompressionIndex,
    SoilFrictionAngle,
    SoilUnitWeight,
    UndrainedShearStrength,
    bowles_est_soil_elastic_modulus,
    rankine_est_min_foundation_depth,
)


def test_compression_index():
    comp_idx = CompressionIndex(liquid_limit=35)
    assert comp_idx.skempton_1994() == pytest.approx(0.175, ERROR_TOLERANCE)
    assert comp_idx.terzaghi_et_al_1967() == pytest.approx(
        0.225, ERROR_TOLERANCE
    )

    comp_idx = CompressionIndex(void_ratio=0.78)
    assert comp_idx.hough_1957() == pytest.approx(0.148, ERROR_TOLERANCE)


def test_soil_friction_angle():
    sfa = SoilFrictionAngle(spt_n60=50)
    assert sfa.wolff_1989() == pytest.approx(40.75, ERROR_TOLERANCE)

    sfa.spt_n60 = 40
    assert sfa.wolff_1989() == pytest.approx(38.236, ERROR_TOLERANCE)

    sfa = SoilFrictionAngle(spt_n60=40, eop=103.8, atm_pressure=101.325)
    assert sfa.kullhawy_mayne_1990() == pytest.approx(46.874, ERROR_TOLERANCE)


def test_soil_unit_weight():
    suw = SoilUnitWeight(spt_n60=13)
    assert suw.moist == pytest.approx(17.3, ERROR_TOLERANCE)
    assert suw.saturated == pytest.approx(18.75, ERROR_TOLERANCE)
    assert suw.submerged == pytest.approx(8.93, ERROR_TOLERANCE)


def test_undrained_shear_strength():
    uss = UndrainedShearStrength(spt_n60=40)
    assert uss.stroud_1974() == pytest.approx(140, ERROR_TOLERANCE)

    uss.eop = 108.3
    uss.plasticity_index = 12

    assert uss.skempton_1957() == pytest.approx(16.722, ERROR_TOLERANCE)

    uss.k = 7.0

    with pytest.raises(ValueError):
        uss.stroud_1974()
    # assert uss.stroud_1974()


def test_foundation_depth():
    est_depth = rankine_est_min_foundation_depth(
        allowable_bearing_capacity=350,
        soil_unit_weight=18,
        soil_friction_angle=35,
    )
    assert est_depth == pytest.approx(1.4, ERROR_TOLERANCE)


def test_soil_elastic_modulus():
    est_elastic_modulus = bowles_est_soil_elastic_modulus(spt_n60=11)
    assert est_elastic_modulus == pytest.approx(8320, ERROR_TOLERANCE)
