from geolysis.constants import UNITS
from geolysis.foundation import FoundationSize
from geolysis.utils import round_


class AllowableSettlementError(ValueError):
    """
    Exception raised when actual settlement exceeds allowable settlement.
    """


def _chk_settlement(actual_settlement: float, allowable_settlement: float):
    if actual_settlement > allowable_settlement:
        errmsg = f"Settlement: {actual_settlement} should be less than or equal \
                Allowable Settlement: {allowable_settlement}"
        raise AllowableSettlementError(errmsg)


class BowlesABC1997:
    """
    Allowable bearing capacity for cohesionless soils according to ``Bowles
    (1997)``.

    :param float avg_corrected_spt_val: Statistical average of corrected SPT N-value
        (55% energy with overburden pressure correction) within the foundation influence
        zone i.e. :math:`0.5B` to :math:`2B`.
    :param float tol_settlement: Tolerable settlement. (mm)
    :param FoundationSize foundation_size: Size of foundation.
    """

    MAX_TOL_SETTLEMENT = 25.4
    unit = UNITS.kilo_pascal

    def __init__(
        self,
        avg_corrected_spt_val: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.avg_corrected_spt_val = avg_corrected_spt_val
        self.tol_settlement = tol_settlement
        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @property
    def fd(self):
        r"""
        Return the depth factor.

        .. math::

            f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
        """
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @round_(ndigits=2)
    def abc_cohl_4_isolated_foundation(self):
        r"""
        Return allowable bearing capacity for isolated foundation on
        cohesionless soils.

        for B :math:`\le` 1.2m:

        .. math::

            q_a(kPa) = 19.16(N_1)_{55} f_d\left(\dfrac{S}{25.4}\right)

        for B :math:`\gt` 1.2m:

        .. math::

            q_a(kPa) = 11.8(N_1)_{55}\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d
            \left(\dfrac{S}{25.4}\right)
        """

        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        if self.f_width <= 1.2:
            abc = (
                19.16 * self.avg_corrected_spt_val * self.fd * settlement_ratio
            )

        else:
            abc = (
                11.98
                * self.avg_corrected_spt_val
                * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
                * self.fd
                * settlement_ratio
            )

        return abc

    @round_(ndigits=2)
    def abc_cohl_4_raft_foundation(self):
        r"""
        Return allowable bearing capacity for raft foundation on cohesionless
        soils.

        .. math::

            q_a(kPa) = 11.98(N_1)_{55}f_d\left(\dfrac{S}{25.4}\right)
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        return 11.98 * self.avg_corrected_spt_val * self.fd * settlement_ratio


class MeyerhofABC1956:
    """
    Allowable bearing capacity for cohesionless soils according to ``Meyerhof
    (1956)``.

    :param float avg_uncorrected_spt_val: Average uncorrected SPT N-value within the
        foundation influence zone i.e. :math:`D_f` to :math:`D_f + 2B`. Only water table
        correction suggested.
    :param float tol_settlement: Tolerable settlement. (mm)
    :param FoundationSize foundation_size: Size of foundation.
    """

    MAX_TOL_SETTLEMENT = 25.4
    unit = UNITS.kilo_pascal

    def __init__(
        self,
        avg_uncorrected_spt_val: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.avg_uncorrected_spt_val = avg_uncorrected_spt_val
        self.tol_settlement = tol_settlement
        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @property
    def fd(self):
        r"""
        Return the depth factor.

        .. math::

            f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33
        """
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @round_(ndigits=2)
    def abc_cohl_4_isolated_foundation(self):
        r"""
        Return allowable bearing capacity for isolated foundation on
        cohesionless soils.

        for B :math:`\le` 1.2m:

        .. math::

            q_a(kPa) = 12N f_d\left(\dfrac{S}{25.4}\right)

        for B :math:`\gt` 1.2m:

        .. math::

            q_a(kPa) = 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d\left(\dfrac{S}{25.4}\right)
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        if self.f_width <= 1.2:
            abc = (
                12 * self.avg_uncorrected_spt_val * self.fd * settlement_ratio
            )

        else:
            abc = (
                8
                * self.avg_uncorrected_spt_val
                * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
                * self.fd
                * settlement_ratio
            )

        return abc

    @round_(ndigits=2)
    def abc_cohl_4_raft_foundation(self):
        r"""
        Return allowable bearing capacity for raft foundation on cohesionless
        soils.

        .. math::

            q_a(kPa) = 8 N f_d\left(\dfrac{S}{25.4}\right)
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        return 8 * self.avg_uncorrected_spt_val * self.fd * settlement_ratio


class TerzaghiABC1948:
    """
    Allowable bearing capacity for cohesionless soils according to ``Terzaghi &
    Peck (1948)``.

    :param float lowest_uncorrected_spt_val: Lowest (or average) uncorrected SPT
        N-values within the foundation influence zone. i.e. :math:`D_f` to :math:`D_f + 2B`
    :param float tol_settlement: Tolerable settlement. (mm)
    :param FoundationSize foundation_size: Size of foundation.
    """

    MAX_TOL_SETTLEMENT = 25.4
    unit = UNITS.kilo_pascal

    def __init__(
        self,
        lowest_uncorrected_spt_val: float,
        tol_settlement: float,
        water_depth: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.lowest_uncorrected_spt_val = lowest_uncorrected_spt_val
        self.tol_settlement = tol_settlement
        self.water_depth = water_depth
        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @property
    def fd(self):
        r"""
        Return the depth factor.

        .. math::

            f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25
        """
        return min(1 + 0.25 * self.f_depth / self.f_width, 1.25)

    @property
    def cw(self):
        r"""
        Return the water correction factor.

        for surface footing:

        .. math::

            c_w = 2 - \frac{D_w}{2B} \le 2

        for fully submerged footing :math:`d_w \le D_f`

        .. math::

            c_w = 2 - \frac{D_f}{2B} \le 2
        """
        if self.water_depth <= self.f_depth:
            # for fully submerged footing
            _cw = 2 - self.f_depth / (2 * self.f_width)
        else:
            # for surface footing
            _cw = 2 - self.water_depth / (2 * self.f_width)

        return min(_cw, 2)

    @round_(ndigits=2)
    def abc_cohl_4_isolated_foundation(self):
        r"""
        Return allowable bearing capacity for isolated foundation on
        cohesionless soils.

        for B :math:`\le` 1.2m:

        .. math::

            q_a(kPa) = 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

        for B :math:`\gt` 1.2m:

        .. math::

            q_a(kPa) = 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}{c_w f_d}
            \left(\dfrac{S}{25.4}\right)
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        if self.f_width <= 1.2:
            abc = (
                12
                * self.lowest_uncorrected_spt_val
                * (1 / (self.cw * self.fd))
                * settlement_ratio
            )
        else:
            abc = (
                8
                * self.lowest_uncorrected_spt_val
                * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
                * (1 / (self.cw * self.fd))
                * settlement_ratio
            )

        return abc

    @round_(ndigits=2)
    def abc_cohl_4_raft_foundation(self):
        r"""
        Return allowable bearing capacity for raft foundation on cohesionless
        soils.

        .. math::

            q_a(kPa) = 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)
        """
        settlement_ratio = self.tol_settlement / self.MAX_TOL_SETTLEMENT

        return (
            8
            * self.lowest_uncorrected_spt_val
            * (1 / (self.cw * self.fd))
            * settlement_ratio
        )
