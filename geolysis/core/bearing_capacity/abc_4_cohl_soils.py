from abc import abstractmethod
from typing import Protocol

from geolysis.core.foundation import FoundationSize
from geolysis.core.utils import round_

__all__ = [
    "BowlesABC4PadFoundation",
    "BowlesABC4MatFoundation",
    "MeyerhofABC4PadFoundation",
    "MeyerhofABC4MatFoundation",
    "TerzaghiABC4PadFoundation",
    "TerzaghiABC4MatFoundation",
]


class SettlementError(ValueError):
    pass


def _chk_settlement(tol_settlement: float, max_tol_settlement: float):
    if tol_settlement > max_tol_settlement:
        err_msg = "tol_settlement should not be greater than 25.4."
        raise SettlementError(err_msg)


class AbstractABC(Protocol):
    MAX_TOL_SETTLEMENT = 25.4

    @abstractmethod
    def bearing_capacity(self): ...


class BowlesABC4PadFoundation(AbstractABC):
    r"""Allowable bearing capacity for mat foundation on cohesionless
    soils according to ``Bowles (1997)``.

    Parameters
    ----------
    corrected_spt_number : float
        Statistical average of corrected SPT N-value (55% energy with
        overburden pressure correction) within the foundation influence
        zone i.e ``0.5B`` to ``2B``.
    tol_settlement : float, mm
        Tolerable settlement.
    foundation_size : FoundationSize
        Size of foundation.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 19.16(N_1)_{55} f_d\left(\dfrac{S}{25.4}\right),
                    \ B \ \le \ 1.2m

        q_a(kPa) &= 11.98(N_1)_{55}\left(\dfrac{3.28B + 1}{3.28B} \right)^2
                    f_d \left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    Examples
    --------
    >>> from geolysis.core.bearing_capacity import BowlesABC4PadFoundation
    >>> from geolysis.core.foundation import create_foundation, Shape

    >>> foundation_size = create_foundation(
    ...     depth=1.5, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> bowles_abc = BowlesABC4PadFoundation(
    ...     corrected_spt_number=17.0,
    ...     tol_settlement=20.0,
    ...     foundation_size=foundation_size,
    ... )
    """

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    # @Config.assign_unit(
    #     default_unit=ureg.kPa,
    #     cgs_unit=UnitSystem.CGS.Pressure,
    #     mks_unit=UnitSystem.MKS.Pressure,
    #     imperial_unit=UnitSystem.IMPERIAL.Pressure,
    #     si_unit=UnitSystem.SI.Pressure,
    # )
    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        B = self.foundation_size.width
        D = self.foundation_size.depth
        FD = min(1 + 0.33 * D / B, 1.33)
        SR = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        N_CORR = self.corrected_spt_number

        if B <= 1.2:
            return 19.16 * N_CORR * FD * SR

        return 11.98 * N_CORR * ((3.28 * B + 1) / (3.28 * B)) ** 2 * FD * SR


class BowlesABC4MatFoundation(AbstractABC):
    r"""Allowable bearing capacity for mat foundation on cohesionless
    soils according to ``Bowles (1997)``.

    Parameters
    ----------
    corrected_spt_number : float
        Statistical average of corrected SPT N-value (55% energy with
        overburden pressure correction) within the foundation influence
        zone i.e ``0.5B`` to ``2B``.
    tol_settlement : float, mm
        Tolerable settlement.
    foundation_size : FoundationSize
        Size of foundation.

    Notes
    -----
    Allowable bearing capacity for ``raft/mat`` foundations:

    .. math:: q_a(kPa) = 11.98(N_1)_{55}f_d\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    Examples
    --------
    >>> from geolysis.core.bearing_capacity import BowlesABC4MatFoundation
    >>> from geolysis.core.foundation import create_foundation, Shape

    >>> foundation_size = create_foundation(
    ...     depth=1.5, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> bowles_abc = BowlesABC4MatFoundation(
    ...     corrected_spt_number=17.0,
    ...     tol_settlement=20.0,
    ...     foundation_size=foundation_size,
    ... )
    """

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        B = self.foundation_size.width
        D = self.foundation_size.depth
        FD = min(1 + 0.33 * D / B, 1.33)
        SR = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        N_CORR = self.corrected_spt_number

        return 11.98 * N_CORR * FD * SR


class MeyerhofABC4PadFoundation(AbstractABC):
    r"""Allowable bearing capacity for pad foundation on cohesionless
    soils according to ``Meyerhof (1956)``.

    Parameters
    ----------
    corrected_spt_number : float
        Average uncorrected SPT N-value (60% energy with dilatancy
        (water) correction if applicable) within the foundation influence
        zone i.e :math:`D_f` to :math:`D_f + 2B`
    tol_settlement : float, mm
        Tolerable settlement
    foundation_size : FoundationSize
        Size of foundation.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 12N f_d\left(\dfrac{S}{25.4}\right), \ B \ \le 1.2m

        q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d\left(
                     \dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    Examples
    --------
    >>> from geolysis.core.bearing_capacity import MeyerhofABC4PadFoundation
    >>> from geolysis.core.foundation import create_foundation, Shape

    >>> foundation_size = create_foundation(
    ...     depth=1.5, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> meyerhof_abc = MeyerhofABC4PadFoundation(
    ...     corrected_spt_number=17.0,
    ...     tol_settlement=20.0,
    ...     foundation_size=foundation_size,
    ... )
    """

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        B = self.foundation_size.width
        D = self.foundation_size.depth
        FD = min(1 + 0.33 * D / B, 1.33)
        SR = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        N_CORR = self.corrected_spt_number

        if B <= 1.2:
            return 12 * N_CORR * FD * SR

        return 8 * N_CORR * ((3.28 * B + 1) / (3.28 * B)) ** 2 * FD * SR


