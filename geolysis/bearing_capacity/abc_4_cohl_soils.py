from geolysis.foundation import FoundationSize
from geolysis.utils import round_

__all__ = ["BowlesABC", "MeyerhofABC", "TerzaghiABC"]


class SettlementError(ValueError):
    pass


def _chk_settlement(tol_settlement: float, max_tol_settlement: float):
    if tol_settlement > max_tol_settlement:
        err_msg = "tol_settlement should not be greater than 25.4."
        raise SettlementError(err_msg)


class BowlesABC:
    r"""Allowable bearing capacity for cohesionless soils according to
    ``Bowles (1997)``.

    Parameters
    ----------
    corrected_spt_number : float
        Statistical average of corrected SPT N-value (55% energy with overburden
        pressure correction) within the foundation influence zone i.e ``0.5B`` to
        ``2B``.
    tol_settlement : float, unit=millimetre
        Tolerable settlement.
    foundation_size : FoundationSize
        Size of foundation.

    Attributes
    ----------
    corrected_spt_number : float
    tol_settlement : float
    f_depth : float
        Depth of foundation
    f_width : float
        Width of foundation footing
    FD : float
        Depth factor.
    MAX_TOL_SETTLEMENT : float

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 19.16(N_1)_{55} f_d\left(\dfrac{S}{25.4}\right), \ B \ \le \ 1.2m

        q_a(kPa) &= 11.8(N_1)_{55}\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d
                    \left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Allowable bearing capacity for ``raft/mat`` foundations:

    .. math:: q_a(kPa) = 11.98(N_1)_{55}f_d\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    Examples
    --------
    >>> from geolysis.bearing_capacity.abc_4_cohl_soils import BowlesABC
    >>> from geolysis.foundation import create_foundation

    >>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
    ...                                     width=1.2, footing_shape="square")
    >>> bowles_abc = BowlesABC(corrected_spt_number=17.0,
    ...                        tol_settlement=20.0,
    ...                        foundation_size=foundation_size)
    >>> bowles_abc.abc_4_pad_foundation()
    341.11
    >>> bowles_abc.abc_4_mat_foundation()
    213.28

    >>> bowles_abc.f_width = 1.4
    >>> bowles_abc.abc_4_pad_foundation()
    316.29

    >>> BowlesABC(corrected_spt_number=11.0, tol_settlement=30.0,
    ...           foundation_size=foundation_size)
    Traceback (most recent call last):
        ...
    SettlementError: tol_settlement should not be greater than 25.4.
    """

    #: Maximum tolerable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:

        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement

        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @property
    def FD(self) -> float:
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @property
    def SR(self) -> float:
        return self.tol_settlement / self.MAX_TOL_SETTLEMENT

    @property
    def N_1_55(self) -> float:
        return self.corrected_spt_number

    @round_(ndigits=2)
    def abc_4_pad_foundation(self) -> float:
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        if self.f_width <= 1.2:
            return 19.16 * self.N_1_55 * self.FD * self.SR

        return (
            11.98
            * self.N_1_55
            * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
            * self.FD
            * self.SR
        )

    @round_(ndigits=2)
    def abc_4_mat_foundation(self) -> float:
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        return 11.98 * self.N_1_55 * self.FD * self.SR


