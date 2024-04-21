from typing import Optional, Sequence

from geolysis.foundation import FoundationSize
from geolysis.spt import SPT, SPTCorrection
from geolysis.utils import floor, round_

__all__ = ["BowlesABC1997", "MeyerhofABC1956", "TerzaghiABC1948"]


class SettlementError(ValueError):
    pass


def _chk_settlement(tol_settlement: float, max_tol_settlement: float):
    if tol_settlement > max_tol_settlement:
        err_msg = "tol_settlement should not be greater than 25.4."
        raise SettlementError(err_msg)


ERR_MSG = "recorded_spt_n_vals should be a Sequence[int] or float or int"


class BowlesABC1997:
    r"""Allowable bearing capacity for cohesionless soils according to
    ``Bowles (1997)``.

    Parameters
    ----------
    recorded_spt_n_vals : Sequence[int] | float
        If ``recorded_spt_n_vals`` is a Sequence, it is taken as ``recorded SPT N-values``
        within the foundation influence zone i.e ``0.5B`` to ``2B``. If it is a float, then
        it is taken as ``corrected SPT N-value``
    tol_settlement : float, unit=millimetre
        Tolerable settlement.
    foundation_size : FoundationSize
        Size of foundation.
    eop : float, default=None, unit= :math:`kN/m^2`
        Effective overburden pressure. If ``recorded_SPT_N_vals`` is a Sequence, then ``eop``
        is required to calculate the ``corrected SPT N-value``

    Attributes
    ----------
    tol_settlement : float
    f_depth : float
        Depth of foundation
    f_width : float
        Width of foundation footing
    N_1_55 : float
        Statistical average of corrected SPT N-value (55% energy with overburden
        pressure correction)
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
    >>> from geolysis.bearing_capacity.abc_4_cohl_soils import BowlesABC1997
    >>> from geolysis.foundation import create_foundation

    >>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
    ...                                     width=1.2, footing_shape="square")
    >>> recorded_spt_n_vals = [8, 15, 23, 30, 38]

    >>> bowles_abc = BowlesABC1997(recorded_spt_n_vals=recorded_spt_n_vals,
    ...                            tol_settlement=20.0,
    ...                            foundation_size=foundation_size, eop=100.0)
    >>> bowles_abc.N_1_55
    17
    >>> bowles_abc.abc_4_pad_foundation()
    341.11
    >>> bowles_abc.abc_4_mat_foundation()
    213.28

    >>> bowles_abc.f_width = 1.4
    >>> bowles_abc.abc_4_pad_foundation()
    316.29

    >>> bowles_abc = BowlesABC1997(recorded_spt_n_vals=11.0, tol_settlement=20.0,
    ...                            foundation_size=foundation_size)
    >>> bowles_abc.abc_4_pad_foundation()
    220.72
    >>> bowles_abc.abc_4_mat_foundation()
    138.01

    >>> BowlesABC1997(recorded_spt_n_vals=11.0, tol_settlement=30.0,
    ...               foundation_size=foundation_size)
    Traceback (most recent call last):
        ...
    SettlementError: tol_settlement should not be greater than 25.4.
    """

    #: Maximum tolerable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
        self,
        recorded_spt_n_vals: Sequence[int] | float,
        tol_settlement: float,
        foundation_size: FoundationSize,
        eop: float = 100.0,
    ) -> None:

        if isinstance(recorded_spt_n_vals, Sequence):
            self._avg_corr_spt_n_val = self._calculate_spt_avg(
                recorded_spt_n_vals, eop
            )
        if isinstance(recorded_spt_n_vals, (float, int)):
            self._avg_corr_spt_n_val = recorded_spt_n_vals

        self.tol_settlement = tol_settlement

        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @staticmethod
    def _calculate_spt_avg(
        recorded_spt_n_vals: Sequence[int], eop: float
    ) -> float:
        corrected_spts: list[float] = []

        for recorded_spt in recorded_spt_n_vals:
            spt_correction = SPTCorrection(
                recorded_spt_n_val=recorded_spt,
                eop=eop,
                energy_percentage=0.55,
            )
            corrected_spt = spt_correction.bazaraa_peck_opc_1969()
            corrected_spts.append(corrected_spt)

        return SPT(corrected_spt_n_vals=corrected_spts).average()

    @property
    def FD(self) -> float:
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @property
    def SR(self) -> float:
        return self.tol_settlement / self.MAX_TOL_SETTLEMENT

    @property
    def N_1_55(self) -> float:
        return floor(self._avg_corr_spt_n_val)

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


