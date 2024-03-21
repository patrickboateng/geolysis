from geolysis.constants import UNITS
from geolysis.foundation import FoundationSize
from geolysis.utils import FloatOrInt, round_

__all__ = ["BowlesABC", "MeyerhofABC", "TerzaghiABC"]


class AllowableSettlementError(ValueError):
    """
    Exception raised when actual settlement exceeds allowable settlement.
    """


def _chk_settlement(
    tol_settlement: FloatOrInt, max_tol_settlement: FloatOrInt
):
    if tol_settlement > max_tol_settlement:
        err_msg = f"Settlement: {tol_settlement} should be less than or equal \
                Allowable Settlement: {max_tol_settlement}"
        raise AllowableSettlementError(err_msg)


class BowlesABC:
    """
    Allowable bearing capacity for cohesionless soils according to ``Bowles``.

    :param FloatOrInt avg_corrected_spt_val: Statistical average of corrected
                                             SPT N-value (55% energy with overburden
                                             pressure correction) within the foundation
                                             influence zone i.e. ``0.5B`` to ``2B``.
    :param FloatOrInt tol_settlement: Tolerable settlement. (mm)
    :param FoundationSize foundation_size: Size of foundation.

    :Example:

        >>> from geolysis.bearing_capacity.abc_4_cohl_soil import BowlesABC1997
        >>> from geolysis.foundation import FoundationSize, FootingSize, SquareFooting
        >>> footing_shape = SquareFooting(width=1.2)
        >>> footing_size = FootingSize(thickness=0.3, footing_shape=footing_shape)
        >>> foundation_size = FoundationSize(depth=1.5, footing_size=footing_size)
        >>> bowles_abc = BowlesABC1997(avg_corrected_spt_val=11,
        ...                            tol_settlement=20,
        ...                            foundation_size=foundation_size)
        >>> bowles_abc.abc_cohl_4_isolated_foundation()
        220.72
    """

    #: Maximum tolerable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    unit = UNITS.kPa

    def __init__(
        self,
        avg_corrected_spt_val: FloatOrInt,
        tol_settlement: FloatOrInt,
        foundation_size: FoundationSize,
    ) -> None:
        self.avg_corrected_spt_val = avg_corrected_spt_val
        self.tol_settlement = tol_settlement

        #: Depth of foundation. (m)
        self.f_depth = foundation_size.depth
        #: Width of foundation footing. (m)
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    def __str__(self) -> str:
        return "Bowles (1997)"

    @property
    def fd(self) -> float:
        """
        Return the depth factor.
        """
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @round_(ndigits=2)
    def abc_4_isolated_foundation_1997(self) -> float:
        """
        Return allowable bearing capacity for isolated foundation on
        cohesionless soils.
        """

        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        if self.f_width <= 1.2:
            return (
                19.16 * self.avg_corrected_spt_val * self.fd * settlement_ratio
            )

        return (
            11.98
            * self.avg_corrected_spt_val
            * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
            * self.fd
            * settlement_ratio
        )

    @round_(ndigits=2)
    def abc_4_raft_foundation_1997(self):
        """
        Return allowable bearing capacity for raft foundation on cohesionless
        soils.
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        return 11.98 * self.avg_corrected_spt_val * self.fd * settlement_ratio


class MeyerhofABC:
    """
    Allowable bearing capacity for cohesionless soils according to ``Meyerhof``.

    :param FloatOrInt avg_uncorrected_spt_val: Average uncorrected SPT N-value
                                               within the foundation influence
                                               zone i.e. :math:`D_f` to :math:`D_f + 2B`.
                                               Only water table correction suggested.
    :param FloatOrInt tol_settlement: Tolerable settlement. (mm)
    :param FoundationSize foundation_size: Size of foundation.
    """

    #: Maximum tolerable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    unit = UNITS.kPa

    def __init__(
        self,
        avg_uncorrected_spt_val: FloatOrInt,
        tol_settlement: FloatOrInt,
        foundation_size: FoundationSize,
    ) -> None:
        self.avg_uncorrected_spt_val = avg_uncorrected_spt_val
        self.tol_settlement = tol_settlement

        #: Depth of footing. (m)
        self.f_depth = foundation_size.depth
        #: Width of footing. (m)
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    def __str__(self) -> str:
        return "Meyerhof (1956)"

    @property
    def fd(self):
        """
        Return the depth factor.
        """
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @round_(ndigits=2)
    def abc_4_isolated_foundation_1956(self):
        """
        Return allowable bearing capacity for isolated foundation on
        cohesionless soils.
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        if self.f_width <= 1.2:
            return (
                12 * self.avg_uncorrected_spt_val * self.fd * settlement_ratio
            )

        return (
            8
            * self.avg_uncorrected_spt_val
            * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
            * self.fd
            * settlement_ratio
        )

    @round_(ndigits=2)
    def abc_4_raft_foundation_1956(self):
        """
        Return allowable bearing capacity for raft foundation on cohesionless
        soils.
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        return 8 * self.avg_uncorrected_spt_val * self.fd * settlement_ratio


class TerzaghiABC:
    """
    Allowable bearing capacity for cohesionless soils according to ``Terzaghi &
    Peck (1948)``.

    :param FloatOrInt lowest_uncorrected_spt_val: Lowest (or average) uncorrected
                                                  SPT N-values within the foundation
                                                  influence zone. i.e. :math:`D_f` to
                                                  :math:`D_f + 2B`
    :param FloatOrInt tol_settlement: Tolerable settlement. (mm)
    :param FloatOrInt water_depth: Depth of water below ground surface. (m)
    :param FoundationSize foundation_size: Size of foundation.
    """

    #: Maximum allowable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    unit = UNITS.kPa

    def __init__(
        self,
        lowest_uncorrected_spt_val: FloatOrInt,
        tol_settlement: FloatOrInt,
        water_depth: FloatOrInt,
        foundation_size: FoundationSize,
    ) -> None:
        self.lowest_uncorrected_spt_val = lowest_uncorrected_spt_val
        self.tol_settlement = tol_settlement
        self.water_depth = water_depth

        #: Depth of foundation. (m)
        self.f_depth = foundation_size.depth
        #: Width of foundation footing. (m)
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    def __str__(self) -> str:
        return "Terzaghi (1948)"

    @property
    def fd(self):
        """
        Return the depth factor.
        """
        return min(1 + 0.25 * self.f_depth / self.f_width, 1.25)

    @property
    def cw(self):
        """
        Return the water correction factor.
        """
        if self.water_depth <= self.f_depth:
            # for fully submerged footing
            _cw = 2 - self.f_depth / (2 * self.f_width)
        else:
            # for surface footing
            _cw = 2 - self.water_depth / (2 * self.f_width)

        return min(_cw, 2)

    @round_(ndigits=2)
    def abc_4_isolated_foundation_1948(self) -> float:
        """
        Return allowable bearing capacity for isolated foundation on
        cohesionless soils.
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        if self.f_width <= 1.2:
            return (
                12
                * self.lowest_uncorrected_spt_val
                * (1 / (self.cw * self.fd))
                * settlement_ratio
            )

        return (
            8
            * self.lowest_uncorrected_spt_val
            * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
            * (1 / (self.cw * self.fd))
            * settlement_ratio
        )

    @round_(ndigits=2)
    def abc_4_raft_foundation_1948(self) -> float:
        """
        Return allowable bearing capacity for raft foundation on cohesionless
        soils.
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        return (
            8
            * self.lowest_uncorrected_spt_val
            * (1 / (self.cw * self.fd))
            * settlement_ratio
        )
