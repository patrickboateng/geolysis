import pytest

from geolysis.bearing_capacity import SquareFooting
from geolysis.bearing_capacity.abc import (
    AllowableSettlementError,
    FoundationSize,
    bowles_cohl_abc_1997,
    meyerhof_cohl_abc_1956,
    terzaghi_peck_cohl_abc_1948,
)
from geolysis.constants import ERROR_TOL


@pytest.mark.parametrize(
    ("spt_n_val", "act_sett", "found_depth", "footing_dim", "abc"),
    ((11, 20, 1.5, 1.2, 220.72), (11, 20, 1.5, 1.4, 204.66)),
)
def test_bowles_cohl_abc(spt_n_val, act_sett, found_depth, footing_dim, abc):
    fs = FoundationSize(
        depth=found_depth,
        footing_size=SquareFooting(width=footing_dim),
    )
    b_abc = bowles_cohl_abc_1997(
        spt_n_design=spt_n_val,
        actual_settlement=act_sett,
        foundation_size=fs,
    )
    assert b_abc == pytest.approx(abc, ERROR_TOL)


@pytest.mark.parametrize(
    ("spt_n_val", "act_sett", "found_depth", "footing_dim", "abc"),
    ((11, 20, 1.5, 1.2, 138.24), (11, 20, 1.5, 1.4, 136.67)),
)
def test_meyerhof_cohl_abc(spt_n_val, act_sett, found_depth, footing_dim, abc):
    fs = FoundationSize(
        depth=found_depth,
        footing_size=SquareFooting(width=footing_dim),
    )
    m_abc = meyerhof_cohl_abc_1956(
        spt_n_val=spt_n_val,
        actual_settlement=act_sett,
        foundation_size=fs,
    )
    assert m_abc == pytest.approx(abc, ERROR_TOL)


def test_meyerhof_cohl_abc_error(foundation_size):
    with pytest.raises(AllowableSettlementError):
        meyerhof_cohl_abc_1956(
            spt_n_val=11, actual_settlement=30, foundation_size=foundation_size
        )


@pytest.mark.parametrize(
    (
        "spt_n_val",
        "act_sett",
        "water_depth",
        "found_depth",
        "footing_dim",
        "abc",
    ),
    ((11, 20, 1.2, 1.5, 1.2, 60.37), (11, 20, 1.7, 1.5, 1.4, 59.01)),
)
def test_terzaghi_peck_cohl_abc(
    spt_n_val, act_sett, water_depth, found_depth, footing_dim, abc
):
    fs = FoundationSize(
        depth=found_depth,
        footing_size=SquareFooting(width=footing_dim),
    )
    t_abc = terzaghi_peck_cohl_abc_1948(
        spt_n_val=spt_n_val,
        actual_settlement=act_sett,
        water_depth=water_depth,
        foundation_size=fs,
    )
    assert t_abc == pytest.approx(abc, ERROR_TOL)