class MeyerhofABC1956:
    r"""Allowable bearing capacity for cohesionless soils according to
    ``Meyerhof (1956)``.

    Parameters
    ----------
    recorded_spt_n_vals : Sequence[int] | float
        If ``recorded_spt_n_vals`` is a Sequence, it is taken as ``recorded SPT N-values``
        within the foundation influence zone i.e :math:`D_f` to :math:`D_f + 2B``. If it is
        a float, then it is taken as ``average uncorrected SPT N-value``. Only water table
        correction is suggested.
    tol_settlement : float, unit=millimetre
        Tolerable settlement
    foundation_size : FoundationSize
        Size of foundation.
    wtc : bool, default=False
        Indicates whether to apply water correction factors when calculating for
        bearing capacities.

    Attributes
    ----------
    tol_settlement : float
    f_depth : float
        Depth of foundation footing
    f_width : float
        Width of foundation footing
    N_1_60 : float
        Average uncorrected SPT N-value (60% energy with dilatancy (water) correction
        if applicable)
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
    >>> from geolysis.bearing_capacity.abc_4_cohl_soils import MeyerhofABC1956
    >>> from geolysis.foundation import create_foundation

    >>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
    ...                                     width=1.2, footing_shape="square")
    >>> recorded_spt_n_vals = [8, 15, 23, 30, 38]

    >>> meyerhof_abc = MeyerhofABC1956(recorded_spt_n_vals=recorded_spt_n_vals, tol_settlement=20.0,
    ...                              foundation_size=foundation_size)
    >>> meyerhof_abc.N_1_60
    17
    >>> meyerhof_abc.abc_4_pad_foundation()
    213.64
    >>> meyerhof_abc.abc_4_mat_foundation()
    142.43

    >>> meyerhof_abc.f_width = 1.4
    >>> meyerhof_abc.abc_4_pad_foundation()
    211.21

    >>> meyerhof_abc = MeyerhofABC1956(recorded_spt_n_vals=recorded_spt_n_vals, tol_settlement=20.0,
    ...                                foundation_size=foundation_size, wtc=True)
    >>> meyerhof_abc.N_1_60
    14
    >>> meyerhof_abc.abc_4_pad_foundation()
    175.94
    >>> meyerhof_abc.abc_4_mat_foundation()
    117.29

    >>> MeyerhofABC1956(recorded_spt_n_vals=11.0, tol_settlement=30.0,
    ...                 foundation_size=foundation_size)
    Traceback (most recent call last):
        ...
    SettlementError: tol_settlement should not be greater than 25.4.
    """

    #: Maximum tolerable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
        self,
        recorded_spt_n_vals: Sequence[int] | float,
        tol_settlement: float,
        foundation_size: FoundationSize,
        wtc=False,
    ) -> None:

        if isinstance(recorded_spt_n_vals, Sequence):
            self._avg_corr_spt_n_val = self._calculate_spt_avg(
                recorded_spt_n_vals, wtc
            )
        if isinstance(recorded_spt_n_vals, (float, int)):
            self._avg_corr_spt_n_val = recorded_spt_n_vals

        self.tol_settlement = tol_settlement

        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @staticmethod
    def _calculate_spt_avg(
        recorded_spt_n_vals: Sequence[int], wtc: bool
    ) -> float:
        corrected_spts: list[float] = []

        for recorded_spt in recorded_spt_n_vals:
            spt_correction = SPTCorrection(recorded_spt_n_val=recorded_spt)
            corrected_spt = (
                spt_correction.terzaghi_peck_dc_1948()
                if wtc
                else spt_correction.energy_correction()
            )
            corrected_spts.append(corrected_spt)

        return SPT(corrected_spt_n_vals=corrected_spts).average()

    @property
    def FD(self) -> float:
        return min(1 + 0.33 * self.f_depth / self.f_width, 1.33)

    @property
    def SR(self) -> float:
        return self.tol_settlement / self.MAX_TOL_SETTLEMENT

    @property
    def N_1_60(self) -> float:
        return floor(self._avg_corr_spt_n_val)

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


