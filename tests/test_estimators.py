import pytest

from geolysis import ERROR_TOLERANCE
from geolysis.estimators import (
    CompressionIndexEst,
    SoilFrictionAngleEst,
    SoilUnitWeight,
    UndrainedShearStrengthEst,
)


def test_compression_index():
    assert CompressionIndexEst.skempton_1994(liquid_limit=35) == pytest.approx(
        0.175, ERROR_TOLERANCE
    )
    assert CompressionIndexEst.terzaghi_et_al_1967(
        liquid_limit=35
    ) == pytest.approx(0.225, ERROR_TOLERANCE)

    assert CompressionIndexEst.hough_1957(void_ratio=0.78) == pytest.approx(
        0.148, ERROR_TOLERANCE
    )


def test_soil_friction_angle():
    assert SoilFrictionAngleEst.wolff_1989(spt_n_60=50) == pytest.approx(
        40.75, ERROR_TOLERANCE
    )

    assert SoilFrictionAngleEst.wolff_1989(spt_n_60=40) == pytest.approx(
        38.236, ERROR_TOLERANCE
    )

    assert SoilFrictionAngleEst.kullhawy_mayne_1990(
        spt_n_60=40, eop=103.8, atm_pressure=101.325
    ) == pytest.approx(46.874, ERROR_TOLERANCE)


def test_soil_unit_weight():
    suw = SoilUnitWeight(spt_n_60=13)
    assert suw.est_moist_wgt == pytest.approx(17.3, ERROR_TOLERANCE)
    assert suw.est_saturated_wgt == pytest.approx(18.75, ERROR_TOLERANCE)
    assert suw.est_submerged_wgt == pytest.approx(8.93, ERROR_TOLERANCE)


def test_undrained_shear_strength():
    assert UndrainedShearStrengthEst.stroud_1974(spt_n_60=40) == pytest.approx(
        140, ERROR_TOLERANCE
    )

    assert UndrainedShearStrengthEst.skempton_1957(
        eop=108.3, plasticity_index=12
    ) == pytest.approx(16.722, ERROR_TOLERANCE)

    with pytest.raises(ValueError):
        UndrainedShearStrengthEst.stroud_1974(spt_n_60=30, k=7)


# def test_foundation_depth():
#     est_depth = rankine_est_min_foundation_depth(
#         allowable_bearing_capacity=350,
#         soil_unit_weight=18,
#         soil_friction_angle=35,
#     )
#     assert est_depth == pytest.approx(1.4, ERROR_TOLERANCE)


# def test_soil_elastic_modulus():
#     est_elastic_modulus = bowles_est_soil_elastic_modulus(spt_n60=11)
#     assert est_elastic_modulus == pytest.approx(8320, ERROR_TOLERANCE)