class MeyerhofABC4MatFoundation(AbstractABC):
    r"""Allowable bearing capacity for mat foundation on cohesionless
    soils according to ``Meyerhof (1956)``.

    Parameters
    ----------
    corrected_spt_number : float
        Average uncorrected SPT N-value (60% energy with dilatancy
        (water) correction if applicable) within the foundation influence
        zone i.e :math:`D_f` to :math:`D_f + 2B`
    tol_settlement : float, mm
        Tolerable settlement
    foundation_size : FoundationSize
        Size of foundation.

    Notes
    -----
    Allowable bearing capacity for ``raft/mat`` foundations:

    .. math:: q_a(kPa) = 8 N f_d\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    Examples
    --------
    >>> from geolysis.core.bearing_capacity import MeyerhofABC4MatFoundation
    >>> from geolysis.core.foundation import create_foundation, Shape

    >>> foundation_size = create_foundation(
    ...     depth=1.5, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> meyerhof_abc = MeyerhofABC4MatFoundation(
    ...     corrected_spt_number=17.0,
    ...     tol_settlement=20.0,
    ...     foundation_size=foundation_size,
    ... )
    """

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        B = self.foundation_size.width
        D = self.foundation_size.depth
        FD = min(1 + 0.33 * D / B, 1.33)
        SR = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        N_CORR = self.corrected_spt_number

        return 8 * N_CORR * FD * SR


class TerzaghiABC4PadFoundation(AbstractABC):
    r"""Allowable bearing capacity for pad foundation on cohesionless
    soils according to ``Terzaghi & Peck (1948)``.

    Parameters
    ----------
    corrected_spt_number : float
        Lowest (or average) uncorrected SPT N-value (60% energy) within
        the foundation influence zone i.e :math:`D_f` to :math:`D_f + 2B`
    tol_settlement : float, mm
        Tolerable settlement.
    water_depth : float, m
        Depth of water below ground surface.
    foundation_size : float
        Size of foundation.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right),
                    \ B \ \le 1.2m

        q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}
                    {c_w f_d}\left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Depth factor:

    .. math:: f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

    Water correction for surface footing:

    .. math:: c_w = 2 - \frac{D_w}{2B} \le 2

    Water correction for fully submerged footing :math:`D_w \le D_f`

    .. math:: c_w = 2 - \frac{D_f}{2B} \le 2

    Examples
    --------
    >>> from geolysis.core.bearing_capacity import TerzaghiABC4PadFoundation
    >>> from geolysis.core.foundation import create_foundation, Shape

    >>> foundation_size = create_foundation(
    ...     depth=1.5, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> terzaghi_abc = TerzaghiABC4PadFoundation(
    ...     corrected_spt_number=17,
    ...     tol_settlement=20.0,
    ...     water_depth=1.2,
    ...     foundation_size=foundation_size,
    ... )
    """

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        water_depth: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size
        self.water_depth = water_depth

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        B = self.foundation_size.width
        D = self.foundation_size.depth
        FD = min(1 + 0.25 * D / B, 1.25)
        SR = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        N_CORR = self.corrected_spt_number

        if self.water_depth <= D:
            CW = 2 - D / (2 * B)
        else:
            CW = 2 - self.water_depth / (2 * B)

        CW = min(CW, 2)

        if B <= 1.2:
            return 12 * N_CORR * (1 / (CW * FD)) * SR

        return (
            8
            * N_CORR
            * ((3.28 * B + 1) / (3.28 * B)) ** 2
            * (1 / (CW * FD))
            * SR
        )


class TerzaghiABC4MatFoundation(AbstractABC):
    r"""Allowable bearing capacity for mat foundation on cohesionless soils
    according to ``Terzaghi & Peck (1948)``.

    Parameters
    ----------
    corrected_spt_number : float
        Lowest (or average) uncorrected SPT N-value (60% energy) within
        the foundation influence zone i.e :math:`D_f` to :math:`D_f + 2B`
    tol_settlement : float, mm
        Tolerable settlement.
    water_depth : float, m
        Depth of water below ground surface.
    foundation_size : float
        Size of foundation.

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math:: q_a(kPa) = 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

    Water correction for surface footing:

    .. math:: c_w = 2 - \frac{D_w}{2B} \le 2

    Water correction for fully submerged footing :math:`D_w \le D_f`

    .. math:: c_w = 2 - \frac{D_f}{2B} \le 2

    Examples
    --------
    >>> from geolysis.core.bearing_capacity import TerzaghiABC4MatFoundation
    >>> from geolysis.core.foundation import create_foundation, Shape

    >>> foundation_size = create_foundation(
    ...     depth=1.5, width=1.2, footing_shape=Shape.SQUARE
    ... )
    >>> terzaghi_abc = TerzaghiABC4MatFoundation(
    ...     corrected_spt_number=17,
    ...     tol_settlement=20.0,
    ...     water_depth=1.2,
    ...     foundation_size=foundation_size,
    ... )
    """

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        water_depth: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.foundation_size = foundation_size
        self.water_depth = water_depth

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        B = self.foundation_size.width
        D = self.foundation_size.depth
        FD = min(1 + 0.25 * D / B, 1.25)
        SR = self.tol_settlement / self.MAX_TOL_SETTLEMENT
        N_CORR = self.corrected_spt_number

        if self.water_depth <= D:
            CW = 2 - D / (2 * B)
        else:
            CW = 2 - self.water_depth / (2 * B)

        CW = min(CW, 2)

        return 8 * N_CORR * (1 / (CW * FD)) * SR