class TerzaghiABC1948:
    r"""Allowable bearing capacity for cohesionless soils according to
    ``Terzaghi & Peck (1948)``.

    Parameters
    ----------
    recorded_spt_n_vals : Sequence[int] | float
        If ``recorded_spt_n_vals`` is a Sequence, it is taken as ``recorded SPT N-values``
        within the foundation influence zone i.e :math:`D_f` to :math:`D_f + 2B``. If it
        is a float, then it is taken as ``average uncorrected SPT N-value``.
    tol_settlement : float, unit=millimetre
        Tolerable settlement.
    water_depth : float, unit=metre
        Depth of water below ground surface.
    foundation_size : float
        Size of foundation.

    Attributes
    ----------
    tol_settlement : float
    water_depth : float
    f_depth : float
        Depth of foundation
    f_width : float
        Width of foundation footing
    N_60 : float
        Lowest uncorrected SPT N-value (60% energy)
    FD : float
        Depth factor
    CW : float
        Water correction factor
    MAX_TOL_SETTLEMENT : float

    Notes
    -----
    Allowable bearing capacity for ``isolated/pad/spread`` foundations:

    .. math::

        q_a(kPa) = 12N \dfrac{1}{c_w f_d}\left(\dfrac{S}{25.4}\right), \ B \ \le 1.2m

        q_a(kPa) = 8N\left(\dfrac{3.28B + 1}{3.28B} \right)^2\dfrac{1}{c_w f_d}
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
    >>> from geolysis.bearing_capacity.abc_4_cohl_soils import TerzaghiABC1948
    >>> from geolysis.foundation import create_foundation

    >>> foundation_size = create_foundation(depth=1.5, thickness=0.3,
    ...                                     width=1.2, footing_shape="square")
    >>> recorded_spt_n_vals = [8, 15, 23, 30, 38]

    >>> terzaghi_abc = TerzaghiABC1948(recorded_spt_n_vals=recorded_spt_n_vals,
    ...                                tol_settlement=20.0, water_depth=1.2,
    ...                                foundation_size=foundation_size)
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
    """

    #: Maximum allowable settlement. (mm)
    MAX_TOL_SETTLEMENT = 25.4

    def __init__(
        self,
        recorded_spt_n_vals: Sequence[int] | float,
        tol_settlement: float,
        water_depth: float,
        foundation_size: FoundationSize,
    ) -> None:

        if isinstance(recorded_spt_n_vals, Sequence):
            self._avg_corr_spt_n_val = self._calculate_spt_avg(
                recorded_spt_n_vals
            )
        if isinstance(recorded_spt_n_vals, (float, int)):
            self._avg_corr_spt_n_val = recorded_spt_n_vals

        self.tol_settlement = tol_settlement
        self.water_depth = water_depth

        self.f_depth = foundation_size.depth
        self.f_width = foundation_size.width

        _chk_settlement(self.tol_settlement, self.MAX_TOL_SETTLEMENT)

    @staticmethod
    def _calculate_spt_avg(recorded_SPT_N_vals: Sequence[float]) -> float:
        corrected_spts: list[float] = []

        for recorded_spt in recorded_SPT_N_vals:
            spt_correction = SPTCorrection(recorded_spt_n_val=recorded_spt)
            corrected_spt = spt_correction.energy_correction()
            corrected_spts.append(corrected_spt)

        return SPT(corrected_spt_n_vals=corrected_spts).min()

    @property
    def N_1_60(self) -> float:
        return floor(self._avg_corr_spt_n_val)

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
