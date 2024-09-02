from abc import ABC, abstractmethod

from geolysis.core.foundation import FoundationSize
from geolysis.core.utils import quantity, round_

# import geolysis.core.constants as constants

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


#: TODO: change B, D
def _get_attributes(obj):
    """
    - **B** : width of foundation footing
    - **D** : depth of foundation footing
    - **SR** : settlement ratio S_tol / S_max
    - **N_CORR** : corrected spt number
    """
    f_w = obj.foundation_size.width
    f_d = obj.foundation_size.depth
    SR = obj.tol_settlement / obj.MAX_TOL_SETTLEMENT
    N_CORR = obj.corrected_spt_number
    return f_w, f_d, SR, N_CORR


class AllowableBearingCapacity(ABC):
    #: Maximum tolerable foundation settlement.
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:
        self.corrected_spt_number = corrected_spt_number
        self.foundation_size = foundation_size
        self.tol_settlement = tol_settlement

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @abstractmethod
    def bearing_capacity(self): ...


class BowlesABC4PadFoundation(AllowableBearingCapacity):
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

    @quantity("Pressure")
    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        f_w = self.foundation_size.width
        SR, FD = _get_fts(self)
        N_CORR = self.corrected_spt_number

        if f_w <= 1.2:
            return 19.16 * N_CORR * FD * SR

        return (
            11.98 * N_CORR * ((3.28 * f_w + 1) / (3.28 * f_w)) ** 2 * FD * SR
        )


class BowlesABC4MatFoundation(AllowableBearingCapacity):
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

    @quantity("Pressure")
    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        SR, FD = _get_fts(self)
        N_CORR = self.corrected_spt_number

        return 11.98 * N_CORR * FD * SR


class MeyerhofABC4PadFoundation(AllowableBearingCapacity):
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

    @quantity("Pressure")
    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        f_w = self.foundation_size.width
        SR, FD = _get_fts(self)
        N_CORR = self.corrected_spt_number

        if f_w <= 1.2:
            return 12 * N_CORR * FD * SR

        return 8 * N_CORR * ((3.28 * f_w + 1) / (3.28 * f_w)) ** 2 * FD * SR


class MeyerhofABC4MatFoundation(AllowableBearingCapacity):
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

    @quantity("Pressure")
    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        SR, FD = _get_fts(self)
        N_CORR = self.corrected_spt_number

        return 8 * N_CORR * FD * SR


class TerzaghiABC4PadFoundation(AllowableBearingCapacity):
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
        super().__init__(corrected_spt_number, tol_settlement, foundation_size)

        self.water_depth = water_depth

    @quantity("Pressure")
    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        f_d, f_w, *_ = self.foundation_size.get_info()
        SR, FD = _get_fts(self)
        N_CORR = self.corrected_spt_number

        if self.water_depth <= f_d:
            CW = 2 - f_d / (2 * f_w)
        else:
            CW = 2 - self.water_depth / (2 * f_w)

        CW = min(CW, 2)

        if f_w <= 1.2:
            return 12 * N_CORR * (1 / (CW * FD)) * SR

        return (
            8
            * N_CORR
            * ((3.28 * f_w + 1) / (3.28 * f_w)) ** 2
            * (1 / (CW * FD))
            * SR
        )


class TerzaghiABC4MatFoundation(AllowableBearingCapacity):
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
        super().__init__(corrected_spt_number, tol_settlement, foundation_size)

        self.water_depth = water_depth

    @quantity("Pressure")
    @round_
    def bearing_capacity(self):
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        f_d, f_w, *_ = self.foundation_size.get_info()
        SR, FD = _get_fts(self)
        N_CORR = self.corrected_spt_number

        if self.water_depth <= f_d:
            CW = 2 - f_d / (2 * f_w)
        else:
            CW = 2 - self.water_depth / (2 * f_w)

        CW = min(CW, 2)

        return 8 * N_CORR * (1 / (CW * FD)) * SR


def _get_fts(obj: AllowableBearingCapacity):
    SR = obj.tol_settlement / obj.MAX_TOL_SETTLEMENT
    f_d, f_w, *_ = obj.foundation_size.get_info()
    FD = min(1 + 0.33 * f_d / f_w, 1.33)

    if isinstance(obj, (TerzaghiABC4PadFoundation, TerzaghiABC4MatFoundation)):
        FD = min(1 + 0.25 * f_d / f_w, 1.25)

    return SR, FD
