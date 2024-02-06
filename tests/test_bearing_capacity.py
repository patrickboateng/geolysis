import pytest

from geolysis.bearing_capacity.abc import (
    AllowableSettlementError,
    BowlesABC1997,
    MeyerhofABC1956,
    TerzaghiABC1948,
)
from geolysis.constants import ERROR_TOL
from geolysis.foundation import FoundationSize, SquareFooting


class TestBowlesABC:

    @pytest.mark.parametrize(
        ("avg_corr_spt", "tol_sett", "found_depth", "footing_dim", "abc"),
        ((11, 20, 1.5, 1.2, 220.72), (11, 20, 1.5, 1.4, 204.66)),
    )
    def test_bowles_cohl_abc(
        self, avg_corr_spt, tol_sett, found_depth, footing_dim, abc
    ):
        fs = FoundationSize(
            depth=found_depth,
            footing_shape=SquareFooting(width=footing_dim),
        )
        b_abc = BowlesABC1997(
            avg_corrected_spt_val=avg_corr_spt,
            tol_settlement=tol_sett,
            foundation_size=fs,
        )

        assert b_abc.abc_cohl_4_isolated_foundation() == pytest.approx(abc)


class TestMeyerhofABC:

    @pytest.mark.parametrize(
        ("avg_corr_spt", "tol_sett", "found_depth", "footing_dim", "abc"),
        ((11, 20, 1.5, 1.2, 138.24), (11, 20, 1.5, 1.4, 136.67)),
    )
    def test_meyerhof_cohl_abc(
        self, avg_corr_spt, tol_sett, found_depth, footing_dim, abc
    ):
        fs = FoundationSize(
            depth=found_depth,
            footing_shape=SquareFooting(width=footing_dim),
        )
        m_abc = MeyerhofABC1956(
            avg_uncorrected_spt_val=avg_corr_spt,
            tol_settlement=tol_sett,
            foundation_size=fs,
        )

        assert m_abc.abc_cohl_4_isolated_foundation() == pytest.approx(abc)

    def test_meyerhof_cohl_abc_error(self):
        fs = FoundationSize(
            depth=1.2,
            footing_shape=SquareFooting(width=1.4),
        )
        with pytest.raises(AllowableSettlementError):
            MeyerhofABC1956(
                avg_uncorrected_spt_val=11,
                tol_settlement=30,
                foundation_size=fs,
            )


class TestTerzaghi:

    @pytest.mark.parametrize(
        (
            "low_uncorr_spt",
            "tol_sett",
            "water_depth",
            "found_depth",
            "footing_dim",
            "abc",
        ),
        ((11, 20, 1.2, 1.5, 1.2, 60.37), (11, 20, 1.7, 1.5, 1.4, 59.01)),
    )
    def test_terzaghi_peck_cohl_abc(
        self,
        low_uncorr_spt,
        tol_sett,
        water_depth,
        found_depth,
        footing_dim,
        abc,
    ):
        fs = FoundationSize(
            depth=found_depth,
            footing_shape=SquareFooting(width=footing_dim),
        )
        t_abc = TerzaghiABC1948(
            lowest_uncorrected_spt_val=low_uncorr_spt,
            tol_settlement=tol_sett,
            water_depth=water_depth,
            foundation_size=fs,
        )
        assert t_abc.abc_cohl_4_isolated_foundation() == pytest.approx(
            abc, ERROR_TOL
        )