class MeyerhofABC:
    r"""Allowable bearing capacity for cohesionless soils according to
    ``Meyerhof (1956)``.

    Parameters
    ----------
    corrected_spt_number : float
        Average uncorrected SPT N-value (60% energy with dilatancy (water) correction
        if applicable) within the foundation influence zone i.e :math:`D_f` to
        :math:`D_f + 2B`
    tol_settlement : float, unit=millimetre
        Tolerable settlement
    foundation_size : FoundationSize
        Size of foundation.

    Attributes
    ----------
    corrected_spt_number : float
    tol_settlement : float
    f_depth : float
        Depth of foundation footing
    f_width : float
        Width of foundation footing
    FD : float
        Depth factor
    MAX_TOL_SETTLEMENT : float

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 12N f_d\left(\dfrac{S}{25.4}\right), \ B \ \le 1.2m

        q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2 f_d\left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Allowable bearing capacity for ``raft/mat`` foundations:

    .. math:: q_a(kPa) = 8 N f_d\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.33 \cdot \frac{D_f}{B} \le 1.33

    Examples
    --------
    >>> from geolysis.bearing_capacity.abc_4_cohl_soils import MeyerhofABC
    >>> from geolysis.foundation import create_foundation

    >>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
    ...                                     width=1.2, footing_shape="square")
    >>> meyerhof_abc = MeyerhofABC(corrected_spt_number=17.0, tol_settlement=20.0,
    ...                            foundation_size=foundation_size)
    >>> meyerhof_abc.abc_4_pad_foundation()
    213.64
    >>> meyerhof_abc.abc_4_mat_foundation()
    142.43

    >>> meyerhof_abc.f_width = 1.4
    >>> meyerhof_abc.abc_4_pad_foundation()
    211.21

    >>> MeyerhofABC(corrected_spt_number=15, tol_settlement=30.0,
    ...             foundation_size=foundation_size)
    Traceback (most recent call last):
        ...
    SettlementError: tol_settlement should not be greater than 25.4.
    """

    #: Maximum tolerable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        foundation_size: FoundationSize,
    ) -> None:

        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement

        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @property
    def FD(self) -> float:
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @property
    def SR(self) -> float:
        return self.tol_settlement / self.MAX_TOL_SETTLEMENT

    @property
    def N_1_60(self) -> float:
        return self.corrected_spt_number

    @round_(ndigits=2)
    def abc_4_pad_foundation(self) -> float:
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """

        if self.f_width <= 1.2:
            return 12 * self.N_1_60 * self.FD * self.SR

        return (
            8
            * self.N_1_60
            * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
            * self.FD
            * self.SR
        )

    @round_(ndigits=2)
    def abc_4_mat_foundation(self) -> float:
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        return 8 * self.N_1_60 * self.FD * self.SR


class TerzaghiABC:
    r"""Allowable bearing capacity for cohesionless soils according to
    ``Terzaghi & Peck (1948)``.

    Parameters
    ----------
    corrected_spt_number : float
        Lowest (or average) uncorrected SPT N-value (60% energy) within the
        foundation influence zone i.e :math:`D_f` to :math:`D_f + 2B`
    tol_settlement : float, unit=millimetre
        Tolerable settlement.
    water_depth : float, unit=metre
        Depth of water below ground surface.
    foundation_size : float
        Size of foundation.

    Attributes
    ----------
    corrected_spt_number : float
    tol_settlement : float
    water_depth : float
    f_depth : float
        Depth of foundation
    f_width : float
        Width of foundation footing
    FD : float
        Depth factor
    CW : float
        Water correction factor
    MAX_TOL_SETTLEMENT : float

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) &= 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right), \ B \ \le 1.2m

        q_a(kPa) &= 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}{c_w f_d}
                    \left(\dfrac{S}{25.4}\right), \ B \ \gt 1.2m

    Allowable bearing capacity for ``raft/mat`` foundations:

    .. math:: q_a(kPa) = 8N\dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right)

    Depth factor:

    .. math:: f_d = 1 + 0.25 \cdot \frac{D_f}{B} \le 1.25

    Water correction for surface footing:

    .. math:: c_w = 2 - \frac{D_w}{2B} \le 2

    Water correction for fully submerged footing :math:`D_w \le D_f`

    .. math:: c_w = 2 - \frac{D_f}{2B} \le 2

    Examples
    --------
    >>> from geolysis.bearing_capacity.abc_4_cohl_soils import TerzaghiABC
    >>> from geolysis.foundation import create_foundation

    >>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
    ...                                     width=1.2, footing_shape="square")
    >>> terzaghi_abc = TerzaghiABC(corrected_spt_number=6, tol_settlement=20.0,
    ...                            water_depth=1.2, foundation_size=foundation_size)
    >>> terzaghi_abc.N_1_60
    6
    >>> terzaghi_abc.abc_4_pad_foundation()
    32.87
    >>> terzaghi_abc.abc_4_mat_foundation()
    21.91

    >>> terzaghi_abc.f_width = 1.4
    >>> terzaghi_abc.water_depth = 1.7
    >>> terzaghi_abc.abc_4_pad_foundation()
    32.26
    >>> terzaghi_abc.abc_4_mat_foundation()
    21.75

    >>> TerzaghiABC(corrected_spt_number=15, tol_settlement=30.0,
    ...             water_depth=1.8, foundation_size=foundation_size)
    Traceback (most recent call last):
        ...
    SettlementError: tol_settlement should not be greater than 25.4.
    """

    #: Maximum allowable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
        self,
        corrected_spt_number: float,
        tol_settlement: float,
        water_depth: float,
        foundation_size: FoundationSize,
    ) -> None:

        self.corrected_spt_number = corrected_spt_number
        self.tol_settlement = tol_settlement
        self.water_depth = water_depth

        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @property
    def N_1_60(self) -> float:
        return self.corrected_spt_number

    @property
    def SR(self) -> float:
        return self.tol_settlement / self.MAX_TOL_SETTLEMENT

    @property
    @round_(ndigits=2)
    def FD(self):
        return min(1 + 0.25 * self.f_depth / self.f_width, 1.25)

    @property
    @round_(ndigits=2)
    def CW(self):
        return (
            min(2 - self.f_depth / (2 * self.f_width), 2)
            if self.water_depth <= self.f_depth
            else min(2 - self.water_depth / (2 * self.f_width), 2)
        )

    @round_(ndigits=2)
    def abc_4_pad_foundation(self) -> float:
        """Return allowable bearing capacity for isolated foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        if self.f_width <= 1.2:
            return 12 * self.N_1_60 * (1 / (self.CW * self.FD)) * self.SR

        return (
            8
            * self.N_1_60
            * ((3.28 * self.f_width + 1) / (3.28 * self.f_width)) ** 2
            * (1 / (self.CW * self.FD))
            * self.SR
        )

    @round_(ndigits=2)
    def abc_4_mat_foundation(self) -> float:
        """Return allowable bearing capacity for raft foundation on
        cohesionless soils. |rarr| :math:`kN/m^2`
        """
        return 8 * self.N_1_60 * (1 / (self.CW * self.FD)) * self.SR
